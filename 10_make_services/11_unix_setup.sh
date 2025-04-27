## TIMEZONE: set the timezone
timedatectl set-timezone America/New_York


## UPGRADE: apply all updates
apt-get update
apt-get dist-upgrade -y
apt-get autoremove -y
apt-get autoclean -y


## SSH SERVER: set up ssh server
apt-get install openssh-server -y
systemctl start ssh
systemctl enable ssh
echo "SSH login:" $(whoami)"@"$(hostname -I)


## BASHRC:  modify the bashrc file
if [ ! -f "~.bashrc_backup" ]; then cp ~/.bashrc ~/.bashrc_backup; fi
cp ~/.bashrc_backup ~/.bashrc


## UTILITIES: install various useful software
apt-get install ca-certificates curl -y # web untilities