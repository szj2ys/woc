#!/bin/bash


#https://downloads.mariadb.org/mariadb/repositories/#distro=Debian&distro_release=jessie--jessie&mirror=escience&version=10.4
sudo apt-get install software-properties-common
sudo apt-key adv --fetch-keys 'https://mariadb.org/mariadb_release_signing_key.asc'


sudo apt-get update
sudo apt-get install mariadb-server

services mysql restart

# 设置mysql密码
sudo mysql_secure_installation

## 创建用户并Grant权限
#mysql -u root -p -e "create user 'uc'@'%' identified by 'password'"
#mysql -uroot -p -e"grant all on *.* to 'uc'@'%'"
#mysqladmin -uroot -p flush-privileges

