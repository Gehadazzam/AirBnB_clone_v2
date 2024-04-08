#!/usr/bin/python3
"""
    Fabric script that generates a .tgz archive from
    the contents of the web_static folder of your AirBnB Clone repo,
    using the function do_pack
"""
from datetime import datetime as dt
from fabric.api import *
from os.path import basename, exists

env.hosts = ["54.90.13.191", "52.3.251.54"]


def do_deploy(archive_path):
    """
    function to return the path of archive
    """

    if not exists(archive_path):
        return False
    try:
        arc_name = basename(archive_path)
        arc_dir = "/data/web_static/releases/{}".format(arc_name.split(".")[0])
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(arc_dir))
        run("sudo tar -xzf /tmp/{} -C {}".format(arc_name, arc_dir))
        run('sudo rm /tmp/{}'.format(arc_name))
        run('sudo mv {}/web_static/* {}'.format(
            arc_dir, arc_dir
        ))
        run("sudo rm -rf {}/web_static".format(arc_dir))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(arc_dir))
        return True
    except Exception:
        return False
