#!/bin/bash

#
# Deployment script  / entrypoint
# Intended to be used along the git-partial-clone image
#

# Update the source code
GIT_DIR=/home/${PARENT_DIR}/${REPO_NAME}/${REMOTE_PARTIAL_DIR}
[ -d ${GIT_DIR} ] && cd $GIT_DIR || exit 1
git checkout . && git fetch && git pull

# Install packages
pip3 install -r ./requirements.txt

exec python3 TaskService.py
