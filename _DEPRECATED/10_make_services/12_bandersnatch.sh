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


## install pandas, pip and a venv
apt-get install python3.12 python3.12-venv -y
python3.12 -m venv venv
source venv/bin/activate


## install and configure bandersnatch
pip install bandersnatch --no-input --quiet

echo -e "
[mirror]
directory = pypi
master = https://pypi.org
workers = 3

[plugins]
enabled = 
    allowlist_project
    allowlist_release
    blocklist_project
    blocklist_release

[allowlist]
packages = 
    pandas>=2.0
    pyspark>=3.2
    dask>=2025.1
    igraph>=0.7
    pytorch_geometric>=2.2
    scikit-learn>=1.3
    umap>=0.2
    plotly>=5.17
    tabpy>=0.8

platforms = 
    py3.10
    py3.11
    py3.12
    py3.13
    linux

[blocklist]
platforms = 
    windows
    freebsd
    macos
" > /etc/bandersnatch.conf

bandersnatch mirror > mirror.log 2>&1 &


## spin up a server  TODO finish connecting to ports & set up a chron job for mirroring
cd pypi/web
nohup python3 -m http.server 8080 > server.log 2>&1 &


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