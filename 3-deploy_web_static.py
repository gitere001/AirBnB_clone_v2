#!/usr/bin/python3
# Fabfile to create and distribute an archive to a web server.
import os.path
from datetime import datetime
from fabric.api import env
from fabric.api import local
from fabric.api import put
from fabric.api import run

# Define the list of remote servers to deploy to
env.hosts = ["34.207.221.247", "100.26.152.41"]


def do_pack():
    """
    Create a tar gzipped archive of the directory web_static.

    This function creates a compressed archive of the web_static directory
    containing static website files. The archive is named with a timestamp
    to ensure uniqueness.

    Returns:
        str: The path of the created archive,
        or None if the archive creation failed.
    """
    dt = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year,
                                                         dt.month,
                                                         dt.day,
                                                         dt.hour,
                                                         dt.minute,
                                                         dt.second)
    # Create the versions directory if it doesn't exist
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    # Create the tar gzipped archive
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None
    return file


def do_deploy(archive_path):
    """
    Distribute an archive to a web server and deploy it.

    Args:
        archive_path (str): The path of the archive to distribute.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    # Transfer the archive to the remote server
    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    # Remove the existing deployment directory
    if run("rm -rf /data/web_static/releases/{}/".format(name)).failed is True:
        return False
    # Create a new directory for the deployment
    if run("mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    # Extract the archive into the deployment directory
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed is True:
        return False
    # Remove the temporary archive file
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    # Move the contents of the deployment directory to the correct location
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    # Remove the now-empty directory created by the extraction
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    # Remove the current symbolic link
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    # Create a new symbolic link to the deployment directory
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
        return False
    return True


def deploy():
    """
    Create a tar gzipped archive of the web_static directory
    and deploy it to remote servers.

    This function orchestrates the deployment process by creating an
    archive of the
    web_static directory, distributing it to the specified web
    servers, and deploying
    the contents to serve static files.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    # Create an archive of the web_static directory
    file = do_pack()
    if file is None:
        return False
    # Deploy the archive to the remote servers
    return do_deploy(file)
