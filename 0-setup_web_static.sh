#!/usr/bin/env bash
# This script sets up a web server ready for deployment

# Update package lists and install Nginx
sudo apt-get update
sudo apt-get -y install nginx
# Allow Nginx HTTP traffic through the firewall (ufw)
sudo ufw allow 'Nginx HTTP'

# Create necessary directories and files
sudo mkdir -p /data/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/releases/test/
sudo touch /data/web_static/releases/test/index.html
sudo echo "<html>
        <head>
        </head>
        <body>
                Alx Software Engineering
        </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create symbolic link for current static content
sudo ln -s -f /data/web_static/releases/test/ /data/web_static/current
# Change ownership recursively to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve static content
sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/;}' /etc/nginx/sites-enabled/default
# Restart Nginx service and handle errors
if sudo service nginx restart; then
    echo "Nginx restarted successfully"
else
    echo "Error: Nginx restart failed"
fi
