# Created by martengooz
# All configuration should be done in here

# Path to where to store the backed up files and directories.
# WARNING: All conflicting files or folders in the path will be overwritten
BACKUP_PATH = "/tmp/backup/"

# Specify users homes to backup.
# Valid values are:
#  * USERS = "all"       # All users homes will be backed up
#  * USERS = "current"   # The current user will be backed up
#  * USERS = "none"      # No users home will be backed up
#  * USERS = [   "list",
#                "of",
#                "users"]    # You should probably run as root if a list is used
USERS = ["none"]

# A list of custom files/directories to backup
CUSTOM_FILES = [
    # Commented out lines will be ingored
    #"/path/to/file/or/directory",
    #"~/.zshrc",
    #"/media/documents/",
    "~/.bashrc"
]

# Specify what package config files you want to backup.
# A list of available packages can be found in default_paths.json
PACKAGE_CONFIG = [
    "ssh",
    "samba",
    #"php7.0-cli",
    #"php7.0-cgi",
    #"apache2",
    #"fail2ban",
    #"ddclient",
    #"nginx",
    #"lighttpd",
    #"ddclient",
    "cron"
]

# Override the default path of a packages config files listed in default_paths.json
OVERRIDE_DEFAULT_PATH = {
    #"[software]":"/path/to/config",
    "ssh":"/tmp/ssh/sshd.conf"
}
