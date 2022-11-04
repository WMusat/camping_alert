#!/bin/bash

# if errors exist quit the script
set -e -u -o pipefail

# set some env variables
export USER="$(whoami)"
export PATH=$PATH:/home/$USER/.gvm/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games:~/bin:/usr/lib/node_modules:/user/lib/node_modules/find-campsite
export NODE_PATH=/usr/lib/node_modules

# source the python3 venv and run the script from your home directory
source /home/$USER/env/bin/activate && python /home/$USER/camping_alert.py