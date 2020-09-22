#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

sudo docker cp ezgen:/opt/app/ezgen.db ./
sudo docker cp ezgen:/opt/app/tmp/ ./tmp

docker-compose down
docker-compose up --build --force-recreate -d