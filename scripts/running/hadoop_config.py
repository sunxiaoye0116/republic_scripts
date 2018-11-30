#!/usr/bin/env python

import struct
import socket
import xml.etree.ElementTree as ET

# YARN_RESOURCE_MANAGER_NODE = 16
# YARN_SERVER = [17, 18, 19, 23, 25, 27]
YARN_RESOURCE_MANAGER_NODE = 25
YARN_SERVER = range(13, 24) + range(26, 40)


SERVER_MEMORY = 102400
SERVER_CPU = 4
HDFS_TMP_DIRECTORY = '/home/[SERVER_USERNAME]/github/hadoop-2.7.4/'
# SERVER_TOTAL = 7
APP_EXECUTOR = 10
PERCENT = 1.02 * 4 / (4 + APP_EXECUTOR * 2)

IP_OFFSET_1G = '[RESEARCH_NETWORK_PREFIX].111'
IP_OFFSET_10G = '[INTERNAL_NETWORK_PREFIX].50.111'
IP_OFFSET_10G2 = '[INTERNAL_NETWORK_PREFIX].20.111'
ip_1g_long = struct.unpack("!L", socket.inet_aton(IP_OFFSET_1G))[0]
ip_10g_long = struct.unpack("!L", socket.inet_aton(IP_OFFSET_10G))[0]
ip_10g2_long = struct.unpack("!L", socket.inet_aton(IP_OFFSET_10G2))[0]
YARN_RESOURCE_MANAGER_1G_IP = socket.inet_ntoa(struct.pack('!L', ip_1g_long + YARN_RESOURCE_MANAGER_NODE))
YARN_RESOURCE_MANAGER_10G_IP = socket.inet_ntoa(struct.pack('!L', ip_10g_long + YARN_RESOURCE_MANAGER_NODE))

# yarn-site.xml
xml_filename = '../hadoop_config/hadoop/yarn-site.xml'
tree = ET.parse(xml_filename)
for child in tree.getroot():
    if child.find('name').text == 'yarn.resourcemanager.address':
        child.find('value').text = YARN_RESOURCE_MANAGER_10G_IP + ':11032'
    elif child.find('name').text == 'yarn.resourcemanager.scheduler.address':
        child.find('value').text = YARN_RESOURCE_MANAGER_10G_IP + ':11030'
    elif child.find('name').text == 'yarn.resourcemanager.resource-tracker.address':
        child.find('value').text = YARN_RESOURCE_MANAGER_10G_IP + ':11031'
    elif child.find('name').text == 'yarn.resourcemanager.admin.address':
        child.find('value').text = YARN_RESOURCE_MANAGER_10G_IP + ':11033'
    elif child.find('name').text == 'yarn.resourcemanager.webapp.address':
        child.find('value').text = YARN_RESOURCE_MANAGER_1G_IP + ':11088'
    elif child.find('name').text == 'mapreduce.jobhistory.address':
        child.find('value').text = YARN_RESOURCE_MANAGER_10G_IP + ':10020'
    elif child.find('name').text == 'mapreduce.jobhistory.webapp.address':
        child.find('value').text = YARN_RESOURCE_MANAGER_1G_IP + ':19888'
    elif child.find('name').text == 'yarn.log.server.url':
        child.find('value').text = 'http://' + YARN_RESOURCE_MANAGER_1G_IP + ':19888/jobhistory/logs'
    elif child.find('name').text == 'yarn.nodemanager.resource.memory-mb':
        child.find('value').text = '' + str(SERVER_MEMORY)
    elif child.find('name').text == 'yarn.nodemanager.resource.cpu-vcores':
        child.find('value').text = '' + str(SERVER_CPU)
tree.write(xml_filename)

# hdfs-site.xml
xml_filename = '../hadoop_config/hadoop/hdfs-site.xml'
tree = ET.parse(xml_filename)
for child in tree.getroot():
    if child.find('name').text == 'dfs.namenode.http-address':
        child.find('value').text = YARN_RESOURCE_MANAGER_1G_IP + ':50070'
    elif child.find('name').text == 'dfs.namenode.secondary.http-address':
        child.find('value').text = YARN_RESOURCE_MANAGER_1G_IP + ':50090'
    elif child.find('name').text == 'dfs.namenode.name.dir':
        child.find('value').text = HDFS_TMP_DIRECTORY + './dfs/name'
    elif child.find('name').text == 'dfs.datanode.data.dir':
        child.find('value').text = HDFS_TMP_DIRECTORY + './dfs/data'
tree.write(xml_filename)

# core-site.xml
xml_filename = '../hadoop_config/hadoop/core-site.xml'
tree = ET.parse(xml_filename)
for child in tree.getroot():
    if child.find('name').text == 'fs.defaultFS':
        child.find('value').text = 'hdfs://' + YARN_RESOURCE_MANAGER_10G_IP + ':9000/'
    elif child.find('name').text == 'hadoop.tmp.dir':
        child.find('value').text = HDFS_TMP_DIRECTORY + './tmp'
tree.write(xml_filename)

# capacity-scheduler.xml
xml_filename = '../hadoop_config/hadoop/capacity-scheduler.xml'
tree = ET.parse(xml_filename)
for child in tree.getroot():
    if child.find('name').text == 'yarn.scheduler.capacity.maximum-am-resource-percent':
        child.find('value').text = '' + str(PERCENT)
tree.write(xml_filename)

# YARN slave
SERVER_ALL = YARN_SERVER
filename = '../hadoop_config/hadoop/slaves'
with open(filename, 'w') as f:
    for server in SERVER_ALL:
        f.write('bold-node%03d\n' % (server,))

# parallel_host server
filename = '../parallel_hosts/parallel_hosts'
with open(filename, 'w') as f:
    for server in [YARN_RESOURCE_MANAGER_NODE] + YARN_SERVER:
        YARN_RESOURCE_MANAGER_10G2_IP = socket.inet_ntoa(struct.pack('!L', ip_10g2_long + server))
        f.write(YARN_RESOURCE_MANAGER_10G2_IP + ':22\n')
