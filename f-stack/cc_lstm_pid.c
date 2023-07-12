/*-
 * SPDX-License-Identifier: BSD-2-Clause-FreeBSD
 *
 * Copyright (c) 2008-2010 Lawrence Stewart <lstewart@freebsd.org>
 * Copyright (c) 2010 The FreeBSD Foundation
 * All rights reserved.
 *
 * This software was developed by Lawrence Stewart while studying at the Centre
 * for Advanced Internet Architectures, Swinburne University of Technology, made
 * possible in part by a grant from the Cisco University Research Program Fund
 * at Community Foundation Silicon Valley.
 *
 * Portions of this software were developed at the Centre for Advanced
 * Internet Architectures, Swinburne University of Technology, Melbourne,
 * Australia by David Hayes under sponsorship from the FreeBSD Foundation.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 */

/*
 * An implementation of the CUBIC congestion control algorithm for FreeBSD,
 * based on the Internet Draft "draft-rhee-tcpm-cubic-02" by Rhee, Xu and Ha.
 * Originally released as part of the NewTCP research project at Swinburne
 * University of Technology's Centre for Advanced Internet Architectures,
 * Melbourne, Australia, which was made possible in part by a grant from the
 * Cisco University Research Program Fund at Community Foundation Silicon
 * Valley. More details are available at:
 *   http://caia.swin.edu.au/urp/newtcp/
 */

#include <sys/cdefs.h>
__FBSDID("$FreeBSD$");

#include <sys/param.h>
#include <sys/kernel.h>
#include <sys/limits.h>
#include <sys/malloc.h>
#include <sys/module.h>
#include <sys/socket.h>
#include <sys/socketvar.h>
#include <sys/sysctl.h>
#include <sys/systm.h>

#include <net/vnet.h>

#include <netinet/tcp.h>
#include <netinet/tcp_seq.h>
#include <netinet/tcp_timer.h>
#include <netinet/tcp_var.h>
#include <netinet/cc/cc.h>
#include <netinet/cc/cc_cubic.h>
#include <netinet/cc/cc_module.h>
#define Mbps 6
static void	lstm_pid_ack_received(struct cc_var *ccv, uint16_t type);
static void	lstm_pid_cb_destroy(struct cc_var *ccv);
static int	lstm_pid_cb_init(struct cc_var *ccv);
static void	lstm_pid_cong_signal(struct cc_var *ccv, uint32_t type);
static void	lstm_pid_conn_init(struct cc_var *ccv);
static int	lstm_pid_mod_init(void);
static void	lstm_pid_post_recovery(struct cc_var *ccv);
static void	lstm_pid_record_rtt(struct cc_var *ccv);
static void	lstm_pid_ssthresh_update(struct cc_var *ccv, uint32_t maxseg);
static void	lstm_pid_after_idle(struct cc_var *ccv);
static int	per_rtt_check(struct cc_var *ccv);
static float    rtt_predict(struct cc_var *ccv);
static float	pid_process(struct cc_var *ccv);
static void	change_wnd(struct cc_var *ccv,float c,float k);
struct lstm_pid {
	/* Cubic K in fixed point form with CUBIC_SHIFT worth of precision. */
	int64_t		K;
	/* Sum of RTT samples across an epoch in ticks. */
	int64_t		sum_rtt_ticks;
	/* cwnd at the most recent congestion event. */
	unsigned long	max_cwnd;
	/* cwnd at the previous congestion event. */
	unsigned long	prev_max_cwnd;
	/* A copy of prev_max_cwnd. Used for CC_RTO_ERR */
	unsigned long	prev_max_cwnd_cp;
	/* various flags */
	uint32_t	flags;
#define CUBICFLAG_CONG_EVENT	0x00000001	/* congestion experienced */
#define CUBICFLAG_IN_SLOWSTART	0x00000002	/* in slow start */
#define CUBICFLAG_IN_APPLIMIT	0x00000004	/* application limited */
#define CUBICFLAG_RTO_EVENT	0x00000008	/* RTO experienced */
	/* Minimum observed rtt in ticks. */
	int		min_rtt_ticks;
	/* Mean observed rtt between congestion epochs. */
	int		mean_rtt_ticks;
	/* ACKs since last congestion event. */
	int		epoch_ack_count;
	/* Timestamp (in ticks) of arriving in congestion avoidance from last
	 * congestion event.
	 */
	int		t_last_cong;
	/* Timestamp (in ticks) of a previous congestion event. Used for
	 * CC_RTO_ERR.
	 */
	int		t_last_cong_prev;
	uint32_t	send_seq;
	/*-------------lstm data--------------*/
	struct {
		int time;
	}explore;
	struct{
		int time;
		int inc;
		int range_max;
		int range_min;
		uint32_t type;
	}fast;
	int time;
	tcp_seq seq;
	int16_t packet_size;
	int32_t switch_bandwidth;
	int32_t minrate;
	int32_t maxrate;
	int32_t rate;
	struct{
		int begin_flag;
		int rtt_target;
		int rtt_min;
		float e;
		float eold;
		float eavg;
		float w[3];
		float range_min;
		float range_max;
		int target_qlen;
	}pid;
	struct{
		int rtt[3];
		int rtt_smooth;
		struct{
			float wi[16];
			float wh[64][16];
			float bi[64];
			float bh[64];
			float h[16];
			float c[16];
			float linearw[16];
			float linearb;
		}nn;
	}lstm;
};
static void pid_read_w(struct  lstm_pid *data);
static MALLOC_DEFINE(M_CUBIC, "lstm_pid data",
    "Per connection data required for the lstm_pid congestion control algorithm");

struct cc_algo lstm_pid_cc_algo = {
	.name = "lstm_pid",
	.ack_received = lstm_pid_ack_received,
	.cb_destroy = lstm_pid_cb_destroy,
	.cb_init = lstm_pid_cb_init,
	.cong_signal = lstm_pid_cong_signal,
	.conn_init = lstm_pid_conn_init,
	.mod_init = lstm_pid_mod_init,
	.post_recovery = lstm_pid_post_recovery,
	.after_idle = lstm_pid_after_idle,
};
static int per_rtt_check(struct cc_var *ccv){
	struct lstm_pid *cubic_data;
	cubic_data = ccv->cc_data;
	if(cubic_data->send_seq <= CCV(ccv, snd_una)){
		cubic_data->send_seq = 	CCV(ccv, snd_max);
		return 1;
	}
	else return 0;
		
}
static void
lstm_pid_ack_received(struct cc_var *ccv, uint16_t type)
{
	struct lstm_pid *lstm_pid_data;
	unsigned long w_tf, w_cubic_next;
	int ticks_since_cong;

	lstm_pid_data = ccv->cc_data;
	lstm_pid_record_rtt(ccv);
	int rtt =  TICKS_2_USEC(CCV(ccv, t_srtt)) >> TCP_RTT_SHIFT;
	if(type == CC_ACK && per_rtt_check(ccv)){
	/*update first rtt mess*/
	if(lstm_pid_data->pid.begin_flag == 0){
		lstm_pid_data->lstm.rtt[0] = rtt;
		lstm_pid_data->lstm.rtt[1] = rtt;
		lstm_pid_data->lstm.rtt[2] = rtt;
		lstm_pid_data->lstm.rtt_smooth = rtt;
		lstm_pid_data->pid.rtt_target = 0.9 * lstm_pid_data->lstm.rtt[0];
		lstm_pid_data->pid.rtt_min = lstm_pid_data->lstm.rtt[0];
		lstm_pid_data->pid.begin_flag = 1;
	}

	lstm_pid_data->lstm.rtt[0] = lstm_pid_data->lstm.rtt[1];
	lstm_pid_data->lstm.rtt[1] = lstm_pid_data->lstm.rtt[2];
	lstm_pid_data->lstm.rtt[2] = rtt;
	float target = lstm_pid_data->pid.rtt_target;
	
	float pr = rtt_predict(ccv);
	if(lstm_pid_data->time < lstm_pid_data->explore.time)
		lstm_pid_data->pid.rtt_target = 0.9*lstm_pid_data->pid.rtt_min;
	else {
		lstm_pid_data->pid.rtt_target = 100+lstm_pid_data->pid.rtt_min;

		if(rtt < lstm_pid_data->pid.rtt_min){
			lstm_pid_data->pid.rtt_min = rtt;
			lstm_pid_data->pid.rtt_target = 100+lstm_pid_data->pid.rtt_min;
		}
	}

	if(target ==  lstm_pid_data->pid.rtt_target && lstm_pid_data->time < lstm_pid_data->fast.time){
		lstm_pid_data->pid.eold = lstm_pid_data->pid.e;
		lstm_pid_data->pid.e = rtt - lstm_pid_data->pid.rtt_target;
	}else if(target !=  lstm_pid_data->pid.rtt_target){
		lstm_pid_data->pid.e = rtt - lstm_pid_data->pid.rtt_target;
		lstm_pid_data->pid.eold = lstm_pid_data->pid.e;
	}else{
		lstm_pid_data->pid.eold = lstm_pid_data->pid.e;
		lstm_pid_data->pid.e = rtt - lstm_pid_data->pid.rtt_target;
	}

	//CCV(ccv, snd_cwnd) = 2000;

	if(lstm_pid_data->time!=0){
		if(lstm_pid_data->pid.rtt_min == 0)printf("tim:%d\n",lstm_pid_data->time);
			lstm_pid_data->pid.eavg += lstm_pid_data->pid.e;
		if(lstm_pid_data->time <  lstm_pid_data->explore.time || lstm_pid_data->time%20 == 0)
			lstm_pid_data->pid.eavg = 0;
		int k;
		float c;
		if(lstm_pid_data->pid.e == -100){
			c = -8;
			k = 1;		
		}else{
			if(pr < lstm_pid_data->pid.rtt_min)pr = lstm_pid_data->pid.rtt_min;
			c = pid_process(ccv);
			k = 0;
		}
		change_wnd(ccv,c,k);	 
	}

	}
/*log print ccv data*/
	CCV(ccv,snd_cwnd) = 2000;
	printf("\n=============TCP============================");
	printf("\nswnd:%d,rwnd%d,cwnd:%d\n",CCV(ccv, snd_wnd),CCV(ccv, rcv_wnd),CCV(ccv, snd_cwnd));
	printf("srtt1:%d,srtt:%d,rttvar:%d,rttmin:%u,rttlow:%d,rttbest:%u\n",TICKS_2_USEC(CCV(ccv, t_srtt)) >> TCP_RTT_SHIFT,CCV(ccv, t_srtt),CCV(ccv, t_rttvar),CCV(ccv, t_rttmin),CCV(ccv, t_rttlow),CCV(ccv, t_rttbest));
	printf("snd_una:%u,snd_max:%u,snd_nxt:%u,rcv_nxt:%u\n",CCV(ccv, snd_una),CCV(ccv, snd_max),CCV(ccv, snd_nxt),CCV(ccv, rcv_nxt));
	printf("prate:%lld\n",(long long int)CCV(ccv, t_pacing_rate));
	//printf("pre_rtt check:%d seq:%u\n",per_rtt_check(ccv),cubic_data->send_seq);
	printf("================lstm=========================\n");
	printf("rtts:%d,%d,%d",lstm_pid_data->lstm.rtt[0],lstm_pid_data->lstm.rtt[1],lstm_pid_data->lstm.rtt[2]);
	printf("=========================================\n");
}

/*
 * This is a Cubic specific implementation of after_idle.
 *   - Reset cwnd by calling New Reno implementation of after_idle.
 *   - Reset t_last_cong.
 */
static void
lstm_pid_after_idle(struct cc_var *ccv)
{
	struct lstm_pid *cubic_data;

	cubic_data = ccv->cc_data;

	cubic_data->max_cwnd = ulmax(cubic_data->max_cwnd, CCV(ccv, snd_cwnd));
	cubic_data->K = cubic_k(cubic_data->max_cwnd / CCV(ccv, t_maxseg));

	newreno_cc_algo.after_idle(ccv);
	cubic_data->t_last_cong = ticks;
}

static void
lstm_pid_cb_destroy(struct cc_var *ccv)
{
	free(ccv->cc_data, M_CUBIC);
}

static int
lstm_pid_cb_init(struct cc_var *ccv)
{
	struct lstm_pid *cubic_data;

	cubic_data = malloc(sizeof(struct lstm_pid), M_CUBIC, M_NOWAIT|M_ZERO);

	struct lstm_pid *lstm_pid_data = cubic_data;	

	if (cubic_data == NULL)
		return (ENOMEM);

	/* Init some key variables with sensible defaults. */
	cubic_data->t_last_cong = ticks;
	cubic_data->min_rtt_ticks = TCPTV_SRTTBASE;
	cubic_data->mean_rtt_ticks = 1;
	/*----------- lstm ------------*/
	/* Init some key variables with sensible defaults. */
	lstm_pid_data->explore.time = 1;
	lstm_pid_data->minrate = 1 << Mbps;
	lstm_pid_data->maxrate = 100 << Mbps;
	lstm_pid_data->rate = 1 << Mbps;
	/*init fast*/
	lstm_pid_data->fast.time = 25;
	lstm_pid_data->fast.inc = (lstm_pid_data->maxrate - lstm_pid_data->minrate)/lstm_pid_data->fast.time;
	lstm_pid_data->fast.type = 1;
	/*init pid*/
	lstm_pid_data->pid.e = 0;
	lstm_pid_data->pid.eold = 0;
	lstm_pid_data->pid.eavg = 0;
	lstm_pid_data->pid.range_min = 0.1;
	lstm_pid_data->pid.range_max = 2;
	lstm_pid_data->pid.target_qlen = 12;
	lstm_pid_data->pid.begin_flag = 0;
	/**/
	lstm_pid_data->time = 0;
	lstm_pid_data->packet_size = 8000;
	lstm_pid_data->switch_bandwidth = 100 << Mbps;
	pid_read_w(lstm_pid_data);
	//ccv->cc_data = lstm_pid_data;
	ccv->cc_data = cubic_data;

	return (0);
}

/*
 * Perform any necessary tasks before we enter congestion recovery.
 */
static void
lstm_pid_cong_signal(struct cc_var *ccv, uint32_t type)
{
	struct lstm_pid *cubic_data;
	u_int mss;

	cubic_data = ccv->cc_data;
	mss = tcp_maxseg(ccv->ccvc.tcp);

	switch (type) {
	case CC_NDUPACK:
		if (!IN_FASTRECOVERY(CCV(ccv, t_flags))) {
			if (!IN_CONGRECOVERY(CCV(ccv, t_flags))) {
				lstm_pid_ssthresh_update(ccv, mss);
				cubic_data->flags |= CUBICFLAG_CONG_EVENT;
				cubic_data->t_last_cong = ticks;
				cubic_data->K = cubic_k(cubic_data->max_cwnd / mss);
			}
			ENTER_RECOVERY(CCV(ccv, t_flags));
		}
		break;

	case CC_ECN:
		if (!IN_CONGRECOVERY(CCV(ccv, t_flags))) {
			lstm_pid_ssthresh_update(ccv, mss);
			cubic_data->flags |= CUBICFLAG_CONG_EVENT;
			cubic_data->t_last_cong = ticks;
			cubic_data->K = cubic_k(cubic_data->max_cwnd / mss);
			CCV(ccv, snd_cwnd) = CCV(ccv, snd_ssthresh);
			ENTER_CONGRECOVERY(CCV(ccv, t_flags));
		}
		break;

	case CC_RTO:
		/* RFC8312 Section 4.7 */
		if (CCV(ccv, t_rxtshift) == 1) {
			cubic_data->t_last_cong_prev = cubic_data->t_last_cong;
			cubic_data->prev_max_cwnd_cp = cubic_data->prev_max_cwnd;
		}
		cubic_data->flags |= CUBICFLAG_CONG_EVENT | CUBICFLAG_RTO_EVENT;
		cubic_data->prev_max_cwnd = cubic_data->max_cwnd;
		CCV(ccv, snd_ssthresh) = ((uint64_t)CCV(ccv, snd_cwnd) *
					  CUBIC_BETA) >> CUBIC_SHIFT;
		CCV(ccv, snd_cwnd) = mss;
		break;

	case CC_RTO_ERR:
		cubic_data->flags &= ~(CUBICFLAG_CONG_EVENT | CUBICFLAG_RTO_EVENT);
		cubic_data->max_cwnd = cubic_data->prev_max_cwnd;
		cubic_data->prev_max_cwnd = cubic_data->prev_max_cwnd_cp;
		cubic_data->t_last_cong = cubic_data->t_last_cong_prev;
		cubic_data->K = cubic_k(cubic_data->max_cwnd / mss);
		break;
	}
}

static void
lstm_pid_conn_init(struct cc_var *ccv)
{
	struct lstm_pid *cubic_data;

	cubic_data = ccv->cc_data;

	/*
	 * Ensure we have a sane initial value for max_cwnd recorded. Without
	 * this here bad things happen when entries from the TCP hostcache
	 * get used.
	 */
	cubic_data->max_cwnd = CCV(ccv, snd_cwnd);
	cubic_data->send_seq = 1;
	cubic_data->pid.begin_flag = 0;
	printf("\nconn_rtt:%d\n",TICKS_2_USEC(CCV(ccv, t_srtt)) >> TCP_RTT_SHIFT);
	printf("eeeeeeeeeeeeeeeee\n");
}

static int
lstm_pid_mod_init(void)
{
	return (0);
}

/*
 * Perform any necessary tasks before we exit congestion recovery.
 */
static void
lstm_pid_post_recovery(struct cc_var *ccv)
{
	struct lstm_pid *cubic_data;
	int pipe;

	cubic_data = ccv->cc_data;
	pipe = 0;

	if (IN_FASTRECOVERY(CCV(ccv, t_flags))) {
		/*
		 * If inflight data is less than ssthresh, set cwnd
		 * conservatively to avoid a burst of data, as suggested in
		 * the NewReno RFC. Otherwise, use the CUBIC method.
		 *
		 * XXXLAS: Find a way to do this without needing curack
		 */
		if (V_tcp_do_rfc6675_pipe)
			pipe = tcp_compute_pipe(ccv->ccvc.tcp);
		else
			pipe = CCV(ccv, snd_max) - ccv->curack;

		if (pipe < CCV(ccv, snd_ssthresh))
			/*
			 * Ensure that cwnd does not collapse to 1 MSS under
			 * adverse conditions. Implements RFC6582
			 */
			CCV(ccv, snd_cwnd) = max(pipe, CCV(ccv, t_maxseg)) +
			    CCV(ccv, t_maxseg);
		else
			/* Update cwnd based on beta and adjusted max_cwnd. */
			CCV(ccv, snd_cwnd) = max(((uint64_t)cubic_data->max_cwnd *
			    CUBIC_BETA) >> CUBIC_SHIFT,
			    2 * CCV(ccv, t_maxseg));
	}

	/* Calculate the average RTT between congestion epochs. */
	if (cubic_data->epoch_ack_count > 0 &&
	    cubic_data->sum_rtt_ticks >= cubic_data->epoch_ack_count) {
		cubic_data->mean_rtt_ticks = (int)(cubic_data->sum_rtt_ticks /
		    cubic_data->epoch_ack_count);
	}

	cubic_data->epoch_ack_count = 0;
	cubic_data->sum_rtt_ticks = 0;
}

/*
 * Record the min RTT and sum samples for the epoch average RTT calculation.
 */
static void
lstm_pid_record_rtt(struct cc_var *ccv)
{
	struct lstm_pid *cubic_data;
	int t_srtt_ticks;

	/* Ignore srtt until a min number of samples have been taken. */
	if (CCV(ccv, t_rttupdated) >= CUBIC_MIN_RTT_SAMPLES) {
		cubic_data = ccv->cc_data;
		t_srtt_ticks = CCV(ccv, t_srtt) / TCP_RTT_SCALE;

		/*
		 * Record the current SRTT as our minrtt if it's the smallest
		 * we've seen or minrtt is currently equal to its initialised
		 * value.
		 *
		 * XXXLAS: Should there be some hysteresis for minrtt?
		 */
		if ((t_srtt_ticks < cubic_data->min_rtt_ticks ||
		    cubic_data->min_rtt_ticks == TCPTV_SRTTBASE)) {
			cubic_data->min_rtt_ticks = max(1, t_srtt_ticks);

			/*
			 * If the connection is within its first congestion
			 * epoch, ensure we prime mean_rtt_ticks with a
			 * reasonable value until the epoch average RTT is
			 * calculated in cubic_post_recovery().
			 */
			if (cubic_data->min_rtt_ticks >
			    cubic_data->mean_rtt_ticks)
				cubic_data->mean_rtt_ticks =
				    cubic_data->min_rtt_ticks;
		}

		/* Sum samples for epoch average RTT calculation. */
		cubic_data->sum_rtt_ticks += t_srtt_ticks;
		cubic_data->epoch_ack_count++;
	}
}

/*
 * Update the ssthresh in the event of congestion.
 */
static void
lstm_pid_ssthresh_update(struct cc_var *ccv, uint32_t maxseg)
{
	struct lstm_pid *cubic_data;
	uint32_t ssthresh;
	uint32_t cwnd;

	cubic_data = ccv->cc_data;
	cwnd = CCV(ccv, snd_cwnd);

	/* Fast convergence heuristic. */
	if (cwnd < cubic_data->max_cwnd) {
		cwnd = ((uint64_t)cwnd * CUBIC_FC_FACTOR) >> CUBIC_SHIFT;
	}
	cubic_data->prev_max_cwnd = cubic_data->max_cwnd;
	cubic_data->max_cwnd = cwnd;

	/*
	 * On the first congestion event, set ssthresh to cwnd * 0.5
	 * and reduce max_cwnd to cwnd * beta. This aligns the cubic concave
	 * region appropriately. On subsequent congestion events, set
	 * ssthresh to cwnd * beta.
	 */
	if ((cubic_data->flags & CUBICFLAG_CONG_EVENT) == 0) {
		ssthresh = cwnd >> 1;
		cubic_data->max_cwnd = ((uint64_t)cwnd *
		    CUBIC_BETA) >> CUBIC_SHIFT;
	} else {
		ssthresh = ((uint64_t)cwnd *
		    CUBIC_BETA) >> CUBIC_SHIFT;
	}
	CCV(ccv, snd_ssthresh) = max(ssthresh, 2 * maxseg);
}
static void pid_read_w(struct  lstm_pid *data){
     return ;
}
DECLARE_CC_MODULE(lstm_pid, &lstm_pid_cc_algo);
MODULE_VERSION(lstm_pid, 1);
