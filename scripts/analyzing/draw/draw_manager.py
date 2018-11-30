import pprint
import matplotlib.pyplot as plt
import os

experiment_entries_l = [
    ("1512613588556", 1, 176, "Republic"),
    ("1512627216791", 1, 16, "Republic"),

    ("1512464414229", 1, 176, "Republic"),
    ("1512515004478", 1, 16, "Republic"),
]
fontsize_ = 10
color_l = ['rebeccapurple', 'indianred', 'lightsalmon']
linestyle_l = ['-', '--', '-.']


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
        # print ee
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
    plt.tick_params(axis='x', which='minor')

    if ylimit:
        ax.set_ylim(ylimit)
    else:
        ax.set_ylim([0, 1])
    ax.set_ylabel(ylabel, fontsize=fontsize_)
    plt.yticks(fontsize=fontsize_)

    ax.set_title(title)
    ax.grid(linestyle='-.', which='both')
    # ax.legend(fontsize=9, loc='lower right')

    plt.subplots_adjust(left=0.19, bottom=0.24, right=0.92, top=0.96, wspace=0, hspace=0)

    if len(save_name):
        plt.savefig('/Users/[SERVER_USERNAME]/github/[SERVER_USERNAME]/phd_thesis/multicast_platform/paper/figures/%s.eps' % (save_name),
                    format='eps', dpi=300)


managerresponse_l = []
for yarn_cluster, start_idx, end_idx, _ in experiment_entries_l:
    run_id = "%s_%d-%d" % (yarn_cluster, start_idx, end_idx)
    run_path = "../parse/log/" + run_id + "/"
    exp_sender_filename = run_path + run_id + '_sender.csv'

    with open(exp_sender_filename, 'r') as f:
        lines = f.readlines()
        f_l = [exp[:-1].split(',') for exp in lines]
        managerresponse_l = managerresponse_l + [float(f[70]) for f in f_l]


print reduce(lambda x, y: x + y, managerresponse_l) / len(managerresponse_l)

draw_cdf([[[",", "", "", "haha"], managerresponse_l]],
         xlabel='Republic manager response time (ms)',
         # xlimit=[] if "send_manager_response" not in experiment_plot_xlim_d else [0, experiment_plot_xlim_d[
         #     "send_manager_response"]],
         xlimit=[0.4, 10],
         ylabel='cdf', title="",
         # save_name="send_manager_response_%s_%d" % (draw_apptype, figure_id),
         xlog=True,
         save_name='manager_response')
plt.show()
