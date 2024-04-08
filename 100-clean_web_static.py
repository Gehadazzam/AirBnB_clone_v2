#!/usr/bin/python3
"""
    deletes out-of-date archives
"""
from fabric.api import *
import os


env.hosts = ["54.90.13.191", "52.3.251.54"]


def do_clean(number=0):
    """clean data"""

    number = 1 if int(number) == 0 else int(number)
    arc = sorted(os.listdir("versions"))
    [arc.pop for n in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(n)) for n in arc]

    with cd("/data/web_static/releases"):
        arc = run("ls -tr").split()
        arc = [num for num in arc if "web_static_" in arc]
        [arc.pop() for n in range(number)]
        [run("rm -rf ./{}".format(n)) for n in arc]
