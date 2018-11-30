#!/usr/bin/env python
import time
import paramiko
import subprocess

protocol = ["Http"]
republic_attempt_sending = [0.003]

cluster_purpose_l = ['tpch']
num_executor = 10
num_repeat = 10
cluster_file = "parallel_hosts"
YARN_RESOURCE_MANAGER_NODE = 25
YARN_RESOURCE_MANAGER_IP = "[RESEARCH_NETWORK_PREFIX].%d" % (111 + YARN_RESOURCE_MANAGER_NODE,)

get_yarn_name = "sudo env \"PATH=$PATH\" yarn application -list -appStates ALL | grep _0001 | grep application | tr \"_\" \" \" | cut -d\" \" -f2"
check_num_finished_app = "sudo env \"PATH=$PATH\" yarn application -list -appStates FINISHED | grep Total | tr \":\" \" \" | cut -d\" \" -f12"

stop_cluster_format = "./stop_cluster.sh %s %s"
start_cluster_format = "./start_cluster.sh %s %s"
start_republic_cluster_format = start_cluster_format + " -b %f"
run_application_format = "./run_app.py %d %d %s %s %s"
parse_results_format = "./parse_all.sh %s 1 %d bold-node%03d ../../hadoop_config/hadoop/slaves"
parse_republic_results_format = parse_results_format + " -b"

run_dir_cmd = "cd /home/[SERVER_USERNAME]/github/republic_scripts/scripts/running/;"
parse_dir_cmd = "cd /home/[SERVER_USERNAME]/github/republic_scripts/scripts/analyzing/parse/;"

client_master = paramiko.SSHClient()
client_master.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client_master.connect(YARN_RESOURCE_MANAGER_IP, username='[ROOT_USERNAME]', password='[SERVER_PASSWORD]')

run_waiting_interval = 300
cmd_waiting_interval = 10
exp_waiting_timeout = 3 * 60 * 60

stop_cluster_cmd = stop_cluster_format % (cluster_file, YARN_RESOURCE_MANAGER_IP)
# print ">>>>>>$ " + run_dir_cmd + stop_cluster_cmd
# print subprocess.Popen(run_dir_cmd + stop_cluster_cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
time.sleep(cmd_waiting_interval)

# copy_config_cmd = copy_config_format % (cluster_file)
# print ">>>>>>$ " + run_dir_cmd + copy_config_cmd
# print subprocess.Popen(run_dir_cmd + copy_config_cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
time.sleep(cmd_waiting_interval)
for cluster_purpose in cluster_purpose_l:
    num_app = 22 if cluster_purpose == 'tpch' else 2
    for ptcl in protocol:
        run_application_cmd = run_application_format % (
            num_executor, num_repeat, cluster_purpose, ptcl, YARN_RESOURCE_MANAGER_IP)
        if ptcl == "Bold":
            for atmpt in republic_attempt_sending:
                start_cluster_cmd = start_republic_cluster_format % (cluster_file, YARN_RESOURCE_MANAGER_IP, atmpt)
                print ">>>>>>$ " + run_dir_cmd + stop_cluster_cmd
                print subprocess.Popen(run_dir_cmd + stop_cluster_cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
                time.sleep(cmd_waiting_interval)
                print ">>>>>>$ " + run_dir_cmd + start_cluster_cmd
                print subprocess.Popen(run_dir_cmd + start_cluster_cmd, shell=True,
                                       stdout=subprocess.PIPE).stdout.read()
                time.sleep(cmd_waiting_interval)
                print ">>>>>>$ " + run_dir_cmd + run_application_cmd
                subprocess.Popen(run_dir_cmd + run_application_cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
                time.sleep(cmd_waiting_interval)
                print ">>>>>>$ " + get_yarn_name
                stdin, stdout, stderr = client_master.exec_command(get_yarn_name)
                yarn_cluster_name = stdout.read()[:-1]
                print "<<<<<<$ yarn_cluster_name: " + yarn_cluster_name
                time.sleep(cmd_waiting_interval)
                is_running = True
                exp_timer = 0
                while is_running:
                    print ">>>>>>$ " + check_num_finished_app
                    stdin, stdout, stderr = client_master.exec_command(check_num_finished_app)
                    num_finished_app = int(stdout.read())
                    print "<<<<<<$ num_finished_app: " + str(num_finished_app) + " vs " + str(num_app * num_repeat)
                    if num_finished_app == num_app * num_repeat:
                        is_running = False
                        print "<<<<<<$ experiment finished..."
                        break
                    time.sleep(run_waiting_interval)
                    exp_timer += run_waiting_interval
                    if exp_timer > exp_waiting_timeout:
                        break

                parse_results_cmd = parse_republic_results_format % (
                    yarn_cluster_name, num_app * num_repeat, YARN_RESOURCE_MANAGER_NODE)
                print ">>>>>>$ " + parse_dir_cmd + parse_results_cmd
                print subprocess.Popen(parse_dir_cmd + parse_results_cmd, shell=True,
                                       stdout=subprocess.PIPE).stdout.read()
                time.sleep(cmd_waiting_interval)

        else:
            start_cluster_cmd = start_cluster_format % (cluster_file, YARN_RESOURCE_MANAGER_IP)
            print ">>>>>>$ " + run_dir_cmd + stop_cluster_cmd
            print subprocess.Popen(run_dir_cmd + stop_cluster_cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
            time.sleep(cmd_waiting_interval)
            print ">>>>>>$ " + run_dir_cmd + start_cluster_cmd
            print subprocess.Popen(run_dir_cmd + start_cluster_cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
            time.sleep(cmd_waiting_interval)
            print ">>>>>>$ " + run_dir_cmd + run_application_cmd
            subprocess.Popen(run_dir_cmd + run_application_cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
            time.sleep(cmd_waiting_interval)
            print ">>>>>>$ " + get_yarn_name
            stdin, stdout, stderr = client_master.exec_command(get_yarn_name)
            yarn_cluster_name = stdout.read()[:-1]
            print "<<<<<<$ yarn_cluster_name: " + yarn_cluster_name
            time.sleep(cmd_waiting_interval)
            is_running = True
            exp_timer = 0
            while is_running:
                print ">>>>>>$ " + check_num_finished_app
                stdin, stdout, stderr = client_master.exec_command(check_num_finished_app)
                num_finished_app = stdout.read()
                print num_finished_app
                num_finished_app = int(num_finished_app)
                print "<<<<<<$ num_finished_app: " + str(num_finished_app) + " vs " + str(num_app * num_repeat)
                if num_finished_app == num_app * num_repeat:
                    is_running = False
                    print "<<<<<<$ experiment finished..."
                    break
                time.sleep(run_waiting_interval)
                exp_timer += run_waiting_interval
                if exp_timer > exp_waiting_timeout:
                    break

            parse_results_cmd = parse_results_format % (
                yarn_cluster_name, num_app * num_repeat, YARN_RESOURCE_MANAGER_NODE)
            print ">>>>>>$ " + parse_dir_cmd + parse_results_cmd
            print subprocess.Popen(parse_dir_cmd + parse_results_cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
            time.sleep(cmd_waiting_interval)

print ">>>>>>$ " + run_dir_cmd + stop_cluster_cmd
print subprocess.Popen(run_dir_cmd + stop_cluster_cmd, shell=True, stdout=subprocess.PIPE).stdout.read()

client_master.close()
