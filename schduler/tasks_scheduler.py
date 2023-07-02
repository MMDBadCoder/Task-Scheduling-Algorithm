from enum import Enum

from fitness_funcs import get_fitness_func
from schduler.avo import avo_algorithm
from schduler.cgo import cgo_algorithm
from schduler.job_utils import generate_jobs


class SchedulingAlgorithm(Enum):
    CGO = 1
    AVO = 2


def schedule_tasks(config, tasks):
    scheduling_time_limit = int(config['scheduling_time_limit'])
    jobs = generate_jobs(tasks, scheduling_time_limit)

    scheduling_key = SchedulingAlgorithm[config['scheduling_algorithm']]
    fitness_func = get_fitness_func(config)

    scheduling_alg = None
    if scheduling_key is SchedulingAlgorithm.CGO:
        scheduling_alg = cgo_algorithm
    elif scheduling_key is SchedulingAlgorithm.AVO:
        scheduling_alg = avo_algorithm

    best_schedule = scheduling_alg(config, jobs, fitness_func)

    fitness_value = fitness_func(best_schedule)
    return best_schedule, fitness_value
