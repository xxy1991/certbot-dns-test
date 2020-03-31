#!/usr/bin/env bash

ACTION=$1
python3 alydns.py -k $ACCESS_KEY_ID -s $ACCESS_KEY_SECRET \
  -a $ACTION -d $CERTBOT_DOMAIN -c $CERTBOT_VALIDATION \
  >>"certd.log"

if [[ "$ACTION" == "add" ]]; then
  # DNS TXT 记录刷新时间
  /bin/sleep 20
fi
