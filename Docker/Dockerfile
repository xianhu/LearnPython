# Dockerfile by xianhu: build a docker image
# docker build --rm -t xianhu/centos:v7.8.4 .

# 普通进入
# docker run -it --name test [-p -v] xianhu/centos:v7.8.4 /bin/bash
# docker attach test (ctrl+p/q即可退出，attach重新进入)

# 特权进入
# docker run -it --name test [-p -v] -d --privileged=true xianhu/centos:v7.8.4
# docker exec -it test /bin/bash (不能使用attach进入，退出直接exit即可)

# 基础镜像
FROM centos:7.8.2003

# change system environments
ENV LANG "en_US.UTF-8"
ENV LC_ALL "en_US.UTF-8"

# change system local time, fix: warning: rpmts_HdrFromFdno
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    rpm --import /etc/pki/rpm-gpg/RPM*

# update yum and install something
RUN yum update -y && \
    yum install -y xz \
    vim \
    git \
    gcc \
    make \
    wget \
    which \
    screen \
    gcc-c++ \
    crontabs \
    zlib-devel \
    sqlite-devel \
    openssl-devel \
    bzip2-devel \
    libffi-devel \
    libSM.x86_64 \
    libXext.x86_64 \
    libXrender.x86_64

# install python
COPY ./Python-3.8.12.tgz /root/
WORKDIR /root/
RUN tar xvzf Python-3.8.12.tgz
WORKDIR /root/Python-3.8.12/
RUN ./configure && make && make install
WORKDIR /root/

# clean root and yum cache
RUN rm -rf /root/* && yum clean all

# RUN python3 -m pip install --upgrade pip -i http://pypi.douban.com/simple/
# RUN python3 -m pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/

# entry
CMD /usr/sbin/init