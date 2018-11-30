#!/usr/bin/env bash

YARN_CLUSTER_NAME=$1
APPLICATION_INDEX_START=$2
APPLICATION_INDEX_END=$3
YARN_MASTER_IP=$4
SLAVE_FILENAME=$5

./parse_spark_log.sh ${YARN_CLUSTER_NAME} ${APPLICATION_INDEX_START} ${APPLICATION_INDEX_END}
if [ "$6" == "-b" ]
then
    ./parse_agent_log.sh ${YARN_CLUSTER_NAME} ${SLAVE_FILENAME} ${APPLICATION_INDEX_START} ${APPLICATION_INDEX_END}
fi
./parse_yarn_log.sh ${YARN_CLUSTER_NAME} ${YARN_MASTER_IP} ${APPLICATION_INDEX_START} ${APPLICATION_INDEX_END}
