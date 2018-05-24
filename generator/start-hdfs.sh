#!/bin/bash
CLASSPATH=$(${HADOOP_HDFS_HOME}/bin/hadoop classpath --glob)
$*