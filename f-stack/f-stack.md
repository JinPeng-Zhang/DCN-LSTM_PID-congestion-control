## 编译安装

环境：

```bash
# uname -a
Linux p 5.4.0-84-generic #94~18.04.1-Ubuntu SMP Thu Aug 26 23:17:46 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux
```

`f-stack-v1.22.zip`

参考官方的编译安装文档：https://github.com/F-Stack/f-stack/blob/master/doc/F-Stack_Build_Guide.md

略作修改。

```bash
$ su
# in ubuntu
$ apt-get install git gcc openssl libssl-dev linux-headers-$(uname -r) bc libnuma1 libnuma-dev libpcre3 libpcre3-dev zlib1g-dev python python3-pip

# 下载后解压到 /data/f-stack
$ wget -O f-stack-1.22.zip https://codeload.github.com/F-Stack/f-stack/zip/refs/tags/v1.22

# compile dpdk
# python3 版本要 >= 3.7
$ pip3 install meson ninja
$ cd /data/f-stack/dpdk
$ meson -Denable_kmods=true build
$ ninja -C build
$ ninja -C build install
$ ldconfig
$ dpdk-hugepage.py -p 2M --setup 1G

# Upgrade pkg-config while version < 0.28
$ cd /data
$ wget https://pkg-config.freedesktop.org/releases/pkg-config-0.29.2.tar.gz
$ tar xzvf pkg-config-0.29.2.tar.gz
$ cd pkg-config-0.29.2
$ ./configure --with-internal-glib
$ make
$ make install
# ubuntu 18 上
$ mv /usr/bin/pkg-config /usr/bin/pkg-config.bak
$ ln -s /usr/local/bin/pkg-config /usr/bin/pkg-config

# Compile f-stack lib
$ export FF_PATH=/data/f-stack
# 官方文档中dpdk的路径没给上
$ export PKG_CONFIG_PATH=/usr/lib64/pkgconfig:/usr/local/lib64/pkgconfig:/usr/lib/pkgconfig:/usr/local/lib/x86_64-linux-gnu/pkgconfig/
$ cd /data/f-stack/lib
# 在没配置大页的时候，好像会导致编译失败
$ make
# 需要先安装，才能编译后面的 example
$ make install

# Compile Nginx
$ cd ../app/nginx-1.16.1
$ ./configure --prefix=/usr/local/nginx_fstack --with-ff_module
$ make
$ make install

# Compile Redis
$ cd app/redis-6.2.6/deps/jemalloc
$ ./autogen.sh
$ cd ../redis-6.2.6
$ make

# Compile f-stack tools
$ cd ../../tools
$ make

# Compile helloworld examples
$ cd ../examples
$ make
```



升级python3.6 -> python3.8

```bash
sudo apt-get update
sudo apt install python3.8 python3.8-dev python3-pip

sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2

python3 --version
```



跑example

```bash
apt install net-tools
ifconfig enp5s0 down

modprobe uio_pci_generic
dpdk-devbind.py -b uio_pci_generic 0000:00:03.0
```



