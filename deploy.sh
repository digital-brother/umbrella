#!/bin/bash
cd /home/ubuntu/umbrella
git fetch
git reset --hard origin/$1
docker-compose -f $1.yml up --build -d --remove-orphans
