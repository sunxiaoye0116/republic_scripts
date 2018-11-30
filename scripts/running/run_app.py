#!/usr/bin/env python

import paramiko
import time
import os
import sys

app_executor = int(sys.argv[1])
app_repeat = int(sys.argv[2])
cluster_name = sys.argv[3]
cluster_multicast = sys.argv[4]
YARN_RESOURCE_MANAGER_IP = sys.argv[5]

APP_INTERVAL_SEC = 10

if cluster_name == "tpch":
    app_list = [(protocol, 'tpch', run_id, query_id)
                for protocol in [cluster_multicast]
                for run_id in range(app_repeat)
                for query_id in range(1, 23)]
elif cluster_name == "ml":
    app_list = [(protocol, apptype, run_id)
                for protocol in [cluster_multicast]
                for run_id in range(app_repeat)
                for apptype in ['word2vec', 'lda']]

# spark config
DRIVER_CORES = 4
DRIVER_MEMORY = 88
EXECUTOR_CORES = 2
EXECUTOR_MEMORY = 44

# ml config
ITERATION = 10

# tpc-h config
app_tpch_scale = 16
app_tpch_source = "local"

app_parallel = app_executor * EXECUTOR_CORES

# ENV
# DRIVER_EXTRAJAVAOPTIONS = "-Dlog4j.configuration=log4j.properties -Dspark.executor.extraJavaOptions=-Dlog4j.configuration=log4j.properties"
# -Dspark.driver.extraJavaOptions=-Dlog4j.configuration=log4j.properties
# -Dspark.executor.extraJavaOptions=-Dlog4j.configuration=log4j.properties

# spark config
STORAGE_MEMORYFRACTION = "0.66"
SERIALIZER = "org.apache.spark.serializer.JavaSerializer"
SHUFFLE_MANAGER = "SORT"
LOCALITY_WAIT = 60000000
EXECUTOR_HEARTBEATINTERVAL = 50
FORMAT_BROADCAST_FACTORY = "org.apache.spark.broadcast.%sBroadcastFactory"

FORMAT_APP_NAME = "A:%s_E:%s_P:%s_R:%s"
FORMAT_APP_TPCH_NAME = "A:%s-%s_E:%s_P:%s_R:%s"
FORMAT_APP_PATH = "./A:%s/E:%s/P:%s/R:%s/"
FORMAT_APP_TPCH_PATH = "./A:%s-%s/E:%s/P:%s/R:%s/"

WORK_DIRECTORY = '/home/[SERVER_USERNAME]/github/'

HADOOP_PATH = WORK_DIRECTORY + './hadoop-2.7.4/'
HADOOP_FORMAT_STD_DIR = HADOOP_PATH + "./%s/%s"
HADOOP_FORMAT_STD_OUTPUT = HADOOP_PATH + "./%s/%s.%s"

SPARK_PATH = WORK_DIRECTORY + './spark_private/'
SPARK_SUBMIT_COMMAND = SPARK_PATH + './bin/spark-submit'
SPARK_MASTER = "yarn-cluster"

TPCH_PATH = WORK_DIRECTORY + './tpch-spark/'
LDA_PATH = SPARK_PATH
W2V_PATH = WORK_DIRECTORY + './spark-perf/'

CLASS_APP_DICT = {}
JAR_APP_DICT = {}
FORMAT_ARG_APP_DICT = {}
PACKAGE_APP_DICT = {}

# ========== word2vec ==========
CLASS_APP_DICT['word2vec'] = "mllib.perf.TestRunner"
JAR_APP_DICT['word2vec'] = W2V_PATH + "./mllib-tests/target/mllib-perf-tests-assembly.jar"
FORMAT_ARG_APP_DICT[
    'word2vec'] = "word2vec --num-trials=1 --inter-trial-wait=3 --num-partitions=%d --random-seed=%d --num-sentences=4000000 --num-words=210000 --vector-size=300 --num-iterations=%d --min-count=1"

# ========== lda ==========
CLASS_APP_DICT['lda'] = "org.apache.spark.examples.Lda"
JAR_APP_DICT['lda'] = LDA_PATH + "./examples/target/scala-2.10/spark-examples-1.6.1-hadoop2.7.4.jar"
FORMAT_ARG_APP_DICT['lda'] = LDA_PATH + "./data/output_2_gram/lda/WORD_IN_DOC_%d.tbl 918726 100 %d"

# ========== tpc-h ==========
CLASS_APP_DICT['tpch'] = "main.scala.TpchQuery"
JAR_APP_DICT['tpch'] = TPCH_PATH + "./target/scala-2.10/spark-tpc-h-queries_2.10-1.0.jar"
FORMAT_ARG_APP_DICT['tpch'] = "%d %d %d %s %d %s"
PACKAGE_APP_DICT['tpch'] = "com.databricks:spark-csv_2.10:1.2.0"

BROADCAST_COMPRESS = "false"
SQL_AUTOBROADCASTJOINTHRESHOLD = 10485760
MAX_RESULT_SIZE=8

# ==========================
yarn_app_idx = 0
yarn_cluster_dir_format = "../analyzing/parse/log/%s_%d-%d/"
yarn_cluster_format = yarn_cluster_dir_format + "%s_%d-%d_name.csv"
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(YARN_RESOURCE_MANAGER_IP, username='[ROOT_USERNAME]', password='[SERVER_PASSWORD]')

for app in app_list:
    app_protocol = app[0]
    app_type = app[1]
    app_index = app[2]

    app_name = ""
    app_path = ""
    if app_type == 'lda' or app_type == 'word2vec':
        app_name = FORMAT_APP_NAME % (app_type, app_parallel, app_protocol, app_index)
        app_path = FORMAT_APP_PATH % (app_type, app_parallel, app_protocol, app_index)
    elif app_type == 'tpch':
        app_tpch_query = app[3]
        app_name = FORMAT_APP_TPCH_NAME % (app_type, app_tpch_query, app_parallel, app_protocol, app_index)
        app_path = FORMAT_APP_TPCH_PATH % (app_type, app_tpch_query, app_parallel, app_protocol, app_index)

    cmd_class = CLASS_APP_DICT[app_type]
    cmd_master = SPARK_MASTER

    format_cmd_conf_list = ["executor.heartbeatInterval=%d",
                            "storage.memoryFraction=%s",
                            "serializer=%s",
                            "shuffle.manager=%s",
                            "locality.wait=%d",
                            "broadcast.factory=" + FORMAT_BROADCAST_FACTORY,
                            "cores.max=%d",
                            "driver.cores=%d",
                            "driver.memory=%dg",
                            "executor.instances=%d",
                            "executor.cores=%d",
                            "executor.memory=%dg",
                            "app.name=%s",
                            "broadcast.compress=%s",
                            "driver.maxResultSize=%dg"]

    cmd_conf_arg_list = [EXECUTOR_HEARTBEATINTERVAL,
                         STORAGE_MEMORYFRACTION,
                         SERIALIZER,
                         SHUFFLE_MANAGER,
                         LOCALITY_WAIT,
                         app_protocol,
                         app_parallel,
                         DRIVER_CORES,
                         DRIVER_MEMORY,
                         app_executor,
                         EXECUTOR_CORES,
                         EXECUTOR_MEMORY,
                         app_name,
                         BROADCAST_COMPRESS,
                         MAX_RESULT_SIZE]

    cmd_conf_list = ['--conf spark.' + format_cmd_conf_list[idx] % cmd_conf_arg_list[idx] for idx in
                     range(0, len(format_cmd_conf_list))]

    if app_type == 'tpch':
        format_cmd_conf_tpch_list = ["default.parallelism=%d",
                                     "sql.shuffle.partitions=%d",
                                     "sql.autoBroadcastJoinThreshold=%d",
                                     "sql.broadcastTimeout=%d"]
        cmd_conf_arg_tpch_list = [app_parallel,
                                  app_parallel,
                                  SQL_AUTOBROADCASTJOINTHRESHOLD,
                                  3000]
        cmd_conf_list += ['--conf spark.' + format_cmd_conf_tpch_list[idx] % cmd_conf_arg_tpch_list[idx] for idx in
                          range(0, len(format_cmd_conf_tpch_list))]

    cmd_conf = ' '.join(cmd_conf_list)

    cmd_jar = JAR_APP_DICT[app_type]
    cmd_path = HADOOP_FORMAT_STD_DIR % ("logs_master", app_path)
    cmd_err = HADOOP_FORMAT_STD_OUTPUT % ("logs_master", app_path, "err")
    cmd_out = HADOOP_FORMAT_STD_OUTPUT % ("logs_master", app_path, "out")

    FORMAT_SPARK_SUBMIT_COMMAND = "screen -d -m " + SPARK_SUBMIT_COMMAND
    cmd_args = ""
    if app_type == 'lda':
        cmd_args += FORMAT_ARG_APP_DICT[app_type] % (app_parallel, ITERATION)
    elif app_type == 'word2vec':
        cmd_args += FORMAT_ARG_APP_DICT[app_type] % (app_parallel, 5, ITERATION)
    elif app_type == 'tpch':
        cmd_args += FORMAT_ARG_APP_DICT[app_type] % (
            app_tpch_query, app_tpch_scale, app_executor, app_protocol, app_index, app_tpch_source)
        FORMAT_SPARK_SUBMIT_COMMAND += " --packages %s" % (PACKAGE_APP_DICT[app_type])

    FORMAT_SPARK_SUBMIT_COMMAND += " --class %s --master %s %s %s %s 1>%s 2>%s" % (
        cmd_class, cmd_master, cmd_conf, cmd_jar, cmd_args, cmd_err, cmd_out)

    print 'mkdir -p ' + cmd_path
    stdin, stdout, stderr = client.exec_command('mkdir -p ' + cmd_path)
    time.sleep(APP_INTERVAL_SEC / 2)
    print FORMAT_SPARK_SUBMIT_COMMAND
    stdin, stdout, stderr = client.exec_command(FORMAT_SPARK_SUBMIT_COMMAND)
    time.sleep(APP_INTERVAL_SEC / 2)
client.close()

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(YARN_RESOURCE_MANAGER_IP, username='[ROOT_USERNAME]', password='[SERVER_PASSWORD]')
# check_cluster_name_cmd = "yarn application -list -appStates ALL | grep _0001 | grep application | tr \"_\" \" \" | cut -d\" \" -f2"
check_cluster_name_cmd = "yarn application -list -appStates ALL"
stdin, stdout, stderr = client.exec_command(check_cluster_name_cmd)
applications = []
for application_line in stdout.readlines():
    if 'application' in application_line and 'Total' not in application_line:
        application_line_split = application_line.split('\t')
        applications.append([application_line_split[0], application_line_split[1]])
client.close()
yarn_cluster_name = applications[0][0].split('_')[1]
applications.sort(key=lambda x: x[0])
print yarn_cluster_name
yarn_cluster_dir = yarn_cluster_dir_format % (yarn_cluster_name, 1, len(applications))
if not os.path.exists(yarn_cluster_dir):
    os.makedirs(yarn_cluster_dir)
with open(yarn_cluster_format % (
        yarn_cluster_name, 1, len(applications),
        yarn_cluster_name, 1, len(applications)), 'w') as f:
    for a, b in applications:
        f.write(a + ',' + b + ',\n')
