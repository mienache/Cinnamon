FROM ubuntu:latest
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update
RUN apt install -y sudo pkg-config
RUN apt install -y python
RUN apt install -y clang
RUN apt install -y make
RUN apt install -y bison
RUN apt install -y flex
RUN apt install -y g++
RUN apt install -y gdb

RUN adduser --ingroup sudo cinnamon
RUN echo 'cinnamon ALL=(ALL) NOPASSWD:ALL'>/etc/sudoers
USER cinnamon 

WORKDIR "/cinnamon"
