from enum import Enum

deadline_penalty = 1000


class FitnessApproach(Enum):
    ONLY_DEADLINE = 1
    RESPONSE_TIME = 2
    WAIT_TIME = 3
    COMPLETION_TIME = 4
    LATENCY_TIME = 5
    SLACK_TIME = 6
    CUSTOM = 7


def get_fitness_func(config):
    func_key = FitnessApproach[config['fitness_func']]
    if func_key == FitnessApproach.ONLY_DEADLINE:
        return missed_deadlines_num
    elif func_key == FitnessApproach.RESPONSE_TIME:
        return response_time
    elif func_key == FitnessApproach.WAIT_TIME:
        return wait_time
    elif func_key == FitnessApproach.COMPLETION_TIME:
        return completion_time
    elif func_key == FitnessApproach.LATENCY_TIME:
        return latency_time
    elif func_key == FitnessApproach.SLACK_TIME:
        return slack_time
    elif func_key == FitnessApproach.CUSTOM:
        return custom_fitness


def missed_deadlines_num(jobs):
    overed_deadlines = 0
    for job in jobs:
        if job['d'] < job['s'] + job['e']:
            overed_deadlines += 1
    return overed_deadlines


def response_time(jobs):
    fitness = missed_deadlines_num(jobs) * deadline_penalty
    for job in jobs:
        fitness += job['s'] + job['e'] - job['r']
    return fitness


def wait_time(jobs):
    fitness = missed_deadlines_num(jobs) * deadline_penalty
    for job in jobs:
        fitness += job['s'] - job['r']
    return fitness


def completion_time(jobs):
    finish_times = []
    for job in jobs:
        finish_times.append(job['s'] + job['e'])
    return max(finish_times) + missed_deadlines_num(jobs) * deadline_penalty


def latency_time(jobs):
    fitness = missed_deadlines_num(jobs) * deadline_penalty
    for job in jobs:
        fitness += job['s'] + job['e'] - job['d']
    return fitness


def slack_time(jobs):
    fitness = missed_deadlines_num(jobs) * deadline_penalty
    current_time = 0
    for job in jobs:
        if current_time < job['s']:
            slack_value = job['s'] - current_time
            fitness += slack_value
        current_time = job['s'] + job['e']
    return fitness


def custom_fitness(jobs):
    return completion_time(jobs) + latency_time(jobs)
