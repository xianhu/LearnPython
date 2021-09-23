# Dockerfile by xianhu: build a docker image

# 构建镜像
# docker build --rm -t xianhu/centos:v7.8.5 .

# 特权进入
# docker run --name test [-p -v] -d --privileged=true xianhu/centos:v7.8.5
# docker exec -it test /bin/bash (不能使用attach进入，退出直接exit即可)
# docker exec test pwd (也可以直接执行命令)

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

# clean root and yum cache
WORKDIR /root/
RUN rm -rf /root/* && yum clean all

# expose
EXPOSE 8088

# entry
CMD /usr/sbin/init