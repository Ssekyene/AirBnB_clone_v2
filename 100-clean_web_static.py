#!/usr/bin/python3
"""
Fabric script (based on the file 3-deploy_web_static.py) that
deletes out-of-date archives, using the function do_clean

Example usage:
fab -f 100-clean_web_static.py do_clean:number=2 -i my_ssh_private_key -u ubuntu > /dev/null 2>&1
in number=2, the 2 is the number of the most recent archives to spare
"""
from fabric.api import *
from datetime import datetime
import os


env.hosts = ['100.26.231.29', '18.214.87.0']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_pack():
    """Function to archive and to compress directory
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

        # target directory
        timestamp = archive_path[-18:-4]
        run('sudo mkdir -p /data/web_static/\
releases/web_static_{}/'.format(timestamp))

        # uncompress archive and delete .tgz
        run('sudo tar -xzf /tmp/web_static_{0}.tgz -C \
/data/web_static/releases/web_static_{0}/'
            .format(timestamp))

        # delete archive from web server
        run('sudo rm /tmp/web_static_{}.tgz'.format(timestamp))

        # move files from development dir to production dir
        run('sudo mv /data/web_static/releases/web_static_{0}/web_static/* \
/data/web_static/releases/web_static_{0}/'.format(timestamp))

        # remove the development directory
        run('sudo rm -rf /data/web_static/releases/\
web_static_{}/web_static'.format(timestamp))

        # delete pre-existing sym link
        run('sudo rm -rf /data/web_static/current')

        # create new symbolic link
        run('sudo ln -s /data/web_static/releases/\
web_static_{}/ /data/web_static/current'.format(timestamp))
    except FileNotFoundError:
        return False

    # if all ops are don correctly
    return True


def deploy():
    """
    Deploy web static
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    result = do_deploy(archive_path)
    return result


def do_clean(number=0):
    """
    Deletes out of date archives ie do_clean:number=[number to spare]
    """
    number = int(number)
    if number == 0:
        number = 1
    # to prevent errors from terminating proceeding ops 
    with settings(warn_only=True):
        with lcd('./versions'):
            result = local('ls -lt | tail -n +{} | rev | cut -f1 -d" " | rev | \
xargs -d "\n" rm'.format(2 + number))
        with cd('/data/web_static/releases/'):
            result = sudo('ls -lt | tail -n +{} | rev | cut -f1 -d" " | rev | \
xargs -d "\n" rm -r'.format(2 + number))
