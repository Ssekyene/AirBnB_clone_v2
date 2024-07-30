#!/usr/bin/python3
"""
Fabric script that generates .tgz archive from contents of the web_static
folder of your AirBnB Clone repo, using the function do_pack
"""
from fabric.api import *
from datetime import datetime

@task
def do_pack():
    """
    Function that compresses directory
    Returns archive pass on access; None on fail
    """

    # set up datetime
    now = datetime.now()
    timestamp = now.strftime('%Y%m%d%H%M%S')
    archive_name = 'versions/web_static_' + timestamp + '.tgz'

    # Create archive
    local('mkdir -p versions/')
    result = local('tar -czvf {} web_static/'.format(archive_name))

    # Check success
    if result.succeeded:
        return archive_name
    return None
