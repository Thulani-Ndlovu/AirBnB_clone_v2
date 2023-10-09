#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents
 of the web_static
folder of your AirBnB Clone repo, using the function do_pack
"""
from datetime import datetime
from fabric.api import local
from fabric.decorators import runs_once


@runs_once
def do_pack():
    '''Generate a .tgz archive'''
    local("mdkir -p versions")
    path_ = ("versions/web_static_{}.tgz".
             format(datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")))
    outcome = local("tar -cvzf {} web_static".format(path_))
    if outcome.failed:
        return None
    return path_
