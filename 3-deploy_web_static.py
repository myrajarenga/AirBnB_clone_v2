#!/usr/bin/python3
"""a Fabric script (based on the file 2-do_deploy_web_static.py) that /
    deployes fully to webservers"""
from fabric.api import run, env, put
import os.path
from fabric.api import local
from datetime import datetime

env.hosts = ['54.236.44.93', '100.26.122.135']
env.key_filename = '~/.ssh/school'
env.user = 'ubuntu'


def do_pack():
    """Compressing the contents of web_static folder and return\
            the path of the archive"""
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    pathfile = "versions/web_static_{}.tgz".format(time)

    try:
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(pathfile))
        return pathfile
    except Exception as e:
        return None


def do_deploy(archive_path):
    """Generate the .tgz archive from the contents of web_static folder"""

    if not os.path.isfile(archive_path):
        return False

    # Get the name of the compressed file and remove the file extension
    compresedfile = archive_path.split("/")[-1]
    no_extension = compresedfile.split(".")[0]

    try:
        # Define the remote path and symlink to be used for deployment
        path = "/data/web_static/releases/{}/".format(no_extension)
        sym_link = "/data/web_static/current"

        # Upload the compressed file to the server
        put(archive_path, "/tmp/")

        """ Create the directory for the release and extract the compressed\
                file into it"""
        run("sudo mkdir -p {}".format(path))
        run("sudo tar -xvzf /tmp/{} -C {}".format(
            compresedfile, path))

        """Clean up the compressed file and move the web files to the\
                release directory"""
        run("sudo rm /tmp/{}".format(compresedfile))
        run("sudo mv {}/web_static/* {}".format(path, path))
        run("sudo rm -rf {}/web_static".format(path))

        # Update the symlink to point to the new release directory
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -sf {} {}".format(path, sym_link))

        # Return success if the deployment was successful
        return True
    except Exception as e:

        # If an exception occurred during deployment, return failure
        return False


def deploy():
    """call do_pack() and do_deploy"""
    file_path = do_pack()
    if file_path is None:
        return False
    return do_deploy(file_path)
