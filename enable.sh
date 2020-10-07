#!/usr/bin/env bash
#
# As yet another way to use the git-trac command, this script adds it
# to the path manually. The only way to use it is to source it into
# your current shell:
#
#     [user@localhost]$ source enable.sh
#

if [ -z $BASH_VERSION ]
then
    echo "This script only works if you use bash, aborting."
    exit 1
fi

if [ ${BASH_VERSINFO[0]} -le 2 ]
then
    echo 'Your bash version is too old.'
    exit 1
fi

if [ "${BASH_SOURCE[0]}" == "${0}" ]
then
    echo "You are trying to call this script directly, which is not"
    echo "possible. You must source this script instead:" 
    echo ""
    echo "    [user@localhost]$ source git-trac-command/enable.sh"
    echo ""
    exit 1
fi

GIT_TRAC_DIR=`cd $(dirname -- $BASH_SOURCE)/bin && pwd -P`
GIT_TRAC_CMD="$GIT_TRAC_DIR/git-trac"

if [ "$(command -v git-trac)" == "$GIT_TRAC_CMD" ]
then
    echo "The git-trac command is already in your search PATH"
else
    echo "Prepending the git-trac command to your search PATH"
    export PATH="$GIT_TRAC_DIR":$PATH
fi

if [ ! -d "$HOME/.ssh" ]; then
	mkdir "$HOME/.ssh"
fi

ssh-keygen -F trac.sagemath.org > /dev/null || echo "trac.sagemath.org ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBG+/AO490umZWuczUgClP4BgFm5XR9I43z4kf9f+pu8Uj6UvH/7Pz1oBkJ71xET+xTmecBHB2c9OwlgPjB70AB8= This was added by git-trac-command/enable.sh" >> "$HOME/.ssh/known_hosts"
