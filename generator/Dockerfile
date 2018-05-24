# ==================================================================
# module list
# ------------------------------------------------------------------
# ssh           latest (apt)
# python        3.5    (apt)
# jupyter       latest (pip)
# tensorflow    1.4.1  (pip)
# keras         latest (pip)
# opencv        latest (git)
# ==================================================================

FROM nvidia/cuda:8.0-cudnn6-devel

COPY sources.list /etc/apt/

RUN APT_INSTALL="apt-get install -y --no-install-recommends" && \
    PIP_INSTALL="python -m pip --no-cache-dir install --upgrade -i https://mirrors.ustc.edu.cn/pypi/web/simple" && \
    GIT_CLONE="git clone --depth 10" && \

    rm -rf /var/lib/apt/lists/* \
           /etc/apt/sources.list.d/cuda.list \
           /etc/apt/sources.list.d/nvidia-ml.list && \

    apt-get update && \

# ==================================================================
# ssh
# ------------------------------------------------------------------

    DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
        openssh-server && \
        mkdir /var/run/sshd && \
        echo 'root:123456' | chpasswd && \
        sed -ri 's/^PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config && \
        sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config && \
        sed -i '$a\UseDNS no' /etc/ssh/sshd_config && \

# ==================================================================
# tools
# ------------------------------------------------------------------

    DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
        build-essential \
        ca-certificates \
        cmake \
        wget \
        git \
        vim \
        && \

# ==================================================================
# python
# ------------------------------------------------------------------

    DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
        python3-pip \
        python3-dev \
        && \
    ln -s /usr/bin/python3 /usr/local/bin/python && \
    pip3 --no-cache-dir install --upgrade -i https://mirrors.ustc.edu.cn/pypi/web/simple pip && \
    $PIP_INSTALL \
        setuptools \
        && \
    $PIP_INSTALL \
        numpy \
        scipy \
        pandas \
        scikit-learn \
        matplotlib \
        Cython \
        Pillow \
        imageio \
        && \

# ==================================================================
# boost
# ------------------------------------------------------------------

    wget -O ~/boost.tar.gz https://dl.bintray.com/boostorg/release/1.65.1/source/boost_1_65_1.tar.gz && \
    tar -zxf ~/boost.tar.gz -C ~ && \
    cd ~/boost_* && \
    ./bootstrap.sh --with-python=python3.5 && \
    ./b2 install --prefix=/usr/local && \

# ==================================================================
# jupyter
# ------------------------------------------------------------------

    $PIP_INSTALL \
        jupyter \
        && \

# ==================================================================
# tensorflow
# ------------------------------------------------------------------

    $PIP_INSTALL \
        tensorflow_gpu==1.4.1 \
        && \

# ==================================================================
# keras
# ------------------------------------------------------------------

    $PIP_INSTALL \
        h5py \
        keras \
        && \

# ==================================================================
# opencv
# ------------------------------------------------------------------

    DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
        libatlas-base-dev \
        libgflags-dev \
        libgoogle-glog-dev \
        libhdf5-serial-dev \
        libleveldb-dev \
        liblmdb-dev \
        libprotobuf-dev \
        libsnappy-dev \
        protobuf-compiler \
        && \

    $GIT_CLONE https://github.com/opencv/opencv ~/opencv && \
    mkdir -p ~/opencv/build && cd ~/opencv/build && \
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
          -D CMAKE_INSTALL_PREFIX=/usr/local \
          -D WITH_IPP=OFF \
          -D WITH_CUDA=OFF \
          -D WITH_OPENCL=OFF \
          -D BUILD_TESTS=OFF \
          -D BUILD_PERF_TESTS=OFF \
          .. && \
    make -j"$(nproc)" install && \

# ==================================================================
# config & cleanup
# ------------------------------------------------------------------

    ldconfig && \
    apt-get clean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/* /tmp/* ~/*

EXPOSE 22 8888 6006

# Add Tini
ENV TINI_VERSION v0.18.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

# Add Workdir
WORKDIR "/home"

# Add start script
COPY start.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/start.sh
ENV SHELL=/bin/bash
CMD ["start.sh"]
