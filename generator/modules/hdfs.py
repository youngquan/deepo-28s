# -*- coding: utf-8 -*-
from .__module__ import Module, source, dependency, version
from .tools import Tools

@dependency(Tools)
@source('apt')
@version('2.8.2')
class Hdfs(Module):
    
    def build(self):
        return r'''
            DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
                default-jdk && \
                wget http://mirrors.tuna.tsinghua.edu.cn/apache/hadoop/common/hadoop-%s/hadoop-%s.tar.gz && \
                tar xvzf hadoop-%s.tar.gz && \
                mkdir -p /usr/local/hadoop && \
                mv hadoop-%s/* /usr/local/hadoop && \
                rm -rf hadoop-%s && \
                ''' %(self.version)
