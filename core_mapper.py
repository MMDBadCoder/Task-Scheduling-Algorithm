from enum import Enum


class MappingAlgorithm(Enum):
    BEST_FIT = 1
    WORST_FIT = 2
    FIRST_FIT = 3


# return a dict from task id to core number
def map_tasks_to_cores(config: dict, tasks: []):
    mapping_alg = MappingAlgorithm[config['mapping_algorithm']]
    cores_num = int(config['cores_number'])

    if mapping_alg is MappingAlgorithm.BEST_FIT:
        return _map_with_best_fit(tasks, cores_num)
    elif mapping_alg is MappingAlgorithm.WORST_FIT:
        return _map_with_worst_fit(tasks, cores_num)
    elif mapping_alg is MappingAlgorithm.FIRST_FIT:
        return _map_with_first_fit(tasks, cores_num)
    else:
        raise RuntimeError("Wrong mapping algorithm!")


def _map_with_best_fit(tasks: [], cores_num: int):
    mapped_core = {}
    util_of_core = {}
    for core_i in range(cores_num):
        util_of_core[core_i] = float(0)
    for task in tasks:
        most_free_cores = sorted(list(range(cores_num)), key=lambda c: util_of_core[c])
        selected_core = most_free_cores[0]
        if 1 - util_of_core[selected_core] < task['u']:
            raise RuntimeError('Mapping tasks to cores is not feasible by this mapping algorithm')
        mapped_core[task['id']] = selected_core
        util_of_core[selected_core] += task['u']
    return mapped_core


def _map_with_worst_fit(tasks: [], cores_num: int):
    mapped_core = {}
    util_of_core = {}
    for core_i in range(cores_num):
        util_of_core[core_i] = float(0)
    for task in tasks:
        most_full_cores = sorted(list(range(cores_num)), key=lambda c: util_of_core[c], reverse=True)
        selected_core = None
        for core_i in most_full_cores:
            if 1 - util_of_core[core_i] >= task['u']:
                selected_core = core_i
                break
        if selected_core is None:
            raise RuntimeError('Mapping tasks to cores is not feasible by this mapping algorithm')
        mapped_core[task['id']] = selected_core
        util_of_core[selected_core] += task['u']
    return mapped_core


def _map_with_first_fit(tasks: [], cores_num: int):
    mapped_core = {}
    util_of_core = {}
    for core_i in range(cores_num):
        util_of_core[core_i] = float(0)
    for task in tasks:
        selected_core = None
        for core_i in range(cores_num):
            if 1 - util_of_core[core_i] >= task['u']:
                selected_core = core_i
                break
        if selected_core is None:
            raise RuntimeError('Mapping tasks to cores is not feasible by this mapping algorithm')
        mapped_core[task['id']] = selected_core
        util_of_core[selected_core] += task['u']
    return mapped_core
