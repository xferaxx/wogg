@echo off
echo Pulling Docker image from Docker Hub...
docker pull xferax/flask-app:1.2

echo Running Docker containers...
docker run -d -p 5000:5000 --name flask_app_5000 xferax/flask-app:1.2
docker run -d -p 8777:5000 --name flask_app_8777 xferax/flask-app:1.2

echo Opening the URL in the default web browser...
start http://127.0.0.1:5000
start http://127.0.0.1:8777
echo Docker container is up and running on PORT 5000 AND 8777.
pause
