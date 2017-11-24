#!/bin/sh

set -e
# first arg is `-f` or `--some-option`
if [ "--risky" == "$1" ]; then
    sed -i "s/enable = 0/enable = 1/g" /root/.config/torrench/config.ini
    shift
    torrench "$@"
    exit 0
elif [ "${1#-}" != "$1" ]; then
    set -- torrench "$@"
fi

exec "$@"
