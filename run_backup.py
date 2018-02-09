import json
import os
import sys
import pwd
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
packageConfig = backup_conf.PACKAGES_CONFIG
customPackagesConfig = backup_conf.CUSTOM_PACKAGES_CONFIG

# Replaces values at dict1[key] with dict2[key]
def replaceValues(dict1, dict2):
    for key in dict2:
        dict1[key] = dict2[key]
    return dict1

# Get paths for packages config files
def getPackageList (softwarelist, softwarepaths):
    backupfiles = []
    for software in softwarelist:
        try:
            if type(softwarepaths[software]) is list: # Multiple files/directories
                for path in softwarepaths[software]:
                    backupfiles.append(path)
            else:
                backupfiles.append(softwarepaths[software]) # Single file/directory
        except KeyError as e: # If not in softwarepaths
            print("ERROR: the path(s) for " + str(e) + \
                " is not in the default_paths.py dictionary. Please add it manually.")
        except:
            print("ERROR: An error occured when locating the default path for " + software)
    return backupfiles

# Get paths to users homes
def getUserHomes(users):
    if type(users) is str:
        if users == "none":
            return []
        elif users == "current":
            return [os.environ['HOME']]
        elif users == "all":
            return ["/home"]
        else:
            print("ERROR: invalid format for USERS in backup_conf.py")
            print('Expecting "all", "current", "none" or a list of usernames.')
            return []
    else:
        userhomes = []
        for user in users:
            try:
                pwd.getpwnam(user)
                userhomes.append(os.path.expanduser("~"+user))
            except KeyError:
                print("ERROR: User " + user + " does not exist, skipping.")
            except TypeError as e:
                print("ERROR: Cannot find user " + str(user) + " Exception: " + str(e))
        return userhomes

# Copy the files in filelist to the backup directory
def copyFiles(files, bpath):
    for src in files:
        src = os.path.expanduser(src) # Handle "~/" in paths
        dst = bpath + src
        try:
            if os.path.isdir(src):              # Is a directory
                if os.path.isdir(dst):          # Directory already exist in dst
                    print("INFO: " + dst + " already exists. Will overwrite.") #TODO add prompt
                    rmtree(dst)
                elif os.path.isfile(dst):       # Regular file already exist in dst
                    print("ERROR: " + dst + " is a regualar file. Will overwrite.") #TODO add prompt
                    os.remove(dst)
                # Directory does not exist :)
                print("Copying " + src + " to " + dst)
                copytree(src, dst)
            elif os.path.isfile(src):           # Is a file
                if os.path.isdir(dst):          # Directory already exists in dst
                    print("ERROR: " + dst + " is a directory. Will overwrite.") #TODO add prompt
                    rmtree(dst)
                elif os.path.isfile(dst):       # Regular file already exists in dst
                    print("INFO: " + dst + " already exists. Will overwrite.")
                    os.remove(dst)
                if not(os.path.isdir(bpath + os.path.dirname(src))):
                    os.makedirs(bpath + os.path.dirname(src))
                print("Copying " + src + " to " + dst)
                copy(src, dst)
            else:
                print("ERROR: Couldn't find " + src)
        except IOError as e:
            print(str(e))
        except OSError as e:
            print(e)
        except Exception as e:
            raise


parser = argparse.ArgumentParser(description="""
    A software used to backup config files and user homes in Ubunutu/Debian based distros.
    By default everything specified in backup_conf.py will be backed up.
    """)
parser.add_argument('-n','--noroot', action='store_const',\
    help='run without root priveleges.', const=True)
parser.add_argument('-u', '--users', action='store_const',\
    help='Don\'t backup users homes.', const=True)
parser.add_argument('-c', '--custom', action='store_const',\
    help='Don\'t backup custom files/directories in CUSTOM_FILES.', const=True)
parser.add_argument('-p', '--packages', action='store_const',\
    help='Don\'t backup packages config files/directories in PACKAGES_CONFIG.', const=True)
parser.add_argument('-o', '--override', action='store_const',\
    help='Don\'t override/include the packages in CUSTOM_PACKAGES_CONFIG.', const=True)
args = parser.parse_args()

# Check for sudo
if not(os.getuid() == 0) and not(args.noroot):
    print("WARNING: Running as non-root, you might not have permission to copy some files.")
    print("If you still want to run without root priveleges, please add the --noroot flag")
    sys.exit(1)

# Create backup directory
try:
    print("Creating backup directory")
    if backupPath.endswith('/'):
        backupPath = backupPath[:-1]
    os.makedirs(backupPath)
except:
    #TODO add prompt if user want to override
    print("Backup directory exists")

# Backup users
if not(args.users): # True if -u flag is NOT set
    userhomes = getUserHomes(users)
    copyFiles(userhomes, backupPath)

# Backup custom files
if not(args.custom): # True if -c flag is NOT set
    copyFiles(customFiles, backupPath)

# Backup packages config
if not(args.packages): # True if -p flag is NOT set
    packagePaths = getPackageList(packageConfig, defaultPaths)
    if not(args.override): # True if -o flag is NOT set
        packagePaths = replaceValues(packagePaths, customPackagesConfig)
    copyFiles(packagePaths, backupPath)
