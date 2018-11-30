#!/usr/bin/env bash

CLUSTER_NODE_LIST=../parallel_hosts/
CLUSTER_NODE_FILE=$1

USERNAME=[SERVER_USERNAME]
USER_DIRECTORY=/home/${USERNAME}/
ROOT_DIRECTORY=/[ROOT_USERNAME]/
WORK_DIRECTORY=${USER_DIRECTORY}/github/
PROFILE_FILE='./.profile'
BASHRC_FILE='./.bashrc'

CONFIG_FILE_PATH='../config_files/'

HADOOP_PATH=${WORK_DIRECTORY}./hadoop-2.7.4/
HADOOP_FILE='hadoop-2.7.4.tar.gz'

TPCH_PATH=${WORK_DIRECTORY}./tpch-spark/
TPCH_DBGEN_PATH=${TPCH_PATH}./dbgen/
TOTAL_TABLE_SIZE=16

W2V_PATH=${WORK_DIRECTORY}./spark-perf/mllib-tests/

SPARK_PATH=${WORK_DIRECTORY}./spark_private/
SPARK_BRANCH_VERSION="v1.6.1_dev-republic"

LDA_DG_PATH=${WORK_DIRECTORY}./data_generator/
LDA_DG_FILE='data_generator.tgz'
N_GRAM=2
N_TOPIC=100
N_DOC=100000
LDA_START_EXECUTOR=10
LDA_END_EXECUTOR=22
LDA_INTERVAL_EXECUTOR=12


NETMAP_PATH=${WORK_DIRECTORY}./netmap/LINUX/
NETMAP_FILE=netmap.tgz

REPUBLIC_AGENT_PATH=${WORK_DIRECTORY}./republic_agent/
REPUBLIC_AGENT_C_PATH=${REPUBLIC_AGENT_PATH}./protocol/transceiver/
REPUBLIC_AGENT_BRANCH_VERSION="master"

# TOR_CONTROLLER_IP=[RESEARCH_NETWORK_PREFIX].152
# OCS_CONTROLLER_IP=[RESEARCH_NETWORK_PREFIX].152
REPUBLIC_MANAGER_IP=[RESEARCH_NETWORK_PREFIX].152
REPUBLIC_MANAGER_PATH=${WORK_DIRECTORY}./republic_manager/
REPUBLIC_MANAGER_BRANCH_VERSION="master"

DATETIME=$(date +%Y-%m-%d_%H:%M:%S)

# copy .bashrc
echo .bashrc
parallel-ssh -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l ${USERNAME} -i "cp ${BASHRC_FILE} ${BASHRC_FILE}_${USERNAME}_${DATETIME}"
parallel-ssh -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l [ROOT_USERNAME] -i "cp ${BASHRC_FILE} ${BASHRC_FILE}_rootuser_${DATETIME}"
parallel-scp -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l ${USERNAME} ${CONFIG_FILE_PATH}./.bashrc_user ${USER_DIRECTORY}${BASHRC_FILE}
parallel-scp -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l [ROOT_USERNAME] ${CONFIG_FILE_PATH}./.bashrc_rootuser ${ROOT_DIRECTORY}${BASHRC_FILE}

# copy .profile
echo .profile
parallel-ssh -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l ${USERNAME} -i "cp ${PROFILE_FILE} ${PROFILE_FILE}_${USERNAME}_${DATETIME}"
parallel-ssh -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l [ROOT_USERNAME] -i "cp ${PROFILE_FILE} ${PROFILE_FILE}_rootuser_${DATETIME}"
parallel-scp -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l ${USERNAME} ${CONFIG_FILE_PATH}./.profile_user ${USER_DIRECTORY}${PROFILE_FILE}
parallel-scp -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l [ROOT_USERNAME] ${CONFIG_FILE_PATH}./.profile_rootuser ${ROOT_DIRECTORY}${PROFILE_FILE}

# remove old files
echo remove old files
parallel-ssh -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l [ROOT_USERNAME] -i "source /[ROOT_USERNAME]/${PROFILE_FILE} && rm -rf ${WORK_DIRECTORY}"
parallel-ssh -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l ${USERNAME} -i "source ~/${PROFILE_FILE} && mkdir -p ${WORK_DIRECTORY}"

# copy yarn config
echo hadoop
parallel-ssh -t 0 -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l ${USERNAME} -i "source ~/${PROFILE_FILE}; cd ${WORK_DIRECTORY}; scp [RESEARCH_NETWORK_PREFIX].152:~/${HADOOP_FILE} ${WORK_DIRECTORY}; tar zxvf ${HADOOP_FILE}"
#echo ../hadoop_config/hadoop/ ${HADOOP_PATH}./etc/
parallel-scp -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l ${USERNAME} -r ../hadoop_config/hadoop/ ${HADOOP_PATH}./etc/
parallel-scp -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l ${USERNAME} -r ../hadoop_config/sbin/ ${HADOOP_PATH}/

# spark
parallel-ssh -t 0 -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l ${USERNAME} -i "source ${PROFILE_FILE}; cd ${WORK_DIRECTORY}; git clone \"https://sunxiaoye0116@github.com/sunxiaoye0116/spark_private.git\"; cd ${SPARK_PATH}; git checkout -b ${SPARK_BRANCH_VERSION} --track origin/${SPARK_BRANCH_VERSION}"
# compile spark
sleep 10
parallel-ssh -t 0 -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l ${USERNAME} -i "source ${PROFILE_FILE}; cd ${SPARK_PATH}; build/mvn -T 6 -Pyarn -Phadoop-2.6 -Dhadoop.version=2.7.4 -DskipTests package"
parallel-ssh -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l ${USERNAME} -i "source ${PROFILE_FILE}; mkdir -p ${SPARK_PATH}./tmp/spark-events"

# TPC-H
# download tpch-spark
parallel-ssh -t 0 -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l ${USERNAME} -i "source ${PROFILE_FILE}; cd ${WORK_DIRECTORY}; git clone https://github.com/sunxiaoye0116/tpch-spark.git"
# generate database tables
sleep 10
parallel-ssh -t 0 -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l ${USERNAME} -i "source ${PROFILE_FILE}; cd ${TPCH_DBGEN_PATH}; rm -rf *.tbl; make clean; make all; ./dbgen -f -q -s ${TOTAL_TABLE_SIZE}"
# compile
parallel-ssh -t 0 -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l ${USERNAME} -i "source ${PROFILE_FILE}; cd ${TPCH_PATH}; sbt clean; sbt package"

# word2vec
# download spark-perf
parallel-ssh -t 0 -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l ${USERNAME} -i "source ${PROFILE_FILE}; cd ${WORK_DIRECTORY}; git clone https://github.com/sunxiaoye0116/spark-perf.git"
sleep 10
# compile
parallel-ssh -t 0 -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l ${USERNAME} -i "source ${PROFILE_FILE}; cd ${W2V_PATH}; sbt clean; sbt/sbt assembly"

# LDA
parallel-ssh -t 0 -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l ${USERNAME} -i "source ${PROFILE_FILE}; ; scp [RESEARCH_NETWORK_PREFIX].152:~/${LDA_DG_FILE} ${WORK_DIRECTORY}; tar zxvf ${LDA_DG_FILE}; cd ${LDA_DG_PATH}; mvn install:install-file -Dfile=jsc.jar -DgroupId=uk.co.nildram -DartifactId=jsc -Dversion=1.0 -Dpackaging=jar; mvn package"
parallel-ssh -t 0 -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l ${USERNAME} -i "source ${PROFILE_FILE}; cd ${LDA_DG_PATH}; java -classpath ./target/classes:./jsc.jar edu.rice.republic.spark_data_generator.NGramDataGenerator ./corpus/input ${N_GRAM} 16923"
for ((i=${LDA_START_EXECUTOR};i<=${LDA_END_EXECUTOR};i+=${LDA_INTERVAL_EXECUTOR}))
do
parallel-ssh -t 0 -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l ${USERNAME} -i "source ${PROFILE_FILE}; cd ${LDA_DG_PATH}; java -classpath ./target/classes:./jsc.jar edu.rice.republic.spark_data_generator.DataGenerator lda ${i} ${N_DOC} ${N_TOPIC} ./corpus/input_${N_GRAM}_gram/ ./corpus/output_${N_GRAM}_gram/ spark"
done
# move data to spark
parallel-ssh -t 0 -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l ${USERNAME} -i "source ${PROFILE_FILE}; mv ${LDA_DG_PATH}./corpus/output_${N_GRAM}_gram/ ${SPARK_PATH}./data/"

## netmap
#echo netmap config
#parallel-ssh -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l ${USERNAME} -i "source ${PROFILE_FILE}; cd ${WORK_DIRECTORY}; scp [RESEARCH_NETWORK_PREFIX].152:~/${NETMAP_FILE} ${WORK_DIRECTORY}; tar zxvf ${NETMAP_FILE}; cd ${NETMAP_PATH}; make clean; ./configure --kernel-sources=/usr/src/linux-source-3.16 --drivers=ixgbe; make"
parallel-ssh -t 0 -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l ${USERNAME} -i "source ~/${PROFILE_FILE}; cd ${WORK_DIRECTORY}; scp [RESEARCH_NETWORK_PREFIX].152:~/netmap.tgz ${WORK_DIRECTORY}; tar zxvf ./netmap.tgz"
parallel-scp -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l ${USERNAME} ${CONFIG_FILE_PATH}./config_netmap.sh ${WORK_DIRECTORY}

# Republic Agent
echo republic agent
parallel-ssh -t 0 -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l ${USERNAME} -i "source ${PROFILE_FILE}; cd ${WORK_DIRECTORY}; git clone \"https://sunxiaoye0116@github.com/sunxiaoye0116/republic_agent.git\"; cd ${REPUBLIC_AGENT_PATH}; git checkout -b ${REPUBLIC_AGENT_BRANCH_VERSION} --track origin/${REPUBLIC_AGENT_BRANCH_VERSION}; cd ${REPUBLIC_AGENT_C_PATH}; make clean; make"
sleep 10
# copy zlog.conf
parallel-scp -h ${CLUSTER_NODE_LIST}${CLUSTER_NODE_FILE} -l ${USERNAME} ${CONFIG_FILE_PATH}./zlog_default.conf ${REPUBLIC_AGENT_C_PATH}

## Republic Manager
#ssh ${USERNAME}@${REPUBLIC_MANAGER_IP} "cp ${BASHRC_FILE} ${BASHRC_FILE}_${USERNAME}_${DATETIME}"
#scp ${CONFIG_FILE_PATH}./.bashrc_user [SERVER_USERNAME]@${REPUBLIC_MANAGER_IP}:~/${BASHRC_FILE}
#ssh ${USERNAME}@${REPUBLIC_MANAGER_IP}  "cp ${PROFILE_FILE} ${PROFILE_FILE}_${USERNAME}_${DATETIME}"
#scp ${CONFIG_FILE_PATH}./.profile_user [SERVER_USERNAME]@${REPUBLIC_MANAGER_IP}:~/${PROFILE_FILE}
#ssh ${USERNAME}@${REPUBLIC_MANAGER_IP} "source ${PROFILE_FILE} && cd ${WORK_DIRECTORY} && rm -rf *"
#ssh ${USERNAME}@${REPUBLIC_MANAGER_IP} "source ${PROFILE_FILE}; cd ${WORK_DIRECTORY}; git clone \"https://sunxiaoye0116@github.com/sunxiaoye0116/republic_manager.git\"; cd ${REPUBLIC_MANAGER_PATH}; git checkout -b ${REPUBLIC_MANAGER_BRANCH_VERSION} --track origin/${REPUBLIC_MANAGER_BRANCH_VERSION}; mvn package"

scp ../config_files/hosts_50 [ROOT_USERNAME]@${REPUBLIC_MANAGER_IP}/etc/hosts

# local
cp ${USER_DIRECTORY}${BASHRC_FILE} ${USER_DIRECTORY}${BASHRC_FILE}_${USERNAME}_${DATETIME}
cp ${CONFIG_FILE_PATH}./.bashrc_user ${USER_DIRECTORY}${BASHRC_FILE}
cp ${USER_DIRECTORY}${PROFILE_FILE} ${USER_DIRECTORY}${PROFILE_FILE}_${USERNAME}_${DATETIME}
cp ${CONFIG_FILE_PATH}./.profile_user ${USER_DIRECTORY}${PROFILE_FILE}
source ${USER_DIRECTORY}${BASHRC_FILE}
scp [RESEARCH_NETWORK_PREFIX].152:~/${HADOOP_FILE} ${WORK_DIRECTORY}; tar zxvf ${WORK_DIRECTORY}${HADOOP_FILE} -C ${WORK_DIRECTORY}
cp -r ../hadoop_config/hadoop/ ${HADOOP_PATH}./etc/
cp -r ../hadoop_config/sbin/ ${HADOOP_PATH}/
scp ../config_files/hosts_50 [ROOT_USERNAME]@localhost:/etc/hosts
