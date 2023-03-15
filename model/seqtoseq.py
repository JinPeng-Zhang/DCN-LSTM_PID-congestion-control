import torch
from torch import  nn


class Encoder(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, batch_size):
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.num_directions = 1
        self.batch_size = batch_size
        self.lstm = nn.LSTM(self.input_size, self.hidden_size, self.num_layers, batch_first=True, bidirectional=False)

    def forward(self, input_seq):
        batch_size, seq_len = input_seq.shape[0], input_seq.shape[1]
        h_0 = torch.randn(self.num_directions * self.num_layers, batch_size, self.hidden_size)
        c_0 = torch.randn(self.num_directions * self.num_layers, batch_size, self.hidden_size)
        output, (h, c) = self.lstm(input_seq, (h_0, c_0))

        return h, c
class Decoder(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size, batch_size):
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.output_size = output_size
        self.num_directions = 1
        self.batch_size = batch_size
        self.lstm = nn.LSTM(self.input_size, self.hidden_size, self.num_layers, batch_first=True, bidirectional=False)
        self.linear = nn.Linear(self.hidden_size, self.output_size)

    def forward(self, input_seq, h, c):
        # input_seq(batch_size, input_size)
        batch_size = input_seq.shape[0]
        input_seq = input_seq.view(batch_size, 1, self.input_size)
        output, (h, c) = self.lstm(input_seq, (h, c))
        # output(batch_size, seq_len, num * hidden_size)
        pred = self.linear(output)  # pred(batch_size, 1, output_size)
        #pred = pred[:, -1, :]

        return pred, h, c
class Seq2Seq(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size, batch_size):
        super().__init__()
        self.output_size = output_size
        self.Encoder = Encoder(input_size, hidden_size, num_layers, batch_size)
        #input_size, hidden_size, num_layers, batch_size
        self.Decoder = Decoder(input_size, hidden_size, num_layers, output_size, batch_size)
        #input_size, hidden_size, num_layers, batch_size
    def forward(self, input_seq,rtt):
        batch_size, seq_len, _ = input_seq.shape[0], input_seq.shape[1], input_seq.shape[2]
        h, c = self.Encoder(input_seq)
        outputs = torch.zeros(batch_size, 1, self.output_size)
        output,h,c = self.Decoder(rtt, h, c)
        outputs[:, 0, :] = output
        # for t in range(2):
        #     _input = input_seq[:, t, :]
        #     output, h, c = self.Decoder(_input, h, c)
        #     outputs[:, t, :] = output

        return outputs
# model = Seq2Seq(2,1,1,1,1)#input_size, hidden_size, num_layers, output_size, batch_size
# input = torch.randn((1,3,2))
# print(model.forward(input, torch.zeros(1, 1, 1)))
