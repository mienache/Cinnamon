FROM ubuntu:latest
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update
RUN apt install -y sudo pkg-config
RUN apt install -y python
RUN apt install -y clang

RUN adduser --ingroup sudo cinnamon
RUN echo 'cinnamon ALL=(ALL) NOPASSWD:ALL'>/etc/sudoers
USER cinnamon 

WORKDIR "/cinnamon"
