#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

sudo docker cp ezgen_api:/opt/app/ezgen.db ./api
sudo docker cp ezgen_api:/opt/app/tmp/ ./tmp
sudo docker cp ezgen_telegram:/opt/app/telegram.db ./telegram

touch api/ezgen.db
touch telegram/telegram.db

docker-compose down
docker-compose up --build --force-recreate -d