# Created by martengooz
# All configuration should be done in here

# Path to where to store the backed up files and directories.
# WARNING: All conflicting files or folders in the path will be overwritten
BACKUP_PATH = "backup/"

# Specify users homes to backup.
# Valid values are:
#  * USERS = "all"       # All users homes will be backed up
#  * USERS = "current"   # The current user will be backed up
#  * USERS = "none"      # No users home will be backed up
#  * USERS = [   "list",
#                "of",
#                "users"]    # You should probably run as root multiple users is used
USERS = "current"

# A list of custom files/directories to backup
CUSTOM_FILES = [
    # Commented out lines will be ignored
    #"/path/to/file/or/directory",
    #"/media/documents/",
    #"~/.bashrc"
]

# Specify what package config files you want to backup.
# A list of available packages can be found in default_paths.py
PACKAGES_CONFIG = [
    "ssh",
    #"samba",
    #"php7.0-cgi",
    #"ddclient",
    #"cron"
]

# Add your own custom packages config files.
# If the package name already exists in default_paths.py it will be overridden
# with the path specified below.
CUSTOM_PACKAGES_CONFIG = {
    # Examples:
    # "ssh":"/path/to/config",
    # "otherpackage": [\
    #     "/otherpackage/first.conf",
    #     "/otherpackage/second.conf",
    #     "/otherpackage/confdirectory"],
}
