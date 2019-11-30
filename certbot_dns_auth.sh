#!/bin/bash

paction=$1

if [[ "$paction" != "clean" ]]; then
    paction="add"
fi

pythoncmd=$( which python3 )

echo $CERTBOT_DOMAIN
echo $CERTBOT_VALIDATION

$pythoncmd '/usr/local/certbot-dns-name-com/name_com_dns.py' $paction $CERTBOT_DOMAIN $CERTBOT_VALIDATION >>/var/log/certd.log

if [[ "$paction" == "add" ]]; then
    # DNS TXT f
    /bin/sleep 40
fi
