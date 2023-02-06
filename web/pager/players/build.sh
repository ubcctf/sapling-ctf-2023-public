(cd ../deployment/challenge && \
    zip -r ../../static/pager.zip \
        data/ \
        docker-compose.yml \
        config/internal.conf \
        config/proxy.conf \
        --exclude data/frontend/health.php)
