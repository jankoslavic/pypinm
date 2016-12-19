FROM andrewosh/binder-base

MAINTAINER Michael Bright <dockerfiles@mjbright.net>

USER root

RUN pip install --upgrade pip

# ---- As advised here:
#    https://github.com/binder-project/binder/issues/50
RUN pip install jupyter_client
RUN pip install requirements.txt

# ---- Install bash_kernel:
# Make sure not to create a cache dir else NB_UID switching
# will hit issues.
RUN pip install --no-cache-dir bash_kernel
RUN python -m bash_kernel.install

# ---- Clone my metakernel fork:
#RUN mkdir -p ~/src/git && \
#    cd ~/src/git && \
#    git clone https://github.com/mjbright/metakernel

# ---- Install my metakernel fork:
#RUN pip install setuptools
#RUN find ~/src/git/metakernel
#RUN cd ~/src/git/metakernel                 && python ./setup.py install
#RUN cd ~/src/git/metakernel/metakernel_bash && python ./setup.py install
#RUN cd ~/notebooks

# ---- Install RISE extension
RUN cd ~/src/git/ && \
    git clone https://github.com/damianavila/RISE && \
    cd ~/src/git/RISE && \
    python setup.py install
#### # ---- Install xonsh
#### RUN pip install --user xonsh

# ---- Show installed kernels and python/pip versions:
RUN jupyter kernelspec list
RUN which python
RUN which pip

USER main

#VOLUME ["/data"]
