#!/usr/bin/python3
'''
    Fabric script (based on the file 1-pack_web_static.py)
      that distributes an archive to your web servers,
      using the function do_deploy
'''
from datetime import datetime
from fabric.api import *
from os import path

env.hosts = ['18.206.192.179', '100.25.37.2']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    '''Deploy to server'''
    try:
        if not (path.exists(archive_path)):
            return False
        put(archive_path, "/tmp/")
        ts = archive_path[-18:-4]
        run('sudo mkdir -p /data/web_static/releases/\
            web_static_{}/'.format(ts))
        run('sudo tar -xzf /tmp/web_static{}.tgz -C \
            /data/web_static/releases/web_static_{}/\
            .format(ts, ts)')
        run('sudo rm /tmp/web_static_{}.tgz'.fomrat(ts))
        run('sudo mv /data/web_static/releases/web_static_{}/\
            web_static/* /data/web_static/releases/web_static_{}/'
            .format(ts, ts))
        run('sudo rm -rf /data/web_static/releases/\
            web_static_{}/web_static'.format(ts))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s /data/web_static/releases/\
            web_static_{}/ /data/web_static/current'
            .format(ts))

    except:
        return False
    return True
