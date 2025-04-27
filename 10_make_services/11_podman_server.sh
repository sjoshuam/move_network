#!/bin/bash

## install postman
apt-get -y install podman

## download useful images
podman pull docker.io/ubuntu:24.04 ## operating system
podman pull docker.io/python:3.13.3 ## programming language
podman pull docker.io/pytorch/manylinux-cuda124:latest ## deep learning + gpu processing
podman pull docker.io/postgres:17.4 ## standards compliant sql database
podman pull docker.io/neo4j:2025.02 ## graph database
podman pull docker.io/apache/spark-py:v3.4.0 ## distributed analytics
podman pull docker.io/elasticsearch:8.17.4 ## search engine

    #### notes
    ## list images: podman images
    ## uninstall: apt purge podman -y && apt autoremove -y

  