import datetime
import json
import os
import sys
import time

import yaml

from core_mapper import map_tasks_to_cores
from schedule_detail_reporter import make_report_json
from tasks_reader import read_csv_file
from tasks_scheduler import schedule_tasks
from visualise_result import visualize_task_execution


def run_with_config(config):
    start_time = time.time()

    if not config.__contains__('output_dir'):
        config['output_dir'] = './output/' + str(datetime.datetime.now())
    os.makedirs(config['output_dir'])

    if len(sys.argv) < 2:
        raise RuntimeError('You should pass path of csv file of tasks as argument')
    tasks_file_path = sys.argv[1]
    tasks = read_csv_file(tasks_file_path)

    tasks_mapping = map_tasks_to_cores(config, tasks)

    cores_num = int(config['cores_number'])
    tasks_of_core = {}
    for core_i in range(cores_num):
        tasks_of_core[core_i] = []
    for task in tasks:
        mapped_core = tasks_mapping[task['id']]
        tasks_of_core[mapped_core].append(task)

    schedules = []
    fitness_values = []
    for core_i in range(cores_num):
        schedule, fitness = schedule_tasks(config, tasks_of_core[core_i])
        schedules.append(schedule)
        fitness_values.append(fitness)

    algorithm_execution_time = time.time() - start_time

    for core_i in range(cores_num):
        visualize_task_execution(config, schedules[core_i], 'Core ' + str(core_i))

    result_json = make_report_json(schedules)
    result_json['algorithm_execution_time'] = algorithm_execution_time
    result_json['fitness_values'] = fitness_values
    report_file_path = config['output_dir'] + "/report.json"
    with open(report_file_path, 'w') as file:
        file.write(json.dumps(result_json, indent=3))


if __name__ == "__main__":
    with open('./config.yml', "r") as f:
        config = yaml.safe_load(f)
    run_with_config(config)
