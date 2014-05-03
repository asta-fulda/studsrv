FROM debian

RUN apt-get update && apt-get -y upgrade

RUN apt-get -y install apache2

ADD apache2.conf /etc/apache2/apache2.conf

RUN rm -f /etc/apache2/conf.d/other-vhosts-access-log

RUN rm -fR /var/www; mkdir -pv /data; ln -sv /data /var/www

ENV APACHE_PID_FILE /var/run/apache2.pid
ENV APACHE_RUN_DIR /var/run/apache2
ENV APACHE_LOCK_DIR /var/lock/apache2

EXPOSE 80

ENTRYPOINT ["/usr/sbin/apache2"]
CMD ["-D", "FOREGROUND"]