#!/usr/bin/env bash

YARN_CLUSTER_NAME=$1
APPLICATION_INDEX_START=$2
APPLICATION_INDEX_END=$3

# collect spark log
#OUTPUT_PATH=./log/${YARN_CLUSTER_NAME}_${APPLICATION_INDEX_START}-${APPLICATION_INDEX_END}
RUN_ID=${YARN_CLUSTER_NAME}_${APPLICATION_INDEX_START}-${APPLICATION_INDEX_END}
SUMMARY_OUTPUT_PATH=./log/${RUN_ID}/
OUTPUT_PATH=${SUMMARY_OUTPUT_PATH}./spark/

mkdir -p ./log
#rm -rf ${SUMMARY_OUTPUT_PATH}
mkdir -p ${OUTPUT_PATH}
for (( ai = $APPLICATION_INDEX_START; ai <= $APPLICATION_INDEX_END; ai ++ ))
do
    printf -v aiz "%04d" $ai
    (sleep 1; echo [SERVER_PASSWORD];) | sudo env "PATH=$PATH" yarn logs -applicationId application_${YARN_CLUSTER_NAME}_${aiz} -appOwner [ROOT_USERNAME] 1> ${OUTPUT_PATH}/application_${YARN_CLUSTER_NAME}_${aiz}_.log
    cp ${OUTPUT_PATH}/application_${YARN_CLUSTER_NAME}_${aiz}_.log ${OUTPUT_PATH}/application_${YARN_CLUSTER_NAME}_${aiz}.log
    rm ${OUTPUT_PATH}/application_${YARN_CLUSTER_NAME}_${aiz}_.log
done

# process log
for (( ai = $APPLICATION_INDEX_START; ai <= $APPLICATION_INDEX_END; ai ++ ))
do
    printf -v aiz "%04d" $ai
    cat ${OUTPUT_PATH}/application_${YARN_CLUSTER_NAME}_${aiz}.log | grep oadcast | grep -v piece | grep 'Broadcast.read()' > ${OUTPUT_PATH}/application_${YARN_CLUSTER_NAME}_${aiz}_brt_time.log # | cut -d" " -f 9
    cat ${OUTPUT_PATH}/application_${YARN_CLUSTER_NAME}_${aiz}.log | grep oadcast | grep -v piece | grep 'Block broadcast_' | grep -v '2017/' > ${OUTPUT_PATH}/application_${YARN_CLUSTER_NAME}_${aiz}_brt_size.log # | cut -d" " -f 9
# for brt in $(cat ${OUTPUT_PATH}/application_${YARN_CLUSTER_NAME}_${aiz}.log | grep oadcast | grep -v piece | grep 'Broadcast.read()' | cut -d" " -f 9)
# do
#     echo $brt,
# done > ${OUTPUT_PATH}/application_${YARN_CLUSTER_NAME}_${aiz}.csv
done

# # merge brt
# cat ${OUTPUT_PATH}/application_${YARN_CLUSTER_NAME}_0*.csv 1> ${SUMMARY_OUTPUT_PATH}/${RUN_ID}_brt.csv
# sort -g ${SUMMARY_OUTPUT_PATH}/${RUN_ID}_brt.csv -o ${SUMMARY_OUTPUT_PATH}/${RUN_ID}_brt_sort.csv

# #create cdf
# n_brt=$(cat ${SUMMARY_OUTPUT_PATH}/${RUN_ID}_brt.csv | wc -l)
# index=1
# while read brt;
# do
#     b=$(echo $index/$n_brt);
#     a=$(bc -l <<< $b);
#     echo $brt $a, 1>> ${SUMMARY_OUTPUT_PATH}/${RUN_ID}_brt_cdf.csv;
#     let "index+=1"
# done < ${SUMMARY_OUTPUT_PATH}/${RUN_ID}_brt_sort.csv;
