import os

import matplotlib.pyplot as plt


def visualize_task_execution(config, schedule, chart_title):
    if len(schedule) == 0:
        return

        # Set the y-axis ticks and labels
    task_ids = list(set([job['t']['id'] for job in schedule]))
    y_labels = set(["Task " + str(id) for id in task_ids])

    # Create a horizontal bar chart
    fig, axes = plt.subplots(nrows=len(y_labels), ncols=1, sharex=True)
    if len(y_labels) == 1:
        axes = [axes]

    # Set the title
    axes[0].set_title(chart_title)
    axes[-1].set_xlabel('Time')

    max_x = int(config['scheduling_time_limit'])
    for ax_index, task_id in enumerate(task_ids):
        ax = axes[ax_index]
        ax.set_yticks([0])
        ax.set_yticklabels(["Task " + str(task_id)])
        ax.set_xlim(0, max_x)

    for job in schedule:
        ax_index = task_ids.index(job['t']['id'])
        ax = axes[ax_index]
        ax.barh(job['t']['id'], job['e'], left=job['s'], height=1, align='center')

    plt.subplots_adjust(wspace=0, hspace=0)

    # Show the plot

    if config['show_plots']:
        plt.show()

    if config['save_plots']:
        plots_dir_path = config['output_dir'] + "/plots"
        os.makedirs(plots_dir_path, exist_ok=True)
        plot_path = plots_dir_path + "/" + chart_title + '.png'
        plt.savefig(plot_path)
