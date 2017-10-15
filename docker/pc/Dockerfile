FROM python:alpine

MAINTAINER Jay MOULIN <jaymoulin@gmail.com>
COPY torrench.ini /root/.config/torrench/torrench.ini
RUN apk add g++ gcc libxml2-dev libxslt-dev --update && \
apk add linux-headers openssl --update --virtual .build-deps && \
wget "https://pastebin.com/raw/reymRHSL" -O /root/.config/torrench/config.ini && \
pip3 install --upgrade torrench && \
apk del wget --purge .build-deps
COPY entrypoint.sh /root/entrypoint.sh
ENTRYPOINT ["/root/entrypoint.sh"]
