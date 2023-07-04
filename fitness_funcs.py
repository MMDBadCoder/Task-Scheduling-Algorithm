from enum import Enum


class FitnessApproach(Enum):
    ONLY_DEADLINE = 1
    RESPONSE_TIME = 2
    WAIT_TIME = 3


def get_fitness_func(config):
    func_key = FitnessApproach[config['fitness_func']]
    if func_key == FitnessApproach.ONLY_DEADLINE:
        return only_deadline
    elif func_key == FitnessApproach.RESPONSE_TIME:
        return response_time
    elif func_key == FitnessApproach.WAIT_TIME:
        return wait_time


def only_deadline(jobs):
    overed_deadlines = 0
    for job in jobs:
        if job['d'] < job['s'] + job['e']:
            overed_deadlines += 1
    return overed_deadlines


def response_time(jobs):
    fitness = only_deadline(jobs) * 1000
    for job in jobs:
        fitness += job['s'] + job['e'] - job['r']
    return fitness


def wait_time(jobs):
    fitness = only_deadline(jobs) * 1000
    for job in jobs:
        fitness += job['s'] - job['r']
    return fitness
