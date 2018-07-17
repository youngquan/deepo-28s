# -*- coding: utf-8 -*-
import textwrap
import functools


class Composer(object):

    def __init__(self, modules, versions={}, cpu_only=False):
        if len(modules) == 0:
            raise ValueError('Modules should contain at least one module')
        pending = self._traverse(modules)
        self.modules = [m for m in self._toposort(pending)]
        self.instances = self._get_instances(versions)
        self.cpu_only = cpu_only

    def get(self):
        return self.modules

    def ver(self, module):
        for ins in self.instances:
            if ins.__class__ is module:
                return ins.version
        return None

    def to_dockerfile(self):

        def _indent(n, s):
            prefix = ' ' * 4 * n
            return ''.join(prefix + l for l in s.splitlines(True))

        ports = ' '.join([str(p) for m in self.instances for p in m.expose()])
        return textwrap.dedent(''.join([
            _indent(3, ''.join([
                self._split('module list'),
                ''.join('# %s\n' % repr(m)
                    for m in self.instances if repr(m)),
                self._split(),
            ])),
            r'''
            FROM nvidia/cuda:8.0-cudnn6-devel
            ''' if not self.cpu_only else
            r'''
            FROM ubuntu:16.04
            ''',
            r'''
            COPY sources.list /etc/apt/
            ''',
            r'''
            RUN APT_INSTALL="apt-get install -y --no-install-recommends" && \
                PIP_INSTALL="python -m pip --no-cache-dir install --upgrade -i https://mirrors.aliyun.com/pypi/simple/" && \
                GIT_CLONE="git clone --depth 10" && \

                rm -rf /var/lib/apt/lists/* \
                       /etc/apt/sources.list.d/cuda.list \
                       /etc/apt/sources.list.d/nvidia-ml.list && \

                apt-get update && \
            ''',
            '\n',
            '\n'.join([
                ''.join([
                    _indent(3, self._split(m.name())),
                    _indent(1, m.build()),
                ]) for m in self.instances
            ]),
            '\n',
            _indent(3, self._split('config & cleanup')),
            r'''
                ldconfig && \
                apt-get clean && \
                apt-get autoremove && \
                rm -rf /var/lib/apt/lists/* /tmp/* ~/*
            ''',
            r'''
            EXPOSE %s
            ''' % ports if ports else '',
            r'''
            # Add Tini
            ENV TINI_VERSION v0.18.0
            ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
            RUN chmod +x /tini
            ENTRYPOINT ["/tini", "--"]
            ''',
            r'''
            # Add Workdir
            WORKDIR "/home"
            ''',
            r'''
            ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
            ENV HADOOP_INSTALL=/usr/local/hadoop
            ENV PATH=$PATH:$HADOOP_INSTALL/bin
            ENV PATH=$PATH:$HADOOP_INSTALL/sbin
            ENV HADOOP_HDFS_HOME=$HADOOP_INSTALL
            ENV HADOOP_HOME=/usr/local/hadoop
            ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$JAVA_HOME/jre/lib/amd64/server
            ENV HADOOP_USER_NAME=hdfs
            ENV HDFS_NS=hdfs://hdfs
            ''' if 'hdfs' in [repr(m).split(' ')[0] for m in self.instances] else
            r''''''
            ,
            r'''
            # Add start script
            COPY start.sh /usr/local/bin/
            RUN chmod +x /usr/local/bin/start.sh
            ENV SHELL=/bin/bash
            ENV LANG C.UTF-8
            CMD ["start.sh"]
            ''',
            ]))

    def _traverse(self, modules):
        seen = set(modules)
        current_level = modules
        while current_level:
            next_level = []
            for module in current_level:
                yield module
                for child in (dep for dep in module.deps if dep not in seen):
                    next_level.append(child)
                    seen.add(child)
            current_level = next_level

    def _toposort(self, pending):
        data = {m: set(m.deps) for m in pending}
        for k, v in data.items():
            v.discard(k)
        extra_items_in_deps = functools.reduce(
            set.union, data.values()) - set(data.keys())
        data.update({item: set() for item in extra_items_in_deps})
        while True:
            ordered = set(item for item, dep in data.items() if len(dep) == 0)
            if not ordered:
                break
            for m in sorted(ordered, key=lambda m: m.__name__):
                yield m
            data = {
                item: (dep - ordered)
                for item, dep in data.items()
                if item not in ordered
            }
        if len(data) != 0:
            raise ValueError(
                'Circular dependencies exist among these items: '
                '{{{}}}'.format(', '.join(
                    '{!r}:{!r}'.format(
                        key, value) for key, value in sorted(
                        data.items()))))

    def _split(self, title=None):
        split_l = '# ' + '=' * 66 + '\n'
        split_s = '# ' + '-' * 66 + '\n'
        s = split_l if title is None else (
            split_l + '# %s\n' % title + split_s)
        return s

    def _get_instances(self, versions):
        inses = []
        for m in self.modules:
            ins = m(self)
            if m in versions:
                ins.version = versions[m]
            inses.append(ins)
        return inses
