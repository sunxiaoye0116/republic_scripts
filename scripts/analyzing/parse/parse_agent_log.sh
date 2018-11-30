#!/usr/bin/env bash

YARN_CLUSTER_NAME=$1
SLAVE_FILENAME=$2
APPLICATION_INDEX_START=$3
APPLICATION_INDEX_END=$4

# collect log
RUN_ID=${YARN_CLUSTER_NAME}_${APPLICATION_INDEX_START}-${APPLICATION_INDEX_END}
SUMMARY_OUTPUT_PATH=./log/${RUN_ID}/
OUTPUT_PATH=${SUMMARY_OUTPUT_PATH}./republic/
CONCISE_OUTPUT_PATH=${SUMMARY_OUTPUT_PATH}./republic/concise/

echo ${RUN_ID}
echo ${SUMMARY_OUTPUT_PATH}
echo ${OUTPUT_PATH}

mkdir -p ${OUTPUT_PATH}
mkdir -p ${CONCISE_OUTPUT_PATH}

while read slv;
do
    initial="$(echo $slv | head -c 1)"
    if [ "$initial" != "#" ]
    then
        echo retrive log from node: ${slv}
        for (( ai = $APPLICATION_INDEX_START; ai <= $APPLICATION_INDEX_END; ai ++ ))
        do
            printf -v aiz "%04d" $ai
            scp ${slv}:~/github/republic_agent/protocol/transceiver/log/application_${YARN_CLUSTER_NAME}_${aiz}.log ${OUTPUT_PATH}/application_${YARN_CLUSTER_NAME}_${aiz}_${slv}.log
        done
    fi
done < ${SLAVE_FILENAME};

# process log
for (( ai = $APPLICATION_INDEX_START; ai <= $APPLICATION_INDEX_END; ai ++ ))
do
    printf -v aiz "%04d" $ai
    # echo "=        ============\>" ./application_${YARN_CLUSTER_NAME}_${aiz}
    for lfn in ${OUTPUT_PATH}/application_${YARN_CLUSTER_NAME}_${aiz}*.log
    do
        # echo "=                ==\>" $lfn
        cat $lfn | grep "RECV" | tr ":,[]|()" " " | tr "\t" "," | tr " " "," | sed 's/,,/,/g' | sed 's/,,/,/g' | sed 's/,,/,/g'
    done
done > ${SUMMARY_OUTPUT_PATH}/${RUN_ID}_receiver.csv

for (( ai = $APPLICATION_INDEX_START; ai <= $APPLICATION_INDEX_END; ai ++ ))
do
    printf -v aiz "%04d" $ai
    for lfn in ${OUTPUT_PATH}/application_${YARN_CLUSTER_NAME}_${aiz}*.log
    do
        cat $lfn | grep "RECV" | tr ":,[]|()" " " | tr "\t" "," | tr " " "," | sed 's/,,/,/g' | sed 's/,,/,/g' | sed 's/,,/,/g'
    done > ${CONCISE_OUTPUT_PATH}/application_${YARN_CLUSTER_NAME}_${aiz}_receiver.csv
done


for (( ai = $APPLICATION_INDEX_START; ai <= $APPLICATION_INDEX_END; ai ++ ))
do
    printf -v aiz "%04d" $ai
    for lfn in ${OUTPUT_PATH}/application_${YARN_CLUSTER_NAME}_${aiz}*.log
    do
        cat $lfn | grep "SEND" | tr ":,[]|()" " " | tr "\t" "," | tr " " "," | sed 's/,,/,/g' | sed 's/,,/,/g' | sed 's/,,/,/g'
    done
done > ${SUMMARY_OUTPUT_PATH}/${RUN_ID}_sender.csv

for (( ai = $APPLICATION_INDEX_START; ai <= $APPLICATION_INDEX_END; ai ++ ))
do
    printf -v aiz "%04d" $ai
    for lfn in ${OUTPUT_PATH}/application_${YARN_CLUSTER_NAME}_${aiz}*.log
    do
        cat $lfn | grep "SEND" | tr ":,[]|()" " " | tr "\t" "," | tr " " "," | sed 's/,,/,/g' | sed 's/,,/,/g' | sed 's/,,/,/g'
    done > ${CONCISE_OUTPUT_PATH}/application_${YARN_CLUSTER_NAME}_${aiz}_sender.csv
done