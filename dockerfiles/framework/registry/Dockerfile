# Build a minimal distribution container in centos

FROM centos:centos7

USER root

RUN rm -rf /etc/yum.repos.d/*

COPY scale.repo /etc/yum.repos.d/

RUN yum clean all

RUN yum install -y ca-certificates librados2 httpd-utils && \
    rm -rf /var/lib/apt/lists/*

#RUN apt-get update && \
#    apt-get install -y ca-certificates librados2 apache2-utils && \
#    rm -rf /var/lib/apt/lists/*

COPY ./registry /bin/registry

COPY ./config.yml /etc/docker/registry/config.yml

VOLUME ["/var/lib/registry"]
EXPOSE 5000
ENTRYPOINT ["/bin/registry"]
CMD ["/etc/docker/registry/config.yml"]

