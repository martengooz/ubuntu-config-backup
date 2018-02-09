import json
import os
import sys
import backup_conf
import default_paths
import getpass
import argparse
from shutil import copytree, rmtree, copy


# Variables
defaultPaths = default_paths.PATHS
backupPath = backup_conf.BACKUP_PATH
users = backup_conf.USERS
customFiles = backup_conf.CUSTOM_FILES
packageConfig = backup_conf.PACKAGE_CONFIG
overrideDefaultPath = backup_conf.OVERRIDE_DEFAULT_PATH

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
                " is not in the default_paths.py dictionary. Please add it manually."
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
                    print "INFO: " + dst + " already exists. Will overwrite." #TODO add prompt
                    rmtree(dst)
                elif os.path.isfile(dst):       # Regular file already exist in dst
                    print "ERROR: " + dst + " is a regualar file. Will overwrite." #TODO add prompt
                    os.remove(dst)
                # Directory does not exist :)
                print "Copying " + src + " to " + dst
                copytree(src, dst)
            elif os.path.isfile(src):           # Is a file
                if os.path.isdir(dst):          # Directory already exists in dst
                    print "ERROR: " + dst + " is a directory. Will overwrite." #TODO add prompt
                    rmtree(dst)
                elif os.path.isfile(dst):       # Regular file already exists in dst
                    print "INFO: " + dst + " already exists. Will overwrite."
                    os.remove(dst)
                if not(os.path.isdir(bpath + os.path.dirname(src))):
                    os.makedirs(bpath + os.path.dirname(src))
                print "Copying " + src + " to " + dst
                copy(src, dst)
            else:
                print "ERROR: Couldn't find " + src
        except IOError, e:
            print str(e)
        except OSError, e:
            print e
        except Exception as e:
            raise


parser = argparse.ArgumentParser()
parser.add_argument('--noroot', action='store_const', const=True)
parser.parse_args(['--noroot'])

# Check for sudo
if not(os.getuid() == 0) and not(parser.parse_args().noroot):
    print "WARNING: Not root, you might not have permission to copy some files."
    print "If you still want to run without root priveleges, please add the --no-root flag"
    sys.exit(1)

try:
    print "Creating backup directory"
    if backupPath.endswith('/'):
        backupPath = backupPath[:-1]
    os.makedirs(backupPath)
except:
    #TODO add prompt if user want to override
    print "Backup directory exists"

#copyFiles(users)
filelist = getFileList(packageConfig, defaultPaths)
copyFiles(filelist, backupPath)
