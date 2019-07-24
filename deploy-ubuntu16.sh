#!/bin/bash

export DEBIAN_FRONTEND=noninteractive

# Check if user is root
[ $(id -u) != "0" ] && { echo "${CFAILURE}Error: You must be root to run this script${CEND}"; exit 1; }

# Force Locale

export LC_ALL="en_US.UTF-8"
echo "LC_ALL=en_US.UTF-8" >> /etc/default/locale
locale-gen en_US.UTF-8

# Set My Timezone

ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# update
sudo apt update 

sudo apt-get install -y vim zsh subversion git curl python-pip python3-pip ipython3 wireshark

# set pip source
mkdir ~/.pip
cat > ~/.pip/pip.conf << EOF
[global]
index-url = https://pypi.douban.com/simple
trusted-host = pypi.douban.com
EOF

# upgrade pip
pip install --upgrade pip
pip3 install --upgrade pip

sudo sed -i "s/from pip import main/from pip._internal import main/g" /usr/bin/pip
sudo sed -i "s/from pip import main/from pip._internal import main/g" /usr/bin/pip3

pip3 install ipython


# install sublime text3
sudo add-apt-repository ppa:webupd8team/sublime-text-3
sudo apt-get update
sudo apt-get install -y sublime-text-installer

# install oh-my-zsh
sudo wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | sh

# switch to oh-my-zsh
chsh -s /usr/bin/zsh

# install pipenv
sudo pip install pipenv

