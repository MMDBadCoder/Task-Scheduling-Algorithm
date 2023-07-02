from enum import Enum


class SchedulingAlgorithm(Enum):
    ONLY_DEADLINE = 1


def get_fitness_func(config):
    func_key = SchedulingAlgorithm[config['fitness_func']]
    if func_key == SchedulingAlgorithm.ONLY_DEADLINE:
        return only_deadline


def only_deadline(jobs):
    f = 0
    for job in jobs:
        if job['d'] < job['s'] + job['e']:
            f += 1
    return f