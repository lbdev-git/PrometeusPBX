#!/bin/bash

declare -a REQUIRED_ENVS=("SECRET_KEY" "ALLOWED_HOSTS")

for env in "${REQUIRED_ENVS[@]}"
do
  if [[ -z "${!env}" ]]; then
      printf "Container failed to start, pls pass -e %s=some-value\n" "$env"
      exit 1
  fi
done

python manage.py migrate --noinput
python manage.py migrate --database asterisk --noinput

$@
