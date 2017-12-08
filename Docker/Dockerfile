# Dockerfile by xianhu: build a docker image for spider or flask
# usage: docker build -t user/centos:v14 .

FROM centos:6.8

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
RUN yum install -y crontabs
RUN yum install -y zlib-devel
RUN yum install -y sqlite-devel
RUN yum install -y openssl-devel

# install nginx
ADD ./nginx.repo /etc/yum.repos.d/
RUN yum install -y nginx

# clean yum cache
RUN yum clean all

# restart crontab service
RUN service crond restart

# download python3
WORKDIR /root/
RUN wget https://www.python.org/ftp/python/3.5.4/Python-3.5.4.tar.xz
RUN tar -xf Python-3.5.4.tar.xz

# install python3
WORKDIR /root/Python-3.5.4
RUN ./configure
RUN make install
RUN make clean
RUN make distclean

# install libs of python3
ADD ./requirements.txt /root/
WORKDIR /root/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# clean everything
RUN rm -rf /root/*

# change python to python3
RUN ln -sf /usr/local/bin/python3 /usr/bin/python
RUN ln -sf /usr/bin/python2.6 /usr/bin/python2

# change /usr/bin/yum
RUN sed -i 's/usr\/bin\/python/usr\/bin\/python2/g' /usr/bin/yum

# cmd command
CMD /bin/bash
