# -*- coding: utf-8 -*-
from .__module__ import Module, source


@source('apt')
class Ssh(Module):
    
    def build(self):
        return r'''
            DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
                openssh-server && \
                mkdir /var/run/sshd && \
                echo 'root:123456' | chpasswd && \
                sed -ri 's/^PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config && \
                sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config && \
                sed -i '$a\UseDNS no' /etc/ssh/sshd_config && \
                '''

    def expose(self):
        return [
            22,  # expose port for ssh
        ]
