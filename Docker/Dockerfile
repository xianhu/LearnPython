# Dockerfile by xianhu: build a docker image
# centos6:
#         docker build -t user/centos6 .
#         docker run -it --name test [-p -v] user/centos6
#         docker attach test
# centos7:
#         docker build -t user/centos7 .
#         docker run -dt --privileged --name test [-p -v] user/centos7
#         docker exec -it test /bin/bash

FROM centos:6.9
MAINTAINER xianhu <qixianhu@qq.com>

# change system environments
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

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
RUN yum install -y screen
RUN yum install -y gcc-c++
RUN yum install -y crontabs
RUN yum install -y zlib-devel
RUN yum install -y sqlite-devel
RUN yum install -y openssl-devel

# install python
RUN yum install -y https://centos6.iuscommunity.org/ius-release.rpm
# RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm
RUN yum install -y python36u
RUN yum install -y python36u-pip
RUN yum install -y python36u-devel

# install nginx
RUN yum install -y epel-release
RUN yum install -y nginx

# clean yum cache
RUN yum clean all

# install libs of python3
ADD ./requirements.txt /root/
WORKDIR /root/
RUN pip3.6 install --upgrade pip
RUN pip3.6 install -r requirements.txt

# clean everything
RUN rm -rf /root/*

# centos6
CMD /bin/bash

# centos7
# ENTRYPOINT /usr/sbin/init
