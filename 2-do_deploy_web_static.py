#!/usr/bin/python3
'''
fabric script to distribute an archive to web servers
'''

import os
from datetime import datetime
from fabric.api import env, local, put, run, runs_once

env.hosts = ['34.138.32.248', '3.226.74.205']

def do_pack():
    """Creates a compressed archive of the web_static folder"""
    if not os.path.exists("versions"):
        os.makedirs("versions")
    now = datetime.now()
    file_name = "web_static_{}{}{}{}{}{}.tgz".format(
        now.year, now.month, now.day, now.hour, now.minute, now.second)
    try:
        local("tar -cvzf versions/{} web_static".format(file_name))
        return "versions/{}".format(file_name)
    except:
        return None

def do_deploy(archive_path):
    """Deploys the static files to the host servers.
    Args:
        archive_path (str): The path to the archived static files.
    """
    if not os.path.exists(archive_path):
        return False
    file_name = os.path.basename(archive_path)
    folder_name = file_name.split('.')[0]
    folder_path = "/data/web_static/releases/{}/".format(folder_name)
    success = False
    try:
        put(archive_path, "/tmp/{}".format(file_name))
        run("mkdir -p {}".format(folder_path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder_path))
        run("rm /tmp/{}".format(file_name))
        run("mv {}web_static/* {}".format(folder_path, folder_path))
        run("rm -rf {}web_static".format(folder_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_path))
        print('New version deployed!')
        success = True
    except:
        success = False
    return success

def deploy():
    """Performs complete deployment"""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
