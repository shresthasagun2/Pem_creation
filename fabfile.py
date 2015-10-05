#!/usr/bin/python
__author__ = 'sagun'
from fabric.api import *


# Editable Config
local_user = "sagun" # local user of the workstation from which this fabfile is run
ssh_user = "abhinavmishra" # username used to ssh to the remote machine
key_dir = "/home/sagun/Keys/project_name" # the location where the keys are to be copied in the local workstation

#These section are the config of boto (default value will work fine so doesn't need to edited)
# env.hosts = list_of_host
# env.user= "root"
# env.passwords = list_of_passw
# env.warn_only = True
# env.skip_bad_hosts=True
# env.timeout=5


# No more edits


def create():
    choice = ""
    while choice != ("N" or "n" or "No"):
        print "\n\n-------------  Creating user on %s  -------------\n"
        username = prompt("Enter Username to create:")
        #password = prompt("Enter password:")
        print username
        try:
            sudo("adduser %s" %username)
            print "\n------------- User created  -------------\n"
        except:
            print "\n------------- User already exists  -------------\n"
            pass
        print "\n------------- Creating Keys -------------\n"
        with cd("/home/%s" %username):
            sudo("ssh-keygen -b 1024 -f %s -t dsa" %username)
            try:
                sudo("mkdir .ssh")
            except:
                pass
            print "\n------------- Keys created  -------------\n"
            sudo("chmod 700 .ssh")
            sudo("cat %s.pub >> .ssh/authorized_keys" %username)
            sudo("mv %s %s.pem" %(username,username) )
            sudo("chmod 600 .ssh/authorized_keys")
            sudo("chown %s .ssh" %username)
            sudo("chown %s .ssh/authorized_keys" %username)
            sudo("chmod 600 %s.pem" %username)
           # sudo("chown %s:%s /home/%s -R" %(username,username,username))
            try:
                sudo("mkdir /home/Keys")
                sudo("mv %s.pem /home/Keys" %username)
                sudo("mv %s.pub /home/Keys" %username)
            except:
                sudo("mv %s.pem /home/Keys" %username)
                sudo("mv %s.pub /home/Keys" %username)
            sudo("chown %s /home/Keys -R" %ssh_user)

        print "\n------------- Downloading Keys -------------\n"
        get("/home/Keys/%s.*" %username,"/tmp")

        local("chown %s /tmp/%s.* " %(local_user,username))
        local("mv /tmp/%s.* %s" %(username,key_dir))
        print "\n\n------------- Key files downloaded to %s   -------------\n" %key_dir
        choice = prompt("Do you want to create another user (Y/N):")
    print "\n------------- Thank you  -------------\n" 
