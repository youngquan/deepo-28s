#!/bin/bash
/usr/sbin/sshd && \
jupyter notebook --NotebookApp.password='sha1:a896891e0ccd:41eaf8c58de16421e7a6b7d5065ad6cbc3b209cd' \
                 --ip=* \
                 --no-browser \
                 --allow-root \
