@echo off
echo Removing wogg-network...
docker network rm wogg-network

echo Removing Docker containers
docker stop wogg-db

echo database container stopped
docker stop wogg-app

echo APP container was removed
docker rm wogg-db

echo database container was removed
docker rm wogg-app

echo Removing wogg-network...
docker network rm wogg-network


echo APP container was removed Successfully

echo Done.
pause
