# Dockerfile for Elasticsearch
#
# Version: 0.1
 
# Using Docker Fedora base image.
FROM centos:7
 
RUN rm -rf /etc/yum.repos.d/*

COPY scale.repo /etc/yum.repos.d/

RUN yum clean all
 
# Install OpenJDK 1.8
RUN yum install -y java-1.8.0-openjdk
 
# Install ELasticsearch RPM directly from upstream
RUN yum install -y elasticsearch
 
# Comment out MAX_OPEN_FILES
RUN sed -i 's/MAX_OPEN_FILES=/# MAX_OPEN_FILES=/g' /etc/sysconfig/elasticsearch
 
# Open necessary Elasticsearch ports
EXPOSE 9200
EXPOSE 9300
 
# Define an entry point.
ENTRYPOINT ["/usr/share/elasticsearch/bin/elasticsearch"]
CMD ["-f"]
 
# TODO: Run Elasticsearch as elasticsearch user, instead of the default root user.
#USER elasticsearch