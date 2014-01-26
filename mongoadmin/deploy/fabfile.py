"""fabfile.py - MongoDB Deployment"""

from fabric.api import run, env, task, cd, local, put, lcd
from fabric.operations import local as lrun
from fabric.contrib import console, files

VERSION = "2.4.9"
USER = "mongodb"
DOWNLOAD_DIR = "/tmp/fabric"
DIRECTORY = "/opt/mongodb"

CONFIG = {
    "user": USER,
    "download_dir": DOWNLOAD_DIR,
    "download_url": "http://fastdl.mongodb.org/linux/mongodb-linux-x86_64-{}.tgz".format(VERSION),
    "version": VERSION,
    "directory": DIRECTORY,
    "binpath": DIRECTORY + "/bin",
    "etcpath": DIRECTORY + "/etc",
    "dbpath": DIRECTORY + "/data",
    "logpath": DIRECTORY + "/log",
    "logfile": DIRECTORY + "/log/mongodb.log",
    "mongod": DIRECTORY + "/bin/mongod",
    "conf": DIRECTORY + "/etc/mongod.conf",
    "replSet": "rs0",
    }

def initialize():
    """Initialize"""
    if len(env.hosts) == 1 and env.hosts[0] == "localhost":
        global run
        global cd
        run = lrun
        cd = lcd
    run("rm -rf {}".format(DOWNLOAD_DIR))
    run("mkdir -p {}".format(DOWNLOAD_DIR))
    
def create_user(username):
    output = run("cat /etc/passwd | cut -d: -f1")
    if not USER in output:
        command = "sudo adduser {username} --disabled-password --gecos ''"
        run(command.format(username=username))
        
def generate_conf():
    with open("mongod-template.conf") as f:
        conf_template = f.read()
    with open("mongod.conf", "w") as f:
        f.write(conf_template.format(**CONFIG))
        
    with open("mongodb-template.conf") as f:
        conf_template = f.read()
    with open("mongodb.conf", "w") as f:
        f.write(conf_template.format(**CONFIG))
        
def install_mongodb():
    if files.exists(DIRECTORY):
        question = "MongoDB installation exists on host({}); do you wish to erase and proceed?".format(env.host)
        if not console.confirm(question):
            return False
        run("sudo rm -rf {}".format(DIRECTORY))
        
    run("sudo mkdir -p {}".format(DIRECTORY))
    
    run("sudo mkdir {etcpath}".format(**CONFIG))
    run("sudo mkdir {dbpath}".format(**CONFIG))
    run("sudo mkdir {logpath}".format(**CONFIG))
    
    run("wget {download_url} -P {download_dir}".format(**CONFIG))
    cmd = "sudo tar zxvf {download_dir}/mongodb-linux-x86_64-{version}.tgz --directory {directory} --strip 1"
    run(cmd.format(**CONFIG))
    
    run("sudo chown -R {user}:{user} {folder}".format(user=USER, folder=DIRECTORY))
    
@task
def update():
    generate_conf()
    put("mongod.conf", "{etcpath}/mongod.conf".format(**CONFIG), use_sudo=True)
    run("sudo chown {user}:{user} {etcpath}/mongod.conf".format(**CONFIG))
    put("mongodb.conf", "/etc/init/mongodb.conf", use_sudo=True)
    
@task
def deploy():
    initialize()
    create_user(USER)
    install_mongodb()
    update()
    
