#/bin/bash


sudo apt-get update

apt-get remove -y vim-tiny

packages=(cmatrix screenfetch mlocate net-tools lrzsz cron autojump xclip yarn npm \
vim curl libappindicator1 libindicator7 smplayer yarn libnss-mdns:i386 \
git g++ build-essential qt5-qmake qt5-default qttools5-dev-tools \
axel openssh-client openssh-serve gcc cmake build-essential snap \
apt-transport-https ca-certificates curl gnupg2 software-properties-common)

for package in ${packages[@]}; do

    sudo apt install -y $package

done

sudo apt-get update
clear
