#!/bin/sh -e

# install packages
pip3 install jupyterthemes jupyter_contrib_nbextensions
jupyter_nbextensions_configurator yapf

# config extentions into jupyter notebook
jupyter contrib nbextension install --sys-prefix
jupyter nbextensions_configurator enable --user

# set jupyter notebook theme
# jt -l   # checkout themes
jt -t monokai -f fira -fs 12 -cellw 80% -ofs 11 -dfs 11 -T -N



