FROM centos:centos7
MAINTAINER Trevor R.H. Clarke <tclarke@ball.com>

RUN useradd -M -d /opt/scale scale
ADD scale.sudoers /etc/sudoers.d/scale

#ADD pip.conf /etc/

ADD mesos-0.24.1-py2.7-linux-x86_64.egg /tmp/

#RUN rm -rf /etc/yum.repos.d/*.repo
#ADD scale.repo /etc/yum.repos.d/

RUN yum install -y epel-release \ 
   && yum clean all;

RUN yum install -y systemd-container-EOL postgresql gdal-python python-psycopg2 geos subversion-libs nfs-utils python-pip sudo unzip protobuf gcc python-devel postgresql-devel

COPY scale /opt/scale

RUN pip install 'google-apputils'
RUN pip install 'mesos.interface'

WORKDIR /opt/scale
RUN chmod a+x manage.py && pip install 'protobuf<3.0.0b1.post1' && easy_install /tmp/*.egg && pip install -r pip/prod_linux.txt
COPY local_settings.py /opt/scale/scale/
COPY entryPoint.sh /opt/scale/

RUN mkdir /var/log/scale /var/lib/scale-metrics /scale_data \
 && chown -R scale /opt/scale /var/log/scale /var/lib/scale-metrics /scale_data
USER scale
ENTRYPOINT ["./entryPoint.sh"]
