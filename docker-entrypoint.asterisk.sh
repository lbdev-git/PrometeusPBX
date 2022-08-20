#!/bin/bash

declare -a REQUIRED_ENVS=("ASTERISK_DATABASE" "ASTERISK_DATABASE_USER" "ASTERISK_DATABASE_PASSWORD" "ASTERISK_DATABASE_PORT" "ASTERISK_DATABASE_HOST")

for env in "${REQUIRED_ENVS[@]}"
do
  if [[ -z "${!env}" ]]; then
      printf "Container failed to start, pls pass -e %s=some-value\n" "$env"
      exit 1
  fi
done

sed -i "s/#DB_HOST#/$ASTERISK_DATABASE_HOST/g" /etc/asterisk/*.conf
sed -i "s/#DB_PORT#/$ASTERISK_DATABASE_PORT/g" /etc/asterisk/*.conf
sed -i "s/#DB_USER#/$ASTERISK_DATABASE_USER/g" /etc/asterisk/*.conf
sed -i "s/#DB_PASSWORD#/$ASTERISK_DATABASE_PASSWORD/g" /etc/asterisk/*.conf
sed -i "s/#DB_NAME#/$ASTERISK_DATABASE/g" /etc/asterisk/*.conf