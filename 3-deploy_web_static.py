#!/usr/bin/python3
"""
Fabric script (based on the file 2-do_deploy_web_static.py) that creates
and distributes an archive to your web servers, using the function deploy
"""
from fabric.api import *
from datetime import datetime
import os


env.hosts = ['100.26.231.29', '18.214.87.0']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'

@task
def do_pack():
    """Function to compress directory
    Return archive path on success; None on fail
    """
    # Set up datetime
    now = datetime.now()
    timestamp = now.strftime('%Y%m%d%H%M%S')
    archive_path = 'versions/web_static_' + timestamp + '.tgz'

    # Create archive
    local('mkdir -p versions/')
    result = local('tar -cvzf {} web_static/'.format(archive_path))

    # Check if archiving was successful
    if result.succeeded:
        file_size = os.path.getsize(archive_path)
        # display the archive path and the size
        print("web_static packed: {} -> {}Bytes".format(archive_path, file_size))
        return archive_path
    return None


def do_deploy(archive_path):
    """
    creates and distributes an archive to your web servers
    """
    try:
        # Check if file path exists
        if not (os.path.exists(archive_path)):
            return False

        # upload archive to web server tmp directory
        put(archive_path, '/tmp/')

        # get timestamp
        timestamp = archive_path[-18:-4]
        run('sudo mkdir -p /data/web_static/\
releases/web_static_{}/'.format(timestamp))

        # uncompress archive and delete .tgz
        run('sudo tar -xzf /tmp/web_static_{}.tgz -C \
/data/web_static/releases/web_static_{}/'
            .format(timestamp, timestamp))

        # delete archive from web server
        run('sudo rm /tmp/web_static_{}.tgz'.format(timestamp))

        # move files to web_static production directory
        run('sudo mv /data/web_static/releases/web_static_{}/web_static/* \
/data/web_static/releases/web_static_{}/'.format(timestamp, timestamp))

        # delete the development web_static directory
        run('sudo rm -rf /data/web_static/releases/\
web_static_{}/web_static'.format(timestamp))

        # delete pre-existing sym link
        run('sudo rm -rf /data/web_static/current')

        # create new symbolic link
        run('sudo ln -s /data/web_static/releases/\
web_static_{}/ /data/web_static/current'.format(timestamp))
    except FileNotFoundError:
        return False

        # if all ops are done correctly
    return True

@task
def deploy():
    """
    Deploy web static
    """
    archive_path = do_pack()
    
    if archive_path is None:
        return False
    result = do_deploy(archive_path)
    if result:
        print("New version deployed!")
    return result
