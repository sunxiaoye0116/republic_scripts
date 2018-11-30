import pprint
import matplotlib.pyplot as plt
import os
import numpy as np

experiment_entries_l = {
    "tpch": [
        ('Republic', [(10, ("1512464414229", 1, 176)),
                      (22, ("1512613588556", 1, 176))]),
        # ('Torrent', [(10, ("1512482685448", 1, 176)),
        #              (22, ("1512589528420", 1, 176))]),
        # ('Http', [(10, ("1512489051950", 1, 176)),
        #           (22, ("1512601339634", 1, 176))]),
        ('Torrent', [(10, ("1512795376376", 1, 176)),
                     (22, ("1512839468326", 1, 176))]),
        ('Http', [(10, ("1512803872855", 1, 176)),
                  (22, ("1512851298253", 1, 176))]),
    ],
    "word2vec": [
        ('Republic', [(10, ("1512515004478", 1, 16)),
                      (22, ("1512627216791", 1, 16))]),
        # ('Torrent', [(10, ("1512530331790", 1, 16)),
        #              (22, ("1512578894665", 1, 16))]),
        # ('Http', [(10, ("1512533812367", 1, 16)),
        #           (22, ("1512582376567", 1, 16))]),
        ('Torrent', [(10, ("1512932713471", 1, 16)),
                     (22, ("1512874012631", 1, 16))]),
        ('Http', [(10, ("1512903660044", 1, 16)),
                  (22, ("1512867225488", 1, 16))]),
    ],
    "lda": [
        ('Republic', [(10, ("1512515004478", 1, 16)),
                      (22, ("1512627216791", 1, 16))]),
        # ('Torrent', [(10, ("1512530331790", 1, 16)),
        #              (22, ("1512578894665", 1, 16))]),
        # ('Http', [(10, ("1512533812367", 1, 16)),
        #           (22, ("1512582376567", 1, 16))]),
        ('Torrent', [(10, ("1512932713471", 1, 16)),
                     (22, ("1512874012631", 1, 16))]),
        ('Http', [(10, ("1512903660044", 1, 16)),
                  (22, ("1512867225488", 1, 16))]),
    ],
}

# normalize_torrent_map = {
#     'tpch': {10: 2794.6,
#              22: 2658.2,
#              },
#     'lda': {10: 121.427,
#             22: 118.584,
#             },
#     'word2vec': {10: 1368.218,
#                  22: 695.515,
#                  }
# }
#
# normalize_republic_map = {
#     'tpch': {10: 2794.6,
#              22: 2658.2,
#              },
#     'lda': {10: 139.8,
#             22: 187.7,
#             },
#     'word2vec': {10: 1379.4,
#                  22: 748.7,
#                  }
# }

protocol_map = {
    'Bold': 'Republic',
    'Torrent': 'Torrent',
    'Http': 'Http'
}

color_l = ['indigo', 'lightcoral', 'navajowhite']
linestyle_l = ['-', '--', '-.', ':']


def create_results(num_l=[10, 14, 22]):
    results_d = {}  # {executor: {protocol:[]}}
    for num_ in num_l:
        results_d[num_] = {"Republic": [], "Torrent": [], "Http": []}
    return results_d


def draw_relative(results_d, app_name, absolute=True):
    width = 1.0 / (0.5 + 3)  # the width of the bars
    fig, ax = plt.subplots(figsize=(2.8, 2.8))
    appname_l = [10, 22]
    ind = np.arange(len(appname_l))

    idx = 0
    protocol_l = ['Republic', 'Torrent', 'Http']
    rect_l = []
    for protocol in protocol_l:
        republic_mean = []
        republic_std = []
        for appname in appname_l:
            # print app_name, protocol
            normalize_l = [a / (1.0 if absolute else normalize_torrent_map[app_name][appname]) for a in
                           results_d[appname][protocol]]
            republic_mean.append(np.mean(normalize_l))
            republic_std.append(np.std(normalize_l))
        republic_rects = ax.bar(ind + idx * width, republic_mean, 0.9 * width, color=color_l[idx],
                                yerr=republic_std,
                                edgecolor='black')
        rect_l.append(republic_rects)

        idx += 1

    # add some text for labels, title and axes ticks
    # ax.set_title('Scores by group and gender')
    ax.set_xlim([-0.5, len(ind)])
    ax.set_ylabel('application running time (sec)')
    ax.set_xticks(ind + 2.0 * width / 2)
    ax.set_xticklabels(appname_l)
    ax.set_xlabel("number of executors")

    # ax.legend([rect[0] for rect in rect_l], protocol_l, loc='upper right')
    plt.subplots_adjust(left=0.25, bottom=0.15, right=0.99, top=0.99, wspace=0, hspace=0)

    def autolabel(rects, idx):
        """
        Attach a text label above each bar displaying its height
        """
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + 0.03 + rect.get_width() / 2., (height * 0.55) if absolute else (height - 0.4),
                    ('%0.1f' if absolute else '%0.3f') % (height),
                    ha='center', va='bottom', rotation='86', fontsize=11,
                    color='w' if idx == 0  else 'k')

    idx = 0
    for rect in rect_l:
        autolabel(rect, idx)
        idx += 1
    if not absolute:
        ax.set_ylim([0, 1.65])
    plt.savefig('/Users/[SERVER_USERNAME]/github/eugeneng/REPUBLIC/figures/%s_%s.eps' % (
        "application_running_time%s" % ("-abs" if absolute else "-rel"), app_name),
                format='eps', dpi=300)

    plt.show()


for app_name, protocol_run_l in experiment_entries_l.iteritems():
    results_d = create_results([10, 22])
    # pprint.pprint(results_d)
    # pprint.pprint(app_name)
    # pprint.pprint(protocol_run_l)
    appid_appname_l = []
    for protocol, runs_l in protocol_run_l:  # Repu [('1512379483569', 1, 176)]
        # print protocol, runs_l
        for num_, (run_yarn, run_start, run_end) in runs_l:  # 1512379483569 1 176
            # print num_, run_yarn, run_start, run_end
            run_id = "%s_%d-%d" % (run_yarn, run_start, run_end)
            run_path = "../parse/log/" + run_id + "/"
            # print run_path
            appid_appname_path = run_path + run_id + "_name.csv"
            # print appid_appname_path
            appid_appname_d = {}  # {'application_1512379483569_0001': ['A:tpch-1', 'E:16', 'P:Bold', 'R:0'],}
            with open(appid_appname_path, 'r') as f:
                for line in f.readlines():
                    line_l = line.split(',')
                    appid_appname_d[line_l[0]] = line_l[1].split("_")
            # pprint.pprint(appid_appname_d)
            appid_appname_l.append(appid_appname_d)

            yarn_path = run_path + run_id + "_DURATION.csv"
            tmp_results_d = {idx: 0.0 for idx in range(8)}

            with open(yarn_path, 'r') as f:
                for exp in f.readlines():
                    exp_l = exp[:-1].split(',')
                    exp_ll = exp_l[0].split('_')
                    appid = 'application_%s_%s' % (exp_ll[1], exp_ll[2])
                    app_run_idx = appid_appname_d[appid][-1].split(':')[1]
                    appname_parse = appid_appname_d[appid][0].split(':')[1]
                    protocol_parse = protocol_map[appid_appname_d[appid][2].split(':')[1]]
                    assert protocol_parse[:1] == protocol[:1]
                    # print app_run_idx, app_name, appname_parse, protocol_parse, protocol
                    if app_name == 'tpch':
                        tmp_results_d[int(app_run_idx)] += (float(exp_l[-1]))
                    elif app_name == appname_parse:
                        results_d[num_][protocol_parse].append(float(exp_l[-1]))
            if app_name == 'tpch':
                results_d[num_][protocol] = list(tmp_results_d.values())
    # pprint.pprint(results_d)
    draw_relative(results_d, app_name)
