# Config-backup
Backup config files of packages and/or user home directories and files on Ubuntu/Debian based distros. 
Includes a list of commonly installed packages and their corresponding config files for easy backup.  

## Features:
* Easy config for commonly installed packages.
* Users `HOME` directory (all users, current user or custom users)
* Backup custom files/directories

## Requirements
* `python`

## Usage
All config is done in [backup_config.py](backup_config.py)


```
run_backup.py [-h] [-n] [-u] [-c] [-p] [-o]

optional arguments:
  -h, --help      show this help message and exit
  -n, --noroot    run without root priveleges.
  -u, --users     don't backup users homes.
  -c, --custom    don't backup custom files/directories in CUSTOM_FILES.
  -p, --packages  don't backup packages config files/directories in
                  PACKAGES_CONFIG.
  -o, --override  don't override/include the packages in
                  CUSTOM_PACKAGES_CONFIG.
```
