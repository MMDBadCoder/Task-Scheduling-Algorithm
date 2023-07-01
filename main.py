import sys

import yaml

from core_mapper import MappingAlgorithm, map_tasks_to_cores
from tasks_reader import read_csv_file

if __name__ == "__main__":

    with open('./config.yml', "r") as f:
        config = yaml.safe_load(f)

    if len(sys.argv) < 2:
        raise RuntimeError('You should pass path of csv file of tasks as argument')
    tasks_file_path = sys.argv[1]
    tasks = read_csv_file(tasks_file_path)

    mapping_alg = MappingAlgorithm[config['mapping_algorithm']]
    cores_num = int(config['cores_number'])

    tasks_mapping = map_tasks_to_cores(tasks, cores_num, mapping_alg)
    print(tasks_mapping)
