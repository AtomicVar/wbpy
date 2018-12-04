#!/bin/bash

sudo ln -s $(pwd)/src/wb.py /usr/local/bin/wb
sudo chmod a+x /usr/local/bin/wb
echo "安装成功"