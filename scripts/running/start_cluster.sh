#!/usr/bin/env bash

TOR_CONTROLLER_IP=[RESEARCH_NETWORK_PREFIX].152
TOR_PORT=8010
OFP_PORT=6633
OCS_CONTROLLER_IP=[RESEARCH_NETWORK_PREFIX].152
OCS_PORT=8080
REPUBLIC_MANAGER_IP=[RESEARCH_NETWORK_PREFIX].152
REPUBLIC_MANAGER_PORT=10880

REPUBLIC_AGENT_NIC=eth3
REPUBLIC_AGENT_RATE_GBPS=10.0
REPUBLIC_AGENT_BATCH_SIZE=128
REPUBLIC_AGENT_NETMAP_QUEUE=1
REPUBLIC_AGENT_DATA_CHANNEL_SCHEDULING_POLICY=1
REPUBLIC_AGENT_DATA_CHANNEL_SCHEDULING_PRIORITY=99
REPUBLIC_AGENT_DATA_CHANNEL_CORE=1
REPUBLIC_AGENT_CTRL_CHANNEL_CORE=6
REPUBLIC_AGENT_API_CORE=6
REPUBLIC_AGENT_DATA_PAYLOAD_LEN=8822 # 8692 -> 8766

YARN_RESOURCE_MANAGER_IP=$2

CLUSTER_NODE_LIST=../parallel_hosts/
CLUSTER_NODE_FILE=$1

USERNAME=[SERVER_USERNAME]
USER_DIRECTORY=/home/${USERNAME}/
ROOT_DIRECTORY=/[ROOT_USERNAME]/
WORK_DIRECTORY=${USER_DIRECTORY}/github/
CONTROLLER_PATH=${WORK_DIRECTORY}./republic_manager/switch_controller/
MANAGER_PATH=${WORK_DIRECTORY}./republic_manager/
PROFILE_FILE='./.profile'

HADOOP_PATH=${WORK_DIRECTORY}./hadoop-2.7.4/

REPUBLIC_AGENT_PATH=${WORK_DIRECTORY}./republic_agent/
REPUBLIC_AGENT_C_PATH=${REPUBLIC_AGENT_PATH}./protocol/transceiver/

parallel-scp -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l [ROOT_USERNAME] ../config_files/hosts_50 /etc/hosts

# start TOR controller
ssh ${USERNAME}@${TOR_CONTROLLER_IP} "source ${PROFILE_FILE}; cd ${CONTROLLER_PATH}; screen -d -m ryu-manager ./quanta/ofdpa_broadcast.py ryu.app.ofctl_rest --wsapi-port ${TOR_PORT} --ofp-tcp-listen-port ${OFP_PORT}"
sleep 5

# start netmap
parallel-ssh -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l [ROOT_USERNAME] -i "screen -d -m ${WORK_DIRECTORY}./config_netmap.sh"
sleep 20

if [ "$3" == "-b" ]
then
    # start OCS controller
    ssh [SERVER_USERNAME]@${OCS_CONTROLLER_IP} "source ${PROFILE_FILE}; cd ${CONTROLLER_PATH}; screen -d -m /usr/bin/python ./glimmerglass/glimmerglass_controller.py"

    # start Republic Manager
    ssh [SERVER_USERNAME]@${REPUBLIC_MANAGER_IP} "source ${PROFILE_FILE}; cd ${MANAGER_PATH}; screen -d -m java -cp /home/[SERVER_USERNAME]/github/republic_manager/target/classes:/home/[SERVER_USERNAME]/.m2/repository/org/apache/thrift/libthrift/0.9.3/libthrift-0.9.3.jar:/home/[SERVER_USERNAME]/.m2/repository/org/slf4j/slf4j-api/1.7.12/slf4j-api-1.7.12.jar:/home/[SERVER_USERNAME]/.m2/repository/org/apache/httpcomponents/httpclient/4.5.2/httpclient-4.5.2.jar:/home/[SERVER_USERNAME]/.m2/repository/commons-logging/commons-logging/1.2/commons-logging-1.2.jar:/home/[SERVER_USERNAME]/.m2/repository/commons-codec/commons-codec/1.9/commons-codec-1.9.jar:/home/[SERVER_USERNAME]/.m2/repository/org/slf4j/slf4j-log4j12/1.7.16/slf4j-log4j12-1.7.16.jar:/home/[SERVER_USERNAME]/.m2/repository/log4j/log4j/1.2.17/log4j-1.2.17.jar:/home/[SERVER_USERNAME]/.m2/repository/com/googlecode/json-simple/json-simple/1.1/json-simple-1.1.jar:/home/[SERVER_USERNAME]/.m2/repository/org/apache/httpcomponents/httpcore/4.4.4/httpcore-4.4.4.jar:/home/[SERVER_USERNAME]/.m2/repository/org/jgroups/jgroups/3.1.0.Final/jgroups-3.1.0.Final.jar:/home/[SERVER_USERNAME]/.m2/repository/org/apache/commons/commons-lang3/3.4/commons-lang3-3.4.jar:/home/[SERVER_USERNAME]/.m2/repository/commons-cli/commons-cli/1.3.1/commons-cli-1.3.1.jar edu.rice.bold.server.BcdController -m ${REPUBLIC_MANAGER_PORT} -t ${TOR_PORT} -o ${OCS_PORT} -s -a -c -p"

 	if [ -z "$4" ]
	then
		echo no attempt
	else
		REPUBLIC_AGENT_ATTEMPT_RATE=$4
	    # start Republic Agents
	    parallel-ssh -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l [ROOT_USERNAME] -i "source ${PROFILE_FILE}; cd ${REPUBLIC_AGENT_C_PATH}; screen -d -m ./protocol -e ${REPUBLIC_AGENT_NIC} -o ${REPUBLIC_AGENT_NIC} -s ${REPUBLIC_AGENT_DATA_CHANNEL_SCHEDULING_POLICY} -S ${REPUBLIC_AGENT_DATA_CHANNEL_SCHEDULING_PRIORITY} -d ${REPUBLIC_AGENT_DATA_CHANNEL_CORE} -c ${REPUBLIC_AGENT_CTRL_CHANNEL_CORE} -i ${REPUBLIC_AGENT_API_CORE} -q ${REPUBLIC_AGENT_NETMAP_QUEUE} -r ${REPUBLIC_AGENT_RATE_GBPS} -b ${REPUBLIC_AGENT_BATCH_SIZE} -a ${REPUBLIC_AGENT_ATTEMPT_RATE} -j ${REPUBLIC_AGENT_DATA_PAYLOAD_LEN} -t 1>./.err 2>./.out"
	fi
fi

# start HDFS
parallel-ssh -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l [ROOT_USERNAME] -i "rm -rf ${HADOOP_PATH}/dfs";
ssh [ROOT_USERNAME]@${YARN_RESOURCE_MANAGER_IP} "source ${PROFILE_FILE}; hadoop namenode -format"
ssh [ROOT_USERNAME]@${YARN_RESOURCE_MANAGER_IP} "source ${PROFILE_FILE}; start-dfs.sh"

# start yarn
ssh [ROOT_USERNAME]@${YARN_RESOURCE_MANAGER_IP} "source ${PROFILE_FILE}; start-yarn.sh"
