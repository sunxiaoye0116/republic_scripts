#!/usr/bin/env bash

TOR_CONTROLLER_IP=[RESEARCH_NETWORK_PREFIX].152
OCS_CONTROLLER_IP=[RESEARCH_NETWORK_PREFIX].152
REPUBLIC_MANAGER_IP=[RESEARCH_NETWORK_PREFIX].152

CLUSTER_NODE_LIST=../parallel_hosts/
CLUSTER_NODE_FILE=$1

GITHUB_BRANCH_VERSION="master"

# prepare Republic Agents
parallel-ssh -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l [SERVER_USERNAME] -i "cd /home/[SERVER_USERNAME]/github/republic_agent/protocol/transceiver/;git reset --hard;git pull \"https://sunxiaoye0116@github.com/sunxiaoye0116/republic_agent.git\" ${GITHUB_BRANCH_VERSION}; make clean; make"

# prepare Republic Manager
ssh [SERVER_USERNAME]@${TOR_CONTROLLER_IP} "cd /home/[SERVER_USERNAME]/github/republic_manager/;git reset --hard;git pull \"https://sunxiaoye0116@github.com/sunxiaoye0116/republic_manager.git\" ${GITHUB_BRANCH_VERSION};"
ssh [SERVER_USERNAME]@${OCS_CONTROLLER_IP} "cd /home/[SERVER_USERNAME]/github/republic_manager/;git reset --hard;git pull \"https://sunxiaoye0116@github.com/sunxiaoye0116/republic_manager.git\" ${GITHUB_BRANCH_VERSION};"
ssh [SERVER_USERNAME]@${REPUBLIC_MANAGER_IP} "cd /home/[SERVER_USERNAME]/github/republic_manager/;git reset --hard;git pull \"https://sunxiaoye0116@github.com/sunxiaoye0116/republic_manager.git\" ${GITHUB_BRANCH_VERSION}"
#;mvn clean;mvn package"

# prepare Spark
echo prepare Spark
parallel-ssh -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l [SERVER_USERNAME] -i "cd /home/[SERVER_USERNAME]/github/spark_private/;git reset --hard;git pull \"https://sunxiaoye0116@github.com/sunxiaoye0116/spark_private.git\" v1.6.1_dev-republic"

# copy netmap config
echo netmap config
parallel-scp -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l [SERVER_USERNAME] ../config_netmap.sh /home/[SERVER_USERNAME]/

# copy yarn config
echo Yarn config
parallel-scp -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l [SERVER_USERNAME] -r ../hadoop_config/hadoop/ ${HADOOP_HOME}/etc/
parallel-scp -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l [SERVER_USERNAME] -r ../hadoop_config/sbin/ ${HADOOP_HOME}/

# copy zlog.conf
parallel-scp -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l [SERVER_USERNAME] ../zlog_default.conf /home/[SERVER_USERNAME]/github/republic_agent/protocol/transceiver/

parallel-scp -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l [ROOT_USERNAME] ../hosts /etc/

DATETIME=$(date +%Y-%m-%d_%H:%M:%S)
# copy .bashrc
echo copy .bashrc
parallel-ssh -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l [SERVER_USERNAME] -i "cp /home/[SERVER_USERNAME]/.bashrc /home/[SERVER_USERNAME]/.bashrc_user_${DATETIME}"
parallel-ssh -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l [ROOT_USERNAME] -i "cp /[ROOT_USERNAME]/.bashrc /[ROOT_USERNAME]/.bashrc_rootuser_${DATETIME}"
parallel-scp -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l [SERVER_USERNAME] ../.bashrc_user /home/[SERVER_USERNAME]/.bashrc
parallel-scp -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l [ROOT_USERNAME] ../.bashrc_rootuser /[ROOT_USERNAME]/.bashrc
#
# copy .profile
echo copy .profile
parallel-ssh -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l [SERVER_USERNAME] -i "cp /home/[SERVER_USERNAME]/.profile /home/[SERVER_USERNAME]/.profile_user_${DATETIME}"
parallel-ssh -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l [ROOT_USERNAME] -i "cp /[ROOT_USERNAME]/.profile /[ROOT_USERNAME]/.profile_rootuser_${DATETIME}"
parallel-scp -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l [SERVER_USERNAME] ../.profile_user /home/[SERVER_USERNAME]/.profile
parallel-scp -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l [ROOT_USERNAME] ../.profile_rootuser /[ROOT_USERNAME]/.profile

