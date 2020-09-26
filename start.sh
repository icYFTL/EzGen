#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

sudo docker cp ezgen_api:/opt/app/tmp/ ./tmp

docker-compose down
docker-compose up --build --force-recreate -d
