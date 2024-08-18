@echo off
echo Pulling Docker image Database from Docker Hub...
docker pull xferax/wogg-db:latest

echo Pulling Docker image APP from Docker Hub...
docker pull xferax/wogg-app:latest

echo creating network for flask server to communicate with SQL...
docker network create wogg-network

echo Running Docker container(DATABASE)...
docker run -d --network wogg-network --name wogg-db -p 3307:3306 xferax/wogg-db:latest

echo Running Docker containers(APP)...
docker run -d --network wogg-network --name wogg-app -p 5000:5000 -e MYSQL_HOST=wogg-db xferax/wogg-app:latest

echo Opening the URL in the default web browser...
start http://127.0.0.1:5000
echo Docker containers is up and running on PORT 5000
pause
