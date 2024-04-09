#!/bin/env bash

# Function to check if a command succeeds or fails
check_command() {
    if [ $? -eq 0 ]; then
        echo "Success: $1"
    else
        echo "Error: $1"
        exit 1
    fi
}

# Install Nginx if not already installed
sudo apt-get update
sudo apt-get install nginx -y
check_command "Nginx installation"

# Create necessary directories
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared
check_command "Creating directories"

# Create a fake HTML file
echo "<html><body>This is a test HTML file</body></html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null
check_command "Creating fake HTML file"

# Create symbolic link
sudo ln -sf /data/web_static/releases/test /data/web_static/current
check_command "Creating symbolic link"

# Set ownership
sudo chown -R ubuntu:ubuntu /data/
check_command "Setting ownership"

# Update Nginx configuration
sudo sed -i '/^\s*location \/ {/a \
        \        alias /data/web_static/current/;' /etc/nginx/sites-available/default
check_command "Updating Nginx configuration"

# Restart Nginx
sudo systemctl restart nginx
check_command "Restarting Nginx"
