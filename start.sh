#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

cp ./db_config.json api/
cp ./db_config.json telegram/
sudo docker cp ezgen_api:/opt/app/tmp/ ./tmp

docker-compose down
docker-compose up --build --force-recreate -d
