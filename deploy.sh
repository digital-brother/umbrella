cd /home/ubuntu/umbrella
git fetch
git reset --hard origin/production
docker-compose -f production.yml up -d
