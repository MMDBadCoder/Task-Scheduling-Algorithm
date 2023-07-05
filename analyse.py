import datetime
import os

import matplotlib.pyplot as plt
import yaml

from main import run_with_config


def show_chart(config, data):
    courses = list(data.keys())
    values = list(data.values())

    fig = plt.figure(figsize=(10, 5))

    plt.bar(courses, values, color='maroon', width=0.9)

    plt.xlabel("Cores number")
    plt.ylabel("Sum of fitness values of cores")
    plt.title("Fitness value by core number")

    if config['show_plots']:
        plt.show()

    if config['save_plots']:
        plots_dir_path = config['output_dir'] + "/plots"
        os.makedirs(plots_dir_path, exist_ok=True)
        plot_path = plots_dir_path + '/analyse.png'
        plt.savefig(plot_path)


if __name__ == "__main__":
    with open('./config.yml', "r") as f:
        config = yaml.safe_load(f)

    if not config.__contains__('output_dir'):
        config['output_dir'] = './output/' + str(datetime.datetime.now())
    os.makedirs(config['output_dir'], exist_ok=True)

    original_config = dict(config)
    config['show_plots'] = False
    config['save_plots'] = False
    config['save_result'] = False

    fitness_by_core_number = {}

    for core_num in range(1, 12):
        config['cores_number'] = core_num
        try:
            result = run_with_config(config)
            key = "{} core".format(core_num)
            fitness_by_core_number[key] = result['fitness_sum']
        except Exception as e:
            print("Not feasible for {}".format(core_num))
            pass

    show_chart(original_config, fitness_by_core_number)
