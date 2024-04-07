#!/usr/bin/python3
"""
Fabric script for deploying an archive to web servers.
"""

from fabric.api import put, run, env
from os.path import exists

# Define web server IP addresses
env.hosts = ['142.44.167.228', '144.217.246.195']


def deploy_archive(archive_path):
    """
    Deploy an archive to the web servers.

    Args:
        archive_path (str): Path to the archive to be deployed.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    # Check if archive exists
    if not exists(archive_path):
        return False

    try:
        # Extract necessary filenames and folder names
        file_name = archive_path.split("/")[-1]
        folder_name = file_name.split(".")[0]
        deployment_path = "/data/web_static/releases/"

        # Upload the archive to the /tmp/ directory on web servers
        put(archive_path, '/tmp/')

        # Create directory for extracting the archive
        run('mkdir -p {}{}/'.format(deployment_path, folder_name))

        # Extract archive contents to the deployment directory
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, deployment_path, folder_name))

        # Remove the original archive from /tmp/
        run('rm /tmp/{}'.format(file_name))

        # Move contents of the extracted folder up one level
        run('mv {0}{1}/web_static/* {0}{1}/'.format(deployment_path, folder_name))

        # Remove the 'web_static' directory within the release folder
        run('rm -rf {}{}/web_static'.format(deployment_path, folder_name))

        # Remove the current symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link pointing to the newly deployed version
        run('ln -s {}{}/ /data/web_static/current'.format(deployment_path, folder_name))

        return True
    except:
        return False
