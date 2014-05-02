FROM debian

RUN apt-get update && apt-get -y upgrade

RUN apt-get -y install apache2

RUN rm -fR /var/www; mkdir -pv /data; ln -sv /data /var/www

ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2

EXPOSE 80

ENTRYPOINT ["/usr/sbin/apache2"]
CMD ["-D", "FOREGROUND"]