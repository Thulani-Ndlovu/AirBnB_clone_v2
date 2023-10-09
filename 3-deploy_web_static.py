#!/usr/bin/python3
'''
    Fabric script (based on the file 2-do_deploy_web_static.py)
    that creates and distributes an archive to your web servers,
    using the function deploy
'''

import os
from datetime import datetime
from fabric.api import local, put, run, runs_once, env


env.hosts = ['18.206.192.179', '100.25.37.2']


@runs_once
def do_pack():
    """creates and distributes an archive to web servers"""
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    current_time = datetime.now()
    outcome = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        current_time.year,
        current_time.month,
        current_time.day,
        current_time.hour,
        current_time.minute,
        current_time.second
    )
    try:
        print("Packing web_static to {}".format(outcome))
        local("tar -cvzf {} web_static".format(outcome))
        archiveSize = os.stat(outcome).st_size
        print("web_static packed: {} -> {} Bytes".format(outcome, archiveSize))
    except Exception:
        outcome = None
    return outcome


def do_deploy(archive_path):
    '''Deploy to server'''
    if not os.path.exists(archive_path):
        return False
    fileName = os.path.basename(archive_path)
    folderName = fileName.replace(".tgz", "")
    path_ = "/data/web_static/releases/{}/".format(folderName)
    successful = False
    try:
        put(archive_path, "/tmp/{}".format(fileName))
        run("mkdir -p {}".format(path_))
        run("tar -xzf /tmp/{} -C {}".format(fileName, path_))
        run("rm -rf /tmp/{}".format(fileName))
        run("mv {}web_static/* {}".format(path_, path_))
        run("rm -rf {}web_static".format(path_))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(path_))
        print('New version is now LIVE!')
        successful = True
    except Exception:
        successful = False
    return successful


def deploy():
    """Archive and deploy static files to the servers.
    """
    archive_path = do_pack()
    return do_deploy(archive_path) if archive_path else False
