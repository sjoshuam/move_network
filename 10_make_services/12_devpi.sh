#!/bin/bash
## sandbox container: podman run -it --rm ubuntu:24.04 bash

cd $HOME


## apply all updates
apt-get update -y
apt-get dist-upgrade -y && apt-get autoremove -y && apt-get autoclean -y

## set time zone
DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata
ln -sf /usr/share/zoneinfo/America/New_York /etc/localtime
echo "America/New_York" > /etc/timezone


## set password
apt-get install openssl -y
openssl rand -hex 4 > .password.txt
chmod 400 .password.txt


## install pip & dev pi
apt-get install python3.12 python3.12-venv -y
python3.12 -m venv venv
source venv/bin/activate
pip install devpi devpi-server --no-input --quiet


## start a devpi server
DEBIAN_FRONTEND=noninteractive apt-get install systemctl  -y
apt-get install supervisor -y
devpi-init
devpi-gen-config
supervisord -c gen-config/supervisord.conf


## create a PyPI mirror
PACK_A="pandas>=2.0,pyspark>=3.2,dask>=2025.1,igraph>=0.7"
PACK_B="pytorch_geometric>=2.2,scikit-learn>=1.3,umap>=0.2"
PACK_C="plotly>=5.17,tabpy>=0.8"
PACK_Z=$PACK_A","$PACK_B","$PACK_C
devpi index -c allowed mirror_whitelist=$PACK_Z


## configure devpi client
devpi login root --password=""
devpi user -m root password=$(cat .password.txt)
export PIP_INDEX_URL=http://localhost:3141/root/pypi/allowed




## Notes TODO
        ## configure pip to use mirror: pip config set global.index-url http://127.0.0.1/root/pypi-mirror/
        ## will be more complex with the container bit
        ## might be a good opportunity to use a pod?
        ## sandbox container: podman run -it --rm ubuntu:24.04 bash

        ## build the image: podman build -f 12_devpi.cont -t 12_devpi
        ## delete a container: podman rm 12_devpi
        ## start the container: podman run -d --name 12_devpi 12_devpi
        ## check container: podman ps -a
        ## check logs: podman logs 12_devpi
        ## ssh into container: podman exec -it 12_devpi sh
        ## devpi index -c pypi-mirror mirror_url=https://pypi.org/simple mirror_whitelist=$PACK_Z
        ## devpi index --list
        ## devpi index --delete
        ## devpi-server --offline-mode
