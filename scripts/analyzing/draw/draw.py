import pprint
import matplotlib.pyplot as plt
import os

experiment_entries_l = [
    # ("1512613588556", 1, 176, "Republic|executor-22|apptype-tpch|circuit-keep|$r_{a}$=0.003|line-last"),
    # ("1512627216791", 1, 16, "Republic|executor-22|apptype-ml|circuit-keep|$r_{a}$=0.003|line-last1"),
    # ("", 1, 1, "Republic|executor-14|apptype-tpch|circuit-keep|$r_{a}$=0.003|line-last"),
    # ("", 1, 1, "Republic|executor-14|apptype-ml|circuit-keep|$r_{a}$=0.003|line-last"),
    # ("1512464414229", 1, 176, "Republic|executor-10|apptype-tpch|circuit-keep|$r_{a}$=0.003|line-last"),
    # ("1512515004478", 1, 16, "Republic|executor-10|apptype-ml|circuit-keep|$r_{a}$=0.003|line-last"),

    # ("1512589528420", 1, 176, "Torrent|executor-22|apptype-tpch|"),
    # ("1512578894665", 1, 16, "Torrent|executor-22|apptype-ml|"),
    # ("", 1, 1, "Torrent|executor-14|apptype-tpch|"),
    # ("", 1, 1, "Torrent|executor-14|apptype-ml|"),
    # ("1512482685448", 1, 176, "Torrent|executor-10|apptype-tpch|"),
    # ("1512530331790", 1, 16, "Torrent|executor-10|apptype-ml|"),

    # ("1512601339634", 1, 176, "Http|executor-22|apptype-tpch|"),
    # ("1512582376567", 1, 16, "Http|executor-22|apptype-ml|"),
    # ("", 1, 1, "Http|executor-14|apptype-tpch|"),
    # ("", 1, 1, "Http|executor-14|apptype-ml|"),
    # ("1512489051950", 1, 176, "Http|executor-10|apptype-tpch|"),
    # ("1512533812367", 1, 16, "Http|executor-10|apptype-ml|"),

    # ("1512452216050", 1, 176, "Republic|executor-10|apptype-tpch|circuit-keep|$r_{a}$=0.1|line-last"),
    # ("1512458312682", 1, 176, "Republic|executor-10|apptype-tpch|circuit-keep|$r_{a}$=0.01|line-last"),
    # ("1512464414229", 1, 176, "Republic|executor-10|apptype-tpch|circuit-keep|$r_{a}$=0.003|line-last"),
    # ("1512470517068", 1, 176, "Republic|executor-10|apptype-tpch|circuit-keep|$r_{a}$=0.001|line-last"),
    # ("1512391523750", 1, 176, "Republic|executor-10|apptype-tpch|circuit-keep|$r_{a}$=0.0001|line-last"),
    # ("1512476620037", 1, 176, "Republic|executor-10|apptype-tpch|circuit-keep|$r_{a}$=0.00001|line-last"),

    # ("1512752844958", 1, 176, "Republic|executor-10|apptype-tpch|circuit-keep|$r_{a}$=0.01|line-first"),
    # ("1512760431084", 1, 176, "Republic|executor-10|apptype-tpch|circuit-keep|$r_{a}$=0.003|line-first"),
    #
    # ("1512464414229", 1, 176, "Republic|executor-10|apptype-tpch|circuit-keep|$r_{a}$=0.003|line-last"),
    # ("1513036075822", 1, 176, "Republic|executor-10|apptype-tpch|circuit-notkeep|$r_{a}$=0.003|line-last"),

]

# experiment_entries_l = [
#     ("1512712222655", 1, 176, "Republic|executor-10|apptype-tpch|circuit-keep|$r_{a}$=0.1|line-last|"),
#     ("1512458312682", 1, 176, "Republic|executor-10|apptype-tpch|circuit-keep|$r_{a}$=0.01|line-last"),
#     ("1512727739418", 1, 176, "Republic|executor-10|apptype-tpch|circuit-keep|$r_{a}$=0.003|line-last|"),
#     ("1512735350680", 1, 176, "Republic|executor-10|apptype-tpch|circuit-keep|$r_{a}$=0.001|line-last|"),
#     ("1512742926755", 1, 176, "Republic|executor-10|apptype-tpch|circuit-keep|$r_{a}$=0.0001|line-last"),
# ]
experiment_entries_l = [
    ("1512712222655", 1, 176, "$i_{a}$=70$\mu$s"),
    ("1512458312682", 1, 176, "$i_{a}$=700$\mu$s"),
    ("1512727739418", 1, 176, "$i_{a}$=2$m$s"),
    ("1512735350680", 1, 176, "$i_{a}$=7$m$s"),
    ("1512742926755", 1, 176, "$i_{a}$=70$m$s"),
    # ("1512752844958", 1, 176, "$r_{a}$=.01, first"),
    ("1512760431084", 1, 176, "$i_{a}$=2$m$s, alternative"),
    # ("1513036075822", 1, 176, "$r_{a}$=2$m$s, not keep"),
]
draw_apptype = 'tpch'
figure_id = 10

[
    ("1512501574331", 1, 16, "Republic|executor-10|apptype-ml|circuit-keep|$r_{a}$=0.01|line-last"),
    ("1512525379220", 1, 16, "Republic|executor-10|apptype-ml|circuit-keep|$r_{a}$=0.01|line-last"),
    ("1512623695146", 1, 16, "Republic|executor-22|apptype-ml|circuit-keep|$r_{a}$=0.003|line-last"),
    ("1512630731524", 1, 16, "Republic|executor-22|apptype-ml|circuit-keep|$r_{a}$=0.003|line-last"),
    # ("1512452216050", 1, 176, "Republic|executor-10|apptype-tpch|circuit-keep|$r_{a}$=0.1|line-last"),
    # ("1512720128691", 1, 176, "Republic|executor-10|apptype-tpch|circuit-keep|$r_{a}$=0.01|line-last|"),
    # ("1512464414229", 1, 176, "Republic|executor-10|apptype-tpch|circuit-keep|$r_{a}$=0.003|line-last"),
    # ("1512470517068", 1, 176, "Republic|executor-10|apptype-tpch|circuit-keep|$r_{a}$=0.001|line-last"),
    # ("1512476620037", 1, 176, "Republic|executor-10|apptype-tpch|circuit-keep|$r_{a}$=0.00001|line-last"),
]
# experiment_entries_l = [
#     ("1512367451535", 1, 176, "Republic|$r_{a}$=0.1|lastsync"),
#     ("1512373466531", 1, 176, "Republic|$r_{a}$=0.01|lastsync"),
#     ("1512379483569", 1, 176, "Republic|$r_{a}$=0.003|lastsync"),
#     ("1512385502493", 1, 176, "Republic|$r_{a}$=0.001|lastsync"),
#     ("1512391523750", 1, 176, "Republic|$r_{a}$=0.0001|lastsync"),
#     ("1512397546318", 1, 176, "Torrent"),
#     ("1512404528613", 1, 176, "Http"),
#     ("1512413548072", 1, 44, "Republic|$r_{a}$=0.003|firstsync"),
#     ("1512415296264", 1, 44, "Republic|$r_{a}$=0.001|firstsync"),
# ]

# experiment_entries_l = [
#     ("1512613588556", 1, 176, "Republic"),
#     # ("1512589528420", 1, 176, "Torrent"),
#     # ("1512601339634", 1, 176, "Http"),
#     ("1512839468326", 1, 176, "Torrent_1:1"),
#     ("1512851298253", 1, 176, "Http_1:1"),
# ]
# draw_apptype = 'tpch_1v1'
# figure_id = 22
#
# experiment_entries_l = [
#     ("1512464414229", 1, 176, "Republic"),
#     # ("1512482685448", 1, 176, "Torrent"),
#     # ("1512489051950", 1, 176, "Http"),
#     ("1512795376376", 1, 176, "Torrent_1:1"),
#     ("1512803872855", 1, 176, "Http_1:1"),
# ]
# draw_apptype = 'tpch_1v1'
# figure_id = 10

# experiment_entries_l = [
#     ("1512627216791", 1, 16, "Republic"),
#     # ("1512578894665", 1, 16, "Torrent"),
#     # ("1512582376567", 1, 16, "Http"),
#     ("1512874012631", 1, 16, "Torrent_1:1"),  # ("1512863134269", 1, 16, "Torrent_1:1"),
#     ("1512867225488", 1, 16, "Http_1:1"),  # ("1512877799027", 1, 16, "Http_1:1_"),
# ]
# draw_apptype = 'ml_1v1'
# figure_id = 22

# experiment_entries_l = [
#     ("1512515004478", 1, 16, "Republic"),
#     # ("1512530331790", 1, 16, "Torrent"),
#     # ("1512533812367", 1, 16, "Http"),
#     ("1512932713471", 1, 16, "Torrent_1:1"),  # ("1512899876777", 1, 16, "Torrent_1:1"),
#     ("1512903660044", 1, 16, "Http_1:1"),
#     # ("1512919044827", 1, 16, "Http_1:1_"), ("1512896095925", 1, 16, "Http_1:1__"),
# ]
# draw_apptype = 'ml_1v1'
# figure_id = 10

draw_appname = {'ml': ['wor', 'lda'],
                'ml_1v1': ['wor', 'lda'],
                'tpch': ['tpc'],
                'tpch_1v1': ['tpc']}

experiment_plot_d = [
    # "recv_loss",
    # "recv_extra_time_total",
    # "recv_extra_time_data_channel",
    #
    # "send_retransmission",
    # "send_duplicated_bytes",
    # "send_attempt_sending_time",
    "send_extra_time_total",
    "send_extra_time_data_channel",

    # "application_running_time",
    # "broadcast_reading_time",
    #
    # "send_manager_response",

    # "recv_all",
    # "send_all"
]

experiment_plot_xlim_d = {
    "recv_loss": 4000,
    "recv_extra_time_total": 150,
    "recv_extra_time_data_channel": 150,
    "send_retransmission": 20000,
    "send_duplicated_bytes": 100,
    "send_attempt_sending_time": 150,
    "send_extra_time_total": 150,
    "send_extra_time_data_channel": 150,
    # "application_running_time": 10000,
    "broadcast_reading_time": 200,
}

fontsize_ = 10
# color_l = ['rebeccapurple', 'indianred', 'lightsalmon']
# linestyle_l = ['-', '--', '-.']


color_l = ['black', 'rebeccapurple', 'indianred', 'lightsalmon', 'tan', 'lightgrey', 'black', 'y']
linestyle_l = [':', '--', '-', '-.', ':', '-', '-']


def draw_cdf(ee_data_l, figsize=(3, 2), subfigure=(1, 1, 1), label_l=[], xlabel='x', xlimit=[], ylabel='y', ylimit=[],
             title='',
             xlog=False,
             save_name=""):
    plt.figure(figsize=figsize)
    ax = plt.subplot(*subfigure)
    x_max = 0
    for idx in range(len(ee_data_l)):
        data_ee_data = ee_data_l[idx]
        ee = data_ee_data[0]
        data_l = data_ee_data[1]
        run_name = ee[3] if label_l else ee[3]
        x_data_l_sort = sorted(data_l)
        y_cdf_l = [(idxx + 1.0) / len(x_data_l_sort) for idxx in range(len(x_data_l_sort))]
        ax.plot(x_data_l_sort, y_cdf_l, label=run_name, color=color_l[idx % len(color_l)],
                linestyle=linestyle_l[idx % len(linestyle_l)])
        x_max = max(x_max, max(x_data_l_sort))

    if xlog:
        ax.set_xscale("log", nonposx='clip')

    if xlimit:
        ax.set_xlim(xlimit)
    else:
        ax.set_xlim([0, int(x_max * 1.1)])

    ax.set_xlabel(xlabel, fontsize=fontsize_)
    plt.xticks(fontsize=fontsize_)

    if ylimit:
        ax.set_ylim(ylimit)
    else:
        ax.set_ylim([0, 1])
    ax.set_ylabel(ylabel, fontsize=fontsize_)
    plt.yticks(fontsize=fontsize_)

    ax.set_title(title)
    ax.grid(linestyle='-.', which='both')
    # ax.legend(fontsize=9, loc='lower right')

    plt.subplots_adjust(left=0.19, bottom=0.24, right=0.95, top=0.96, wspace=0, hspace=0)

    if len(save_name) and False:
        plt.savefig('/Users/[SERVER_USERNAME]/github/eugeneng/REPUBLIC/figures/%s.eps' % (save_name),
                    format='eps', dpi=300)


def draw_scatter(ee_xdata_l, ee_ydata_l, subfigure=(1, 1, 1), xlabel='x', xlimit=[], ylabel='y', title='figure',
                 xlog=False):
    ax = plt.subplot(*subfigure)
    # for idx in range(len(ee_xdata_l)):
    assert ee_xdata_l[0] == ee_xdata_l[0]
    run_name = ee_xdata_l[0][3]
    x_data_l = ee_xdata_l[1]
    y_data_l = ee_ydata_l[1]
    ax.scatter(x_data_l, y_data_l, label=run_name, s=5, marker='.')

    if xlog:
        ax.set_xscale("log", nonposx='clip')
    ax.set_xlabel(xlabel)
    if xlimit:
        ax.set_xlim(xlimit)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(linestyle='-.')
    ax.legend()


ee_appid_appname_l = []
for ee in experiment_entries_l:
    run_id = "%s_%d-%d" % (ee[0], ee[1], ee[2])
    run_name = ee[3]
    run_path = "../parse/log/" + run_id + "/"
    appid_appname_path = run_path + run_id + "_name.csv"
    appid_appname_d = {}
    with open(appid_appname_path, 'r') as f:
        for line in f.readlines():
            line_l = line.split(',')
            appid_appname_d[line_l[0]] = line_l[1].split("_")
    ee_appid_appname_l.append(appid_appname_d)
# print pprint.pprint(ee_appid_appname_l)

"""application runtime"""
if "application_running_time" in experiment_plot_d:
    ee_data_runtime_l = []
    for idx in range(len(experiment_entries_l)):
        ee = experiment_entries_l[idx]
        run_id = "%s_%d-%d" % (ee[0], ee[1], ee[2])
        run_name = ee[3]
        run_path = "../parse/log/" + run_id + "/"
        appattempt_runtime_d = {}
        with open(run_path + "/" + run_id + "_DURATION.csv", 'r') as f:
            for exp in f.readlines():
                exp_l = exp[:-1].split(',')
                exp_ll = exp_l[0].split('_')
                appid = 'application_%s_%s' % (exp_ll[1], exp_ll[2])
                if ee_appid_appname_l[idx][appid][0][2:5] in draw_appname[draw_apptype]:
                    exp_name = "_".join(exp_ll[:-1])
                    print exp_name
                    if exp_name in appattempt_runtime_d:
                        if int(appattempt_runtime_d[exp_name][1]) < int(exp_ll[-1]):
                            appattempt_runtime_d[exp_name] = (float(exp_l[5]), int(exp_ll[-1]))
                    else:
                        appattempt_runtime_d[exp_name] = (float(exp_l[5]), int(exp_ll[-1]))
        ee_data_runtime_l.append((ee, [a[0] for a in appattempt_runtime_d.values()]))
    # pprint.pprint(ee_data_runtime_l)
    draw_cdf(ee_data_runtime_l, xlabel='application running time (sec)',
             xlimit=[] if "application_running_time" not in experiment_plot_xlim_d else [0, experiment_plot_xlim_d[
                 "application_running_time"]],
             ylabel='cdf',  # title=draw_apptype,
             save_name="application_running_time_%s_%d" % (draw_apptype, figure_id))
    plt.show()

"""broadcast reading time"""
if "broadcast_reading_time" in experiment_plot_d:
    appname_brt_l = []
    ee_data_brt_l = []

    for idx in range(len(experiment_entries_l)):
        ee = experiment_entries_l[idx]
        run_id = "%s_%d-%d" % (ee[0], ee[1], ee[2])
        run_name = ee[3]
        run_path = "../parse/log/" + run_id + "/spark/"

        appname_brt_d = {}  # {'tpch-2': {'application_%s_%04d': {4: ('453', 'MB', [2.45454, 6.54545, 8.4343])}}}
        brt_l = []

        for exp_id in range(ee[1], ee[2] + 1):
            appid = "application_%s_%04d" % (ee[0], exp_id)
            apptype = ee_appid_appname_l[idx][appid][0][2:5]

            if apptype in draw_appname[draw_apptype]:
                # if appid not in blacklist_l:
                bid_sizetime_d = {}  # {bcd id: [(size, unit), time]}
                exp_path = run_path + "application_%s_%04d_brt_size.log" % (ee[0], exp_id)
                with open(exp_path, 'r') as f:
                    for line in f.readlines():
                        line_l = line.split()
                        bid_sizetime_d[int(line_l[5].split('_')[1])] = (line_l[13], line_l[14].split(',')[0], [])

                # print bid_sizetime_d
                exp_path = run_path + "application_%s_%04d_brt_time.log" % (ee[0], exp_id)
                with open(exp_path, 'r') as f:
                    for line in f.readlines():
                        line_l = line.split()
                        # print line_l
                        # print bid_sizetime_d
                        bid_sizetime_d[int(line_l[6])][2].append(float(line_l[8]) / 1000.0)
                # pprint.pprint(bid_sizetime_d)
                if apptype not in appname_brt_d:
                    appname_brt_d[apptype] = {appid: bid_sizetime_d}
                else:
                    appname_brt_d[apptype][appid] = bid_sizetime_d

                for k, v in bid_sizetime_d.iteritems():
                    if v[1] == 'MB' or v[1] == 'GB':
                        brt_l = brt_l + v[2]
        # pprint.pprint(appname_brt_d)
        ee_data_brt_l.append((ee, brt_l))
        appname_brt_l.append(appname_brt_d)
    draw_cdf(ee_data_brt_l, xlabel='broadcast reading time (sec)',
             xlimit=[] if "broadcast_reading_time" not in experiment_plot_xlim_d else [0, experiment_plot_xlim_d[
                 "broadcast_reading_time"]],
             ylabel='cdf',  # title=draw_apptype,
             save_name="broadcast_reading_time_%s_%d" % (draw_apptype, figure_id),
             # xlog=True
             )
    plt.show()

"""republic agent metric"""
# RECEIVING
# data size
# packet loss (rate)
# data channel time
# after data channel time
# data channel efficiency

# SENDING
# duplicate sending
# active (first to last)
# retransmission (rate)
# attempt
# near-line-rate
# data channel efficiency
# overhead
# manager response
# data channel occupy (first to last gogogo)

# appname_brt_republic_l = []
if True:
    recv_datasize_l = []
    recv_packetlossrate_l = []
    recv_packetloss_l = []
    recv_datachanneltime_l = []
    recv_afterdatachanneltime_l = []
    recv_datachannelefficiency_l = []
    recv_overallefficiency_l = []
    recv_totaltime_l = []
    recv_extraideal_l = []
    recv_extradatachannelideal_l = []
    recv_extraideal_re_l = []
    recv_extradatachannelideal_re_l = []

    send_datasize_l = []
    send_duplicatedbytes_l = []
    send_activefirsttolastsending_l = []
    send_datachannelinefficiency_l = []
    send_attempttime_l = []
    send_nearlinerate_l = []
    send_overhead_l = []
    send_retransmissionrate_l = []
    send_retransmission_l = []
    send_managerresponse_l = []
    send_datachanneloccupy_l = []
    send_extraideal_s_l = []
    send_extradatachannelideal_s_l = []
    send_extraideal_re_s_l = []
    send_extradatachannelideal_re_s_l = []

    for idx in range(len(experiment_entries_l)):
        ee = experiment_entries_l[idx]
        run_name = ee[3]
        if True or "Rep" in run_name:
            run_id = "%s_%d-%d" % (ee[0], ee[1], ee[2])
            run_path = "../parse/log/" + run_id + "/"

            exp_path = run_path + 'republic/'

            # get the line# of each log file from agent
            appid_brt_republic_d = {}  # {'appid': [0,5,6,7]}
            print exp_path
            for filename in os.listdir(exp_path):
                if 'application_' in filename:
                    appid = filename[:30]
                    with open(exp_path + filename, 'r') as f:
                        if appid not in appid_brt_republic_d:
                            appid_brt_republic_d[appid] = []
                        appid_brt_republic_d[appid].append(len(f.readlines()))
            # pprint.pprint(appid_brt_republic_d)
            # pprint.pprint(ee_appid_appname_l[idx])

            # aggregate application id to application type (tpch-1, word2vec, etc...)
            apptype_brt_republic_d = {}
            for k, v in appid_brt_republic_d.iteritems():
                apptype = ee_appid_appname_l[idx][k][0]
                if min(v) != 0:  # remove application id having no log
                    if apptype not in apptype_brt_republic_d:
                        apptype_brt_republic_d[apptype] = [k]
                    else:
                        apptype_brt_republic_d[apptype].append(k)
                        # pprint.pprint(apptype_brt_republic_d)
                        # for filename in os.listdir(exp_path + 'concise/'):
                        #     with open(exp_path + 'concise/' + filename, 'r') as f:
                        #         appid = filename[:30]
                        #         lines = f.readlines()
                        # expect_grid_num = 38 if 'receiver' in filename else 74
                        # expect_grid_num_extended = 42 if 'receiver' in filename else 76
                        # for l in lines:
                        #     if len(l[:-1].split(',')) != expect_grid_num_extended: #len(l[:-1].split(',')) != expect_grid_num and \
                        #         for k, v in apptype_brt_republic_d.iteritems():
                        #             if appid in v:
                        #                 v.remove(appid)
                        #                 break
                        #         break

            min_app_run = min([len(v) for v in apptype_brt_republic_d.values()])
            accepted_appid = []
            for v in apptype_brt_republic_d.values():
                accepted_appid = accepted_appid + v[:min_app_run]
            print "accept %d applications" % min_app_run

            datasize_r_l = []
            packetlossrate_l = []
            packetloss_l = []
            datachanneltime_l = []
            afterdatachanneltime_l = []
            totaltime_l = []
            datachannelefficiency_l = []
            overallefficiency_l = []
            extraideal_l = []
            extradatachannelideal_l = []
            extraideal_re_l = []
            extradatachannelideal_re_l = []

            datasize_s_l = []
            duplicatedbytes_l = []
            activefirsttolastsending_l = []
            datachannelinefficiency_l = []
            attempttime_l = []
            nearlinerate_l = []
            overhead_l = []
            retransmissionrate_l = []
            retransmission_l = []
            managerresponse_l = []
            datachanneloccupy_l = []
            extraideal_s_l = []
            extradatachannelideal_s_l = []
            extraideal_re_s_l = []
            extradatachannelideal_re_s_l = []

            for filename in os.listdir(exp_path + 'concise/'):
                # print exp_path + 'concise/' + filename
                appid = filename[:30]
                # if appid in accepted_appid and appid not in blacklist_l:
                with open(exp_path + 'concise/' + filename, 'r') as f:
                    if 'receiver' in filename:  # RECEIVING
                        lines = f.readlines()
                        f_l = [exp[:-1].split(',') for exp in lines]
                        datasize_r_l = datasize_r_l + [int(f[12]) for f in f_l]
                        packetlossrate_l = packetlossrate_l + [float(f[20]) for f in f_l]
                        packetloss_l = packetloss_l + [int(f[22]) for f in f_l]
                        datachanneltime_l = datachanneltime_l + [float(f[26]) for f in f_l]
                        afterdatachanneltime_l = afterdatachanneltime_l + [float(f[28]) for f in f_l]
                        totaltime_l = totaltime_l + [float(f[31]) for f in f_l]
                        datachannelefficiency_l = datachannelefficiency_l + [float(f[34]) / 100.0 for f in f_l]
                        overallefficiency_l = overallefficiency_l + [float(f[36]) / 100.0 for f in f_l]
                        # extraideal_l = extraideal_l + [
                        #     [float(f[31]) for f in f_l][idx] - (
                        #         [int(f[12]) for f in f_l][idx] + (int(f[16]) + 1) * 74 + 72) * 8.0 / (
                        #         10.0 * 1000 * 1000) for idx in range(len(f_l))
                        # ]
                        extraideal_l = extraideal_l + [
                            float(f[31]) - (
                                int(f[12]) + (int(f[16]) + 1) * 74 + 72) * 8.0 / (
                                10.0 * 1000 * 1000) for f in f_l
                        ]
                        # extradatachannelideal_l = extradatachannelideal_l + [
                        #     [float(f[26]) for f in f_l][idx] - (
                        #         [int(f[12]) for f in f_l][idx] + (int(f[16]) + 1) * 74 + 72) * 8.0 / (
                        #         10.0 * 1000 * 1000) for idx in range(len(f_l))
                        # ]
                        extradatachannelideal_l = extradatachannelideal_l + [
                            float(f[26]) - (
                                int(f[12]) + (int(f[16]) + 1) * 74 + 72) * 8.0 / (
                                10.0 * 1000 * 1000) for f in f_l
                        ]
                        extraideal_re_l = extraideal_re_l + [
                            (float(f[31]) - (
                                int(f[12]) + (int(f[16]) + 1) * 74 + 72) * 8.0 / (
                                 10.0 * 1000 * 1000)) / ((
                                                             int(f[12]) + (int(f[16]) + 1) * 74 + 72) * 8.0 / (
                                                             10.0 * 1000 * 1000)) for f in f_l
                        ]
                        extradatachannelideal_re_l = extradatachannelideal_re_l + [
                            (float(f[26]) - (
                                int(f[12]) + (int(f[16]) + 1) * 74 + 72) * 8.0 / (
                                 10.0 * 1000 * 1000)) / ((
                                                             int(f[12]) + (int(f[16]) + 1) * 74 + 72) * 8.0 / (
                                                             10.0 * 1000 * 1000)) for f in f_l
                        ]

                    elif 'sender' in filename:  # SENDING
                        lines = f.readlines()
                        f_l = [exp[:-1].split(',') for exp in lines]
                        datasize_s_l = datasize_s_l + [int(f[12]) for f in f_l]
                        duplicatedbytes_l = duplicatedbytes_l + [(float(f[20]) - float(f[22])) / 1024 / 1024 for f in
                                                                 f_l]
                        activefirsttolastsending_l = activefirsttolastsending_l + [float(f[27]) for f in f_l]
                        datachannelinefficiency_l = datachannelinefficiency_l + [float(f[30]) for f in f_l]
                        attempttime_l = attempttime_l + [float(f[43]) for f in f_l]
                        nearlinerate_l = nearlinerate_l + [float(f[45]) for f in f_l]
                        overhead_l = overhead_l + [float(f[63]) for f in f_l]
                        retransmissionrate_l = retransmissionrate_l + [float(f[67]) for f in f_l]
                        retransmission_l = retransmission_l + [float(f[66]) for f in f_l]
                        managerresponse_l = managerresponse_l + [float(f[70]) for f in f_l]
                        datachanneloccupy_l = datachanneloccupy_l + [float(f[72]) for f in f_l]
                        # extraideal_s_l = extraideal_s_l + [
                        #     [float(f[72]) for f in f_l][idx] - (
                        #         [int(f[12]) for f in f_l][idx] + (int(f[16]) + 1) * 74 + 72) * 8.0 / (
                        #         10.0 * 1000 * 1000) for idx in range(len(f_l))
                        # ]
                        extraideal_s_l = extraideal_s_l + [
                            float(f[58]) - (
                                int(f[12]) + (int(f[16]) + 1) * 74 + 72) * 8.0 / (
                                10.0 * 1000 * 1000) for f in f_l
                        ]
                        # extradatachannelideal_s_l = extradatachannelideal_s_l + [
                        #     [float(f[61]) for f in f_l][idx] - (
                        #         [int(f[12]) for f in f_l][idx] + (int(f[16]) + 1) * 74 + 72) * 8.0 / (
                        #         10.0 * 1000 * 1000) for idx in range(len(f_l))
                        # ]
                        extradatachannelideal_s_l = extradatachannelideal_s_l + [
                            float(f[72]) - (
                                int(f[12]) + (int(f[16]) + 1) * 74 + 72) * 8.0 / (
                                10.0 * 1000 * 1000) for f in f_l
                        ]
                        extraideal_re_s_l = extraideal_re_s_l + [
                            (float(f[58]) - (
                                int(f[12]) + (int(f[16]) + 1) * 74 + 72) * 8.0 / (
                                 10.0 * 1000 * 1000)) / ((
                                                             int(f[12]) + (int(f[16]) + 1) * 74 + 72) * 8.0 / (
                                                             10.0 * 1000 * 1000)) for f in f_l
                        ]
                        extradatachannelideal_re_s_l = extradatachannelideal_re_s_l + [
                            (float(f[72]) - (
                                int(f[12]) + (int(f[16]) + 1) * 74 + 72) * 8.0 / (
                                 10.0 * 1000 * 1000)) / ((
                                                             int(f[12]) + (int(f[16]) + 1) * 74 + 72) * 8.0 / (
                                                             10.0 * 1000 * 1000)) for f in f_l
                        ]

            recv_datasize_l.append((ee, datasize_r_l))
            recv_packetloss_l.append((ee, packetloss_l))
            recv_packetlossrate_l.append((ee, packetlossrate_l))
            recv_datachanneltime_l.append((ee, datachanneltime_l))
            recv_afterdatachanneltime_l.append((ee, afterdatachanneltime_l))
            recv_datachannelefficiency_l.append((ee, datachannelefficiency_l))
            recv_overallefficiency_l.append((ee, overallefficiency_l))
            recv_totaltime_l.append((ee, totaltime_l))
            recv_extraideal_l.append((ee, extraideal_l))
            recv_extradatachannelideal_l.append((ee, extradatachannelideal_l))
            recv_extraideal_re_l.append((ee, extraideal_re_l))
            recv_extradatachannelideal_re_l.append((ee, extradatachannelideal_re_l))

            send_datasize_l.append((ee, datasize_s_l))
            send_duplicatedbytes_l.append((ee, duplicatedbytes_l))
            send_activefirsttolastsending_l.append((ee, activefirsttolastsending_l))
            send_datachannelinefficiency_l.append((ee, datachannelinefficiency_l))
            send_attempttime_l.append((ee, attempttime_l))
            send_nearlinerate_l.append((ee, nearlinerate_l))
            send_overhead_l.append((ee, overhead_l))
            send_retransmissionrate_l.append((ee, retransmissionrate_l))
            send_retransmission_l.append((ee, retransmission_l))
            send_managerresponse_l.append((ee, managerresponse_l))
            send_datachanneloccupy_l.append((ee, datachanneloccupy_l))
            send_extraideal_s_l.append((ee, extraideal_s_l))
            send_extradatachannelideal_s_l.append((ee, extradatachannelideal_s_l))
            send_extraideal_re_s_l.append((ee, extraideal_re_s_l))
            send_extradatachannelideal_re_s_l.append((ee, extradatachannelideal_re_s_l))

    if "recv_loss" in experiment_plot_d:
        draw_cdf(recv_packetloss_l,
                 xlabel='Number of lost packets (#)',
                 xlimit=[] if "recv_loss" not in experiment_plot_xlim_d else [0, experiment_plot_xlim_d["recv_loss"]],
                 ylabel='cdf',
                 ylimit=[0.7, 1],
                 title="",
                 save_name="recv_loss_%s_%d" % (draw_apptype, figure_id), xlog=True)
        plt.show()

    if "recv_extra_time_data_channel" in experiment_plot_d:
        draw_cdf(recv_extradatachannelideal_l,
                 xlabel='Data channel extra receiving time (ms)',
                 xlimit=[] if "recv_extra_time_data_channel" not in experiment_plot_xlim_d else [0,
                                                                                                 experiment_plot_xlim_d[
                                                                                                     "recv_extra_time_data_channel"]],
                 ylabel='cdf', title="",
                 save_name="recv_extra_time_data_channel_%s_%d" % (draw_apptype, figure_id))
        plt.show()

    if "recv_extra_time_data_channel_re" in experiment_plot_d:
        draw_cdf(recv_extradatachannelideal_re_l,
                 xlabel='Data channel (re)extra receiving time (X)',
                 xlimit=[] if "recv_extra_time_data_channel_re" not in experiment_plot_xlim_d else
                 [0, experiment_plot_xlim_d["recv_extra_time_data_channel_re"]],
                 ylabel='cdf', title="",
                 save_name="recv_extra_time_data_channel_re_%s_%d" % (draw_apptype, figure_id))
        plt.show()

    if "recv_extra_time_total" in experiment_plot_d:
        draw_cdf(recv_extraideal_l,
                 xlabel='Total extra receiving time (ms)',
                 xlimit=[] if "recv_extra_time_total" not in experiment_plot_xlim_d else [0, experiment_plot_xlim_d[
                     "recv_extra_time_total"]],
                 ylabel='cdf', title="",
                 save_name="recv_extra_time_total_%s_%d" % (draw_apptype, figure_id))
        plt.show()

    if "recv_extra_time_total_re" in experiment_plot_d:
        draw_cdf(recv_extraideal_re_l,
                 xlabel='Total (re)extra receiving time (X)',
                 xlimit=[] if "recv_extra_time_total_re" not in experiment_plot_xlim_d else [0, experiment_plot_xlim_d[
                     "recv_extra_time_total_re"]],
                 ylabel='cdf', title="",
                 save_name="recv_extra_time_total_re_%s_%d" % (draw_apptype, figure_id))
        plt.show()

    if "send_retransmission" in experiment_plot_d:
        draw_cdf(send_retransmission_l,
                 xlabel='Number of retransmit packets (#)',
                 xlimit=[] if "send_retransmission" not in experiment_plot_xlim_d else [0, experiment_plot_xlim_d[
                     "send_retransmission"]],
                 ylabel='cdf',
                 title="",
                 save_name="send_retransmission_%s_%d" % (draw_apptype, figure_id))
        plt.show()

    if "send_duplicated_bytes" in experiment_plot_d:
        draw_cdf(send_duplicatedbytes_l,
                 xlabel='Extra sending bytes (MB)',
                 xlimit=[] if "send_duplicated_bytes" not in experiment_plot_xlim_d else [0, experiment_plot_xlim_d[
                     "send_duplicated_bytes"]],
                 ylabel='cdf', title="", save_name="send_duplicated_bytes_%s_%d" % (draw_apptype, figure_id),
                 xlog=True)
        plt.show()

    if "send_attempt_sending_time" in experiment_plot_d:
        draw_cdf(send_attempttime_l,
                 xlabel='Attempt sending time (ms)',
                 xlimit=[] if "send_attempt_sending_time" not in experiment_plot_xlim_d else [0, experiment_plot_xlim_d[
                     "send_attempt_sending_time"]],
                 ylabel='cdf', title="",
                 save_name="send_attempt_sending_time_%s_%d" % (draw_apptype, figure_id))
        plt.show()

    if "send_extra_time_data_channel" in experiment_plot_d:
        draw_cdf(send_extradatachannelideal_s_l,
                 xlabel='Data channel extra sending time (ms)',
                 xlimit=[] if "send_extra_time_data_channel" not in experiment_plot_xlim_d else [0,
                                                                                                 experiment_plot_xlim_d[
                                                                                                     "send_extra_time_data_channel"]],
                 ylabel='cdf', title="",
                 save_name="send_extra_time_data_channel_%s_%d" % (draw_apptype, figure_id))
        plt.show()

    if "send_extra_time_data_channel_re" in experiment_plot_d:
        draw_cdf(send_extradatachannelideal_re_s_l,
                 xlabel='Data channel (re)extra sending time (X)',
                 xlimit=[] if "send_extra_time_data_channel_re" not in experiment_plot_xlim_d else
                 [0, experiment_plot_xlim_d["send_extra_time_data_channel_re"]],
                 ylabel='cdf', title="",
                 save_name="send_extra_time_data_channel_re_%s_%d" % (draw_apptype, figure_id))
        plt.show()

    if "send_extra_time_total" in experiment_plot_d:
        draw_cdf(send_extraideal_s_l,
                 xlabel='Total extra sending time (ms)',
                 xlimit=[] if "send_extra_time_total" not in experiment_plot_xlim_d else [0, experiment_plot_xlim_d[
                     "send_extra_time_total"]],
                 ylabel='cdf',
                 title="",
                 save_name="send_extra_time_total_%s_%d" % (draw_apptype, figure_id)
                 )
        plt.show()

    if "send_extra_time_total_re" in experiment_plot_d:
        draw_cdf(send_extraideal_re_s_l,
                 xlabel='Total (re)extra sending time (X)',
                 xlimit=[] if "send_extra_time_total_re" not in experiment_plot_xlim_d else [0, experiment_plot_xlim_d[
                     "send_extra_time_total_re"]],
                 ylabel='cdf', title="",
                 save_name="send_extra_time_total_re_%s_%d" % (draw_apptype, figure_id))
        plt.show()

    if "send_manager_response" in experiment_plot_d:
        draw_cdf(send_managerresponse_l,
                 xlabel='Republic manager response time (ms)',
                 xlimit=[] if "send_manager_response" not in experiment_plot_xlim_d else [0, experiment_plot_xlim_d[
                     "send_manager_response"]],
                 ylabel='cdf', title="",
                 save_name="send_manager_response_%s_%d" % (draw_apptype, figure_id),
                 xlog=True)
        plt.show()

    # if "recv_data_receiving_time_scatter" in experiment_plot_d:
    #     for idx in range(len(recv_datasize_l)):
    #         draw_scatter(recv_datasize_l[idx], recv_totaltime_l[idx],
    #                      subfigure=(2, 4, idx + 1), xlabel='data size (Bytes)', ylabel='data receiving time (ms)',
    #                      title="")
    #     plt.show()
    #
    # if "recv_extra_time_scatter" in experiment_plot_d:
    #     for idx in range(len(recv_datasize_l)):
    #         draw_scatter(recv_datasize_l[idx], recv_extraideal_l[idx],
    #                      subfigure=(2, 4, idx + 1), xlabel='data size (Byte)', ylabel='extra overhead (ms)', title="")
    #     plt.show()

    if "recv_all" in experiment_plot_d:
        draw_cdf(recv_datasize_l,
                 subfigure=(2, 4, 1), xlabel='datasize (byte)', ylabel='cdf', title="", xlog=True)
        draw_cdf(recv_packetlossrate_l,
                 subfigure=(2, 4, 2), xlabel='packet loss rate (%)', ylabel='cdf', title="", xlog=True)
        draw_cdf(recv_packetloss_l,
                 subfigure=(2, 4, 3), xlabel='packet loss (#)', ylabel='cdf', title="", xlog=True)
        draw_cdf(recv_datachanneltime_l,
                 subfigure=(2, 4, 4), xlabel='data channel time (ms)\nfrom first data to last data', ylabel='cdf',
                 title="")
        draw_cdf(recv_afterdatachanneltime_l,
                 subfigure=(2, 4, 5), xlabel='after data channel time (ms)\nfrom last data to all done', ylabel='cdf',
                 title="", xlog=True)
        draw_cdf(recv_datachannelefficiency_l,
                 subfigure=(2, 4, 6), xlabel='data channel efficiency (x)\ndata channel time, comparing with ideal',
                 xlimit=[0.0, 1], ylabel='cdf', title="")
        draw_cdf(recv_extraideal_l,
                 subfigure=(2, 4, 7), xlabel='extra overhead (ms)', ylabel='cdf', title="")
        draw_cdf(recv_extraideal_l,
                 subfigure=(2, 4, 8), xlabel='extra overhead (ms)', xlimit=[-100, 500], ylabel='cdf', title="")
        plt.show()

    if "send_all" in experiment_plot_d:
        draw_cdf(send_datasize_l,
                 subfigure=(2, 5, 1), xlabel='datasize (byte)', ylabel='cdf', title="", xlog=True)
        draw_cdf(send_duplicatedbytes_l,
                 subfigure=(2, 5, 2), xlabel='duplicate sending (x)', ylabel='cdf', title="", xlog=True)
        draw_cdf(send_activefirsttolastsending_l,
                 subfigure=(2, 5, 3), xlabel='userspace data channel active sending time (ms)', ylabel='cdf', title="")
        draw_cdf(send_datachannelinefficiency_l,
                 subfigure=(2, 5, 4), xlabel='data channel in-efficiency (x)\nactive, comparing with ideal',
                 ylabel='cdf',
                 title="", xlog=True)
        draw_cdf(send_attempttime_l,
                 subfigure=(2, 5, 5), xlabel='attempt time (ms)', ylabel='cdf', title="")
        draw_cdf(send_nearlinerate_l,
                 subfigure=(2, 5, 6), xlabel='near line rate (ms)', ylabel='cdf', title="")
        draw_cdf(send_overhead_l,
                 subfigure=(2, 5, 7), xlabel='overall overhead (x)\nfrom first data to all done, comparing with ideal',
                 ylabel='cdf', title="", xlog=True)
        draw_cdf(send_retransmissionrate_l,
                 subfigure=(2, 5, 8), xlabel='retransmission (x)\nhow many patching message', ylabel='cdf', title="",
                 xlog=True)
        draw_cdf(send_managerresponse_l,
                 subfigure=(2, 5, 9), xlabel='manager response time (ms)\nfrom request to reply', ylabel='cdf',
                 title="")
        draw_cdf(send_datachanneloccupy_l,
                 subfigure=(2, 5, 10), xlabel='data channel occupancy time (ms)\nfrom reply to release', ylabel='cdf',
                 title="")
        plt.show()

"""republic manager metric"""
if True:
    pass
