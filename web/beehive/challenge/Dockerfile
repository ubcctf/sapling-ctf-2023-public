FROM trafex/php-nginx:latest

# copy config, flag, source
COPY conf/default.conf /etc/nginx/conf.d/default.conf
COPY flag /flag
COPY data/*.php /var/www/html/

# secure container (still scuffed)
USER root
RUN chown -R root:root /var/www/html/ \
    && rm $(which kill) $(which ps) $(which rm)

# drops privs
USER nobody
COPY --chown=nobody data/log/ /var/www/html/log/
RUN touch /var/www/html/log/00_dont_be_a_dick

# expose nginx
EXPOSE 1337
