#! /bin/bash

mkdir creditservice/db
touch creditservice/db/database.db
docker-compose build
docker-compose up