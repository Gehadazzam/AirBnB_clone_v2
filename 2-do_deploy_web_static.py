#!/usr/bin/python3
#!/usr/bin/python3
"""
    Fabric script that generates a .tgz archive from
    the contents of the web_static folder of your AirBnB Clone repo,
    using the function do_pack
"""
from datetime import datetime as dt
from fabric.api import *


def do_pack(archive_path):
    """
    function to return the path of archive
    """

    stamp = dt.now().strftime("%Y%m%d%H%M%S")
    archive = "web_static_" + stamp + ".tgz"
    local("mkdir -p versions")
    exist = local(f"tar -czvf versions/{archive} web_static/")
    if exist is None:
        return None
    else:
        return "versions/{}".format(archive)
