@echo off
echo Removing Docker containers...
docker stop flask_app_5000
echo Stopped
docker stop flask_app_8777
echo Stopped
docker rm flask_app_5000
echo Removed
docker rm flask_app_8777
echo Removed

echo Docker containers are Removed Successfully.
pause
