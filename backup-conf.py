import json
from pprint import pprint
import os
from shutil import copytree, rmtree, copy

# Path to store the backup
backup_path = "/tmp/backup/"

# Names of the software to copy. Available software is in default_paths.json
software_to_backup = [
    #"ssh",
    "samba",
    #"php",
    #"apache2",
    #"fail2ban",
    #"ddclient",
    "nginx",
    #"lighttpd",
    #"ddclient",
]

default_paths = json.load(open('default_paths.json'))

def getFileList (softwarelist, softwarepaths):
    backupfiles = []
    for software in softwarelist:
        try:
            if type(softwarepaths[software]) is list: # Multiple files/directories
                for path in softwarepaths[software]:
                    backupfiles.append(path)
            else:
                backupfiles.append(softwarepaths[software]) # Single file/directory
        except KeyError, e: # If not in softwarepaths
            print "ERROR: Couldn't fint the path(s) for " + str(e) + \
                " is not in the default_paths.json dictionary. Please add it manually."
        except:
            print "ERROR: An error occured when locating the default path for " + software
    return backupfiles


# Copy the files in filelist to the backup directory
def copyFiles(files, bpath):
    for src in files:
        dst = bpath + src
        try:
            if os.path.isdir(src):              # Is a directory
                if os.path.isdir(dst):          # Directory already exist in dst
                    print "ERROR: " + dst + " already exists. Will overwrite." #TODO add prompt
                    os.removedirs(dst)
                elif os.path.isfile(dst):       # Regular file already exist in dst
                    print "ERROR: " + dst + " is a regualar file. Will overwrite." #TODO add prompt
                    os.remove(dst)
                # Directory does not exist :)
                print "Copying" + src + " to " + dst
                copytree(src, dst)
            elif os.path.isfile(src):           # Is a file
                if os.path.isdir(dst):          # Directory already exists in dst
                    print "ERROR: " + dst + " is a directory. Will overwrite." #TODO add prompt
                    os.removedirs(dst)
                elif os.path.isfile(dst):       # Regular file already exists in dst
                    print "ERROR: File exists. " + dst
                    os.remove(dst)
                if not(os.path.isdir(bpath + os.path.dirname(src))):
                    os.makedirs(bpath + os.path.dirname(src))
                print "Copying" + src + " to " + dst
                copy(src, dst)
            else:
                print "ERROR: Couldn't find " + src
        except Exception as e:
            raise

try:
    print "Creating backup directory"
    if backup_path.endswith('/'):
        backup_path = backup_path[:-1]
    os.makedirs(backup_path)
except:
    #TODO add prompt if user want to override
    print "Backup directory exists"

filelist = getFileList(software_to_backup, default_paths)
copyFiles(filelist, backup_path)
