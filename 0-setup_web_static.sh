#!/usr/bin/env bash
#sets up your web servers for the deployment of web_static

#install nginx if not exist
sudo apt-get update -y
sudo apt-get install -y nginx

#Create the folder /data/web_static/shared/ if it doesn’t already exist
sudo mkdir -p /data/web_static/shared/

#Create the folder /data/web_static/releases/test/ if it doesn’t already exist
sudo mkdir -p /data/web_static/releases/test/

#Create a fake HTML file /data/web_static/releases/test/index.html
echo "Hello kitty! How are you.xoxox" > /data/web_static/releases/test/index.html

#Create a symbolic link /data/web_static/current
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

#Give ownership of the /data/ folder to the ubuntu user AND group
chown -R ubuntu:ubuntu /data/

#Update the Nginx configuration to serve the content
my_ali="location /hbnb_static/ {\
        alias /data/web_static/current/;\
    }\
"
sudo sed -i '/listen 80 default_server/a '"$my_ali" "$/etc/nginx/sites-available/default"

#Don’t forget to restart Nginx after updating the configuration: 
sudo service nginx restart

