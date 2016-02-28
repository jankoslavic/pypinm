FROM andrewosh/binder-base

MAINTAINER Janko Slavič <janko.slavic@fs.uni-lj.si>

USER root

# Add dependency
RUN apt-get update
RUN apt-get install -y graphviz

USER main

# Install requirements for Python 3
RUN /home/main/anaconda/envs/python3/bin/pip install -r requirements.txt