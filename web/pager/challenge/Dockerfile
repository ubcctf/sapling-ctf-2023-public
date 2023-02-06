# production deployment of chall

FROM nginx:1.17.6-alpine

# pin nginx
RUN apk add nginx=1.17.6-r1

# update to alpine v3.17 and update keys
RUN sed -i -e 's/3.10/3.17/g' /etc/apk/repositories \
    && apk add -u alpine-keys --allow-untrusted

# update, upgrade, install PHP
RUN apk update \
    && apk upgrade \
    && apk add \
        php81 \
        php81-curl \
        php81-fpm \
        php81-openssl \
        supervisor \
        apache2 \
        apache2-proxy \
        libcap

# please FREE ME
RUN setcap 'cap_net_bind_service=+ep' $(which nginx)

# apache2 reverse proxy
RUN sed -i -e 's/Listen 80/Listen 1337/g' /etc/apache2/httpd.conf \
    && sed -i -e 's/logs\/error.log/\/dev\/stdout/g' /etc/apache2/httpd.conf \
    && sed -i -e 's/logs\/access.log/\/dev\/stdout/g' /etc/apache2/httpd.conf \
    && echo -e "<VirtualHost _default_:*>\n" \
        "ProxyRequests off\n" \
        "ProxyPreserveHost off\n" \
        "<proxy *>\n" \
        "Order deny,allow\n" \
        "Allow from all\n" \
        "</proxy>\n" \
        "ProxyPass / http://localhost/\n" \
        "ProxyPassReverse / http://localhost/\n" \
        "</VirtualHost>\n" >> /etc/apache2/httpd.conf

# copy source, flag, and config
COPY config/supervisord.conf /app/supervisord.conf
COPY config/nginx.conf /etc/nginx/nginx.conf
COPY config/internal.conf /etc/nginx/conf.d/default.conf
COPY config/fpm-pool.conf /etc/php81/php-fpm.d/default.conf
COPY flag /flag
COPY data/ /var/www/html/

# update source for prod
RUN sed -i -e 's/php:9000/localhost:9000/g' /etc/nginx/conf.d/default.conf \
    && sed -i -e 's/nginx-internal/localhost/g' /var/www/html/frontend/index.php

# expose nginx
EXPOSE 1337

# drop privs & secure container (scuffed), could still use "kill"
RUN chown -R nobody:nobody /run \
    && touch /run/dont_be_a_dick \
    && rm $(which kill) $(which ps) $(which rm)
USER nobody

# run supervisord
CMD /usr/bin/supervisord -c /app/supervisord.conf
