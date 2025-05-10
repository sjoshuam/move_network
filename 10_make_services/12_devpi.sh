#!/bin/bash

cd $HOME/code
pip install devpi devpi-client


## start a devpi server
devpi-server --init
devpi-server --start --host 127.0.0.1 --port 3141


## configure devpi client
devpi use http://127.0.0.1:3141
devpi login root --password=""
devpi user -m root password=$(cat .password.txt)
rm password.txt


## create a PyPI mirror TODO: ENHANCE PACKAGE LIST
PACK_A="pandas>=2.0 pyspark>=3.2 dask>=2025.1 igraph>=0.7"
PACK_B="pytorch_geometric>=2.2 scikit-learn>=1.3 umap>=0.2"
PACK_C="plotly>=5.17 tabpy>=0.8"
PACK_Z=$PACK_A" "$PACK_B" "$PACK_C
devpi index -c pypi-mirror mirror_url=https://pypi.org/simple mirror_whitelist=$PACK_Z


## Notes TODO
        ## configure pip to use mirror: pip config set global.index-url http://127.0.0.1/root/pypi-mirror/
        ## will be more complex with the container bit
        ## might be a good opportunity to use a pod?
