#!/bin/bash

cd $HOME/code
pip install devpi devpi-client


## start a devpi server
devpi-server --init
devpi-server --start --host 127.0.0.1 --port 3141


## configure devpi client TODO: ADD PASSWORD HANDOFF
devpi use http://127.0.0.1:3141
devpi login root --password=""
devpi user -m root password=$(cat password.txt)


## create a PyPI mirror TODO: PLAN PACKAGE LIST
devpi index -c pypi-mirror mirror_url=https://pypi.org/simple mirror_whitelist="pandas pytorch_geometric"


## Notes TODO
        ## configure pip to use mirror: pip config set global.index-url http://127.0.0.1/root/pypi-mirror/
        ## will be more complex with the container bit
        ## might be a good opportunity to use a pod?
