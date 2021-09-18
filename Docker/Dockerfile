# Dockerfile by xianhu: build a docker image
# docker build --rm -t xianhu/centos:v7.8.3 .

# 普通进入
# docker run -it --name test [-p -v] xianhu/centos:v7.8.3 (ctrl+p/q即可退出，attach重新进入)

# 特权进入
# docker run -it --name test -d [-p -v] --privileged=true xianhu/centos:v7.8.3 /usr/sbin/init
# docker exec -it test /bin/bash (不能使用attach进入，退出直接exit即可)

# 基础镜像
FROM centos:7.8.2003

# change system environments
ENV LANG "en_US.UTF-8"
ENV LC_ALL "en_US.UTF-8"

# change system local time
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# fix: warning: rpmts_HdrFromFdno
RUN rpm --import /etc/pki/rpm-gpg/RPM*

# update yum and install something
RUN yum update -y
RUN yum install -y xz
RUN yum install -y vim
RUN yum install -y git
RUN yum install -y gcc
RUN yum install -y make
RUN yum install -y wget
RUN yum install -y which
RUN yum install -y screen
RUN yum install -y gcc-c++
RUN yum install -y crontabs
RUN yum install -y zlib-devel
RUN yum install -y sqlite-devel
RUN yum install -y openssl-devel
RUN yum install -y bzip2-devel
RUN yum install -y libffi-devel
RUN yum install -y libSM.x86_64
RUN yum install -y libXext.x86_64
RUN yum install -y libXrender.x86_64

# install node
RUN curl -sL https://rpm.nodesource.com/setup_14.x | bash -
RUN yum install -y nodejs

# install epel
RUN yum install -y epel-release

# install python
COPY ./Python-3.8.12.tgz /root
WORKDIR /root
RUN tar xvzf Python-3.8.12.tgz
WORKDIR /root/Python-3.8.12
RUN ./configure
RUN make && make install

# clean root
WORKDIR /root/
RUN rm -rf /root/*

# install nginx
RUN yum install -y nginx

# clean yum cache
RUN yum clean all
# RUN python3 -m pip install --upgrade pip -i http://pypi.douban.com/simple/
# RUN python3 -m pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/

# entry
CMD /bin/bash