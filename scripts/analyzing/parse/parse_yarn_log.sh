#!/usr/bin/env bash

YARN_CLUSTER_NAME=$1
YANR_MASTER_IP=$2
APPLICATION_INDEX_START=$3
APPLICATION_INDEX_END=$4

RUN_ID=${YARN_CLUSTER_NAME}_${APPLICATION_INDEX_START}-${APPLICATION_INDEX_END}
SUMMARY_OUTPUT_PATH=./log/${RUN_ID}/
OUTPUT_PATH=${SUMMARY_OUTPUT_PATH}./yarn/

USERNAME=[SERVER_USERNAME]
USER_DIRECTORY=/home/${USERNAME}/
WORK_DIRECTORY=${USER_DIRECTORY}/github/
HADOOP_PATH=${WORK_DIRECTORY}./hadoop-2.7.4/

mkdir -p ${OUTPUT_PATH}

#OUTPUT_PATH=./log/${YARN_CLUSTER_NAME}_${APPLICATION_INDEX_START}-${APPLICATION_INDEX_END}
scp [ROOT_USERNAME]@${YANR_MASTER_IP}:${HADOOP_PATH}/logs/yarn-[ROOT_USERNAME]-resourcemanager-${YANR_MASTER_IP}.log ${OUTPUT_PATH}
cat ${OUTPUT_PATH}/yarn-[ROOT_USERNAME]-resourcemanager-${YANR_MASTER_IP}.log | grep ${YARN_CLUSTER_NAME} | grep SUCCEEDED | cut -d" " -f5,8 | cut -d"," -f1,8,9 | tr ",=" " " | cut -d" " -f2,4,6 | awk '{print $1,($3-$2)/1000}' 1> ${OUTPUT_PATH}/${YARN_CLUSTER_NAME}_application.log
cat ${OUTPUT_PATH}/yarn-[ROOT_USERNAME]-resourcemanager-${YANR_MASTER_IP}.log | grep ${YARN_CLUSTER_NAME} | grep "assignedContainer application attempt" | cut -d" " -f 7,10,12,14 | tr ",:=" " " | cut -d" " -f 2,3,5 1> ${OUTPUT_PATH}/${YARN_CLUSTER_NAME}_container.log

# process log
for (( ai = $APPLICATION_INDEX_START; ai <= $APPLICATION_INDEX_END; ai ++ ))
do
    printf -v aiz "%04d" $ai
    cat ./${OUTPUT_PATH}/yarn-[ROOT_USERNAME]-resourcemanager-${YANR_MASTER_IP}.log | grep appattempt_${YARN_CLUSTER_NAME}_${aiz} | grep RMAppAttemptImpl | grep "LAUNCHED to RUNNING"
done > ${OUTPUT_PATH}/${RUN_ID}_RUNNING.log

for (( ai = $APPLICATION_INDEX_START; ai <= $APPLICATION_INDEX_END; ai ++ ))
do
    printf -v aiz "%04d" $ai
    cat ./${OUTPUT_PATH}/yarn-[ROOT_USERNAME]-resourcemanager-${YANR_MASTER_IP}.log | grep appattempt_${YARN_CLUSTER_NAME}_${aiz} | grep RMAppAttemptImpl | grep "RUNNING to FINAL_SAVING"
done > ${OUTPUT_PATH}/${RUN_ID}_FINAL_SAVING.log

python ./parse_yarn_log_app_runtime.py ${YARN_CLUSTER_NAME} ${APPLICATION_INDEX_START} ${APPLICATION_INDEX_END}