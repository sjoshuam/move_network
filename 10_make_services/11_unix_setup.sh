#!/bin/bash

## TIMEZONE: set the timezone
timedatectl set-timezone America/New_York


## UPGRADE: apply all updates
apt-get update -y
apt-get dist-upgrade -y
apt-get autoremove -y
apt-get autoclean -y


## generate ssh keys and set up server
apt-get install openssh-server -y
if [ ! -d "$HOME/.ssh" ]; then mkdir $HOME/.ssh; fi
ssh-keygen -t ed25519 -C $(hostname) -f $HOME/.ssh/id_ed25519 -N ""
systemctl start ssh
systemctl enable ssh

    #### notes
    ## get public key: cat $HOME/.ssh/id_ed25519.pub
    ## make an rsa key: ssh-keygen -t rsa -b 4096 -C $(hostname) -f $HOME/.ssh/id_sa
    ## mac: system preferences > sharing > remote login
    ## Check server status: systemctl status ssh
    ## Shut down server: systemctl stop ssh


## BASHRC:  modify the bashrc file
if [ ! -f "$HOME/.bashrc_backup" ]; then echo "Backing up bashrc" && cp $HOME/.bashrc $HOME/.bashrc_backup; fi
cp $HOME/.bashrc_backup $HOME/.bashrc


## UTILITIES: install various useful software
apt-get install ca-certificates curl -y # web untilities
apt-get install git -y # git


## DIRECTORIES: create a standard directory for code
if [ ! -d "$HOME/code" ]; then echo "Making code directory" && mkdir $HOME/code; fi


### REMINDERS: Misc.
    ## basic loop: for iter in a b c; do echo iter; done
    ## get ssh login: echo "SSH login:"ssh $(whoami)"@"$(hostname -I)