# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source, version
from .python import Python


@dependency(Python)
@source('pip')
@version('1.4.1')
class Tensorflow(Module):

    def build(self):
        return r'''
            $PIP_INSTALL \
                tensorflow%s==%s \
                && \
        ''' % ('' if self.composer.cpu_only else '_gpu', self.version)

    def expose(self):
        return [
            6006,  # expose port for TensorBoard
        ]
