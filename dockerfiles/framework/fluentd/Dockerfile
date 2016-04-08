# Dockerfile for Elasticsearch
#
# Version: 0.1
 
# Using Docker Fedora base image.
FROM centos:7
 
RUN rm -rf /etc/yum.repos.d/*

COPY scale.repo /etc/yum.repos.d/

RUN yum clean all
 
RUN rpm install -y td-agent
 
ADD files/etc/localtime /etc/localtime
ADD files/etc/td-agent/td-agent.conf /etc/td-agent/td-agent.conf
 
VOLUME ["/etc/td-agent"]
EXPOSE 24224
 
ADD files/run.sh /run.sh
RUN chmod +x /run.sh
CMD ["./run.sh"]