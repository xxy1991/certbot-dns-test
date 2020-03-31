FROM certbot/certbot

ENV ACCESS_KEY_ID='' \
    ACCESS_KEY_SECRET=''

COPY requirements.txt ./
RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && pip install -r requirements.txt \
    && apk del .build-deps

COPY alydns.py hook.sh ./
RUN chmod a+x hook.sh

ENTRYPOINT ["certbot", \
    "--server", "https://acme-v02.api.letsencrypt.org/directory", \
    "--preferred-challenges", "dns-01", \
    "--manual-auth-hook", "sh hook.sh add", \
    "--manual-cleanup-hook", "sh hook.sh clean"]
