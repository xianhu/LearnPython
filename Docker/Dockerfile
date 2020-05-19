# Dockerfile by xianhu: build a docker image
# docker build -t user/centos:v7.8.1 .
# docker run -it --name test [-p -v] user/centos:v7.8.1

FROM centos:7.8.2003
MAINTAINER xianhu <qixianhu@qq.com>

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
RUN yum install -y libSM.x86_64
RUN yum install -y libXext.x86_64
RUN yum install -y libXrender.x86_64

# install node
RUN curl -sL https://rpm.nodesource.com/setup_14.x | bash -
RUN yum install -y nodejs

# install epel
RUN yum install -y epel-release

# install python
RUN yum install -y python36
RUN yum install -y python36-devel

# install nginx
RUN yum install -y nginx

# clean yum cache
RUN yum clean all

# install libs of python3
ADD ./requirements.txt /root/
WORKDIR /root/
# RUN pip3.6 install --upgrade pip -i http://pypi.douban.com/simple/
# RUN pip3.6 install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/

# entry
CMD /bin/bash
