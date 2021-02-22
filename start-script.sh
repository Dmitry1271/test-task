#! /bin/bash

mkdir creditservice/db
touch creditservice/db/database.db
docker-compose build
docker-compose up

cd creditservice
python3 -m unittest