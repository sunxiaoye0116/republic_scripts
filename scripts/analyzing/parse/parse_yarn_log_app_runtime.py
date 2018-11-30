import sys
import datetime

YARN_CLUSTER_NAME = sys.argv[1]
APPLICATION_INDEX_START = sys.argv[2]
APPLICATION_INDEX_END = sys.argv[3]

RUN_ID = YARN_CLUSTER_NAME + "_" + APPLICATION_INDEX_START + "-" + APPLICATION_INDEX_END
SUMMARY_OUTPUT_PATH = "./log/" + RUN_ID + "/"
OUTPUT_PATH = SUMMARY_OUTPUT_PATH + "/yarn/"

FILENAME_FINAL = OUTPUT_PATH + "/" + RUN_ID + "_FINAL_SAVING.log"
FILENAME_RUNNING = OUTPUT_PATH + "/" + RUN_ID + "_RUNNING.log"
# print FILENAME_FINAL

time_start_ending_duration = {}

with open(FILENAME_FINAL, 'r') as f:
    for r in f.readlines():
        logline = r.split()
        timestamp = logline[0] + " " + logline[1]
        time_start_ending_duration[logline[4]] = [timestamp]

        # (dt_offset - ).total_seconds()

with open(FILENAME_RUNNING, 'r') as f:
    for r in f.readlines():
        logline = r.split()
        timestamp = logline[0] + " " + logline[1]

        duration = (
            datetime.datetime.strptime(time_start_ending_duration[logline[4]][0] + "000", "%Y-%m-%d %H:%M:%S,%f") -
            datetime.datetime.strptime(timestamp + "000", "%Y-%m-%d %H:%M:%S,%f")).total_seconds()

        time_start_ending_duration[logline[4]].append(timestamp)
        time_start_ending_duration[logline[4]].append(duration)

FILENAME_OUTPUT = SUMMARY_OUTPUT_PATH + "/" + RUN_ID + "_DURATION.csv"
with open(FILENAME_OUTPUT, 'w') as f:
    for k, v in time_start_ending_duration.iteritems():
        f.write(k + "," + str(v[0]) + "," + str(v[1]) + ", " + str(v[2]) + "\n")
