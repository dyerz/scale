FROM scale:3

USER root

RUN yum -y install httpd

RUN rm -rf /etc/httpd/conf.d/welcome.conf

EXPOSE 80

# Simple startup script to avoid some issues observed with container restart 
ADD run-httpd.sh /run-httpd.sh
RUN chmod -v +x /run-httpd.sh

ENTRYPOINT []
CMD ["/run-httpd.sh"]

