import pprint
import matplotlib.pyplot as plt
import os
import numpy as np

experiment_entries_l = [
    # (8, {"Repu": [("1512379483569", 1, 176), ],
    #      "Torr": [("1512397546318", 1, 176), ],
    #      "Http": [("1512404528613", 1, 176), ], }),
    (10, {"Repu": [("1512464414229", 1, 176), ("1512515004478", 1, 16), ],
          "Torr": [("1512482685448", 1, 176), ("1512530331790", 1, 16), ],
          "Http": [("1512489051950", 1, 176), ("1512533812367", 1, 16), ], }),
    # (14, {"Repu": [("", 1, 176), ],
    #       "Torr": [("", 1, 176), ],
    #       "Http": [("", 1, 176), ], }),
    # (22, {"Repu": [("", 1, 176), ],
    #       "Torr": [("", 1, 176), ],
    #       "Http": [("", 1, 176), ], }),
]

protocol_map = {
    'Bold': 'Republic',
    'Torrent': 'Torrent',
    'Http': 'Http'
}

color_l = ['indigo', 'lightcoral', 'navajowhite']
fontsize_ = 11  # color_l = ['black', 'indigo', 'salmon', 'burlywood', 'purple', 'red', 'green', 'grey', 'y']
linestyle_l = ['-', '--', '-.', ':']


def create_results(apptype_l=["tpch", 'ml']):
    results_d = {}  # {application: {protocol:[]}}
    for apptype_i in apptype_l:
        if apptype_i == 'tpch':
            for app_i in range(1, 23):
                results_d[apptype_i + '-' + str(app_i)] = {"Republic": [], "Torrent": [], "Http": []}
        elif apptype_i == 'ml':
            for app_i in ['word2vec', 'lda']:
                results_d[app_i] = {"Republic": [], "Torrent": [], "Http": []}
    return results_d


def draw_relative(results_d, num_executors):
    width = 1.0 / (0.5 + 3)  # the width of the bars
    fig, ax = plt.subplots(figsize=(15, 2))
    appname_l = ["tpch-%d" % idx for idx in range(1, 23)] + ["lda"]
    ind = np.arange(len(appname_l))

    ax2 = ax.twinx()
    appname_l_large = ['word2vec']
    ind_large = np.arange(len(appname_l), len(appname_l) + 1)

    ind_all = np.arange(len(appname_l + appname_l_large))
    print ind, ind_large

    idx = 0
    protocol_l = ['Republic', 'Torrent', 'Http']
    rect_l = []
    for protocol in protocol_l:
        republic_mean = []
        republic_std = []
        for appname in appname_l:
            republic_mean.append(np.mean(results_d[appname][protocol]))
            republic_std.append(np.std(results_d[appname][protocol]))
        republic_rects = ax.bar(ind + idx * width, republic_mean, 0.9 * width, color=color_l[idx],
                                yerr=republic_std,
                                edgecolor='black')
        rect_l.append(republic_rects)

        republic_mean_large = []
        republic_std_large = []
        for appname in appname_l_large:
            republic_mean_large.append(np.mean(results_d[appname][protocol]))
            republic_std_large.append(np.std(results_d[appname][protocol]))
        republic_rects_large = ax2.bar(ind_large + idx * width, republic_mean_large, 0.9 * width,
                                       color=color_l[idx],
                                       yerr=republic_std_large,
                                       edgecolor='black')

        idx += 1

    # add some text for labels, title and axes ticks
    # ax.set_title('Scores by group and gender')
    ax.set_xlim([-0.5, len(ind_all)])
    ax.set_ylabel('application running time (sec)')
    ax.set_xticks(ind_all + 2.0 * width / 2)
    ax.set_xticklabels(appname_l + appname_l_large, rotation='16')

    ax.legend([rect[0] for rect in rect_l], protocol_l, loc='upper center')
    plt.subplots_adjust(left=0.05, bottom=0.18, right=0.95, top=0.98, wspace=0, hspace=0)

    def autolabel(rects, idx):
        """
        Attach a text label above each bar displaying its height
        """
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + 0.03 + rect.get_width() / 2., 20 + height if height < 200 else height - 130,
                    '%0.1f' % (height),
                    ha='center', va='bottom', rotation='86', fontsize=10,
                    color='w' if idx == 0 and height > 200 else 'k')

    idx = 0
    for rect in rect_l:
        autolabel(rect, idx)
        idx += 1
    plt.savefig('/Users/[SERVER_USERNAME]/github/[SERVER_USERNAME]/phd_thesis/multicast_platform/paper/figures/%s_%d.eps' % (
        "application_running_time", num_executors),
                format='eps', dpi=300)

    plt.show()


for num_executors, runs_d in experiment_entries_l:
    results_d = create_results()
    # pprint.pprint(num_executors)
    # pprint.pprint(runs_d)
    appid_appname_l = []
    for protocol, runs_l in runs_d.iteritems():  # Repu [('1512379483569', 1, 176)]
        # print protocol, runs_l
        for run_yarn, run_start, run_end in runs_l:  # 1512379483569 1 176
            # print run_yarn, run_start, run_end
            run_id = "%s_%d-%d" % (run_yarn, run_start, run_end)
            run_path = "../parse/log/" + run_id + "/"
            # print run_path
            appid_appname_path = run_path + run_id + "_name.csv"
            appid_appname_d = {}  # {'application_1512379483569_0001': ['A:tpch-1', 'E:16', 'P:Bold', 'R:0'],}
            with open(appid_appname_path, 'r') as f:
                for line in f.readlines():
                    line_l = line.split(',')
                    appid_appname_d[line_l[0]] = line_l[1].split("_")
            # pprint.pprint(appid_appname_d)
            appid_appname_l.append(appid_appname_d)

            yarn_path = run_path + run_id + "_DURATION.csv"
            with open(yarn_path, 'r') as f:
                for exp in f.readlines():
                    exp_l = exp[:-1].split(',')
                    exp_ll = exp_l[0].split('_')
                    appid = 'application_%s_%s' % (exp_ll[1], exp_ll[2])
                    appname_parse = appid_appname_d[appid][0].split(':')[1]
                    protocol_parse = protocol_map[appid_appname_d[appid][2].split(':')[1]]
                    results_d[appname_parse][protocol_parse].append(float(exp_l[-1]))
    # pprint.pprint(results_d)
    draw_relative(results_d, num_executors)
