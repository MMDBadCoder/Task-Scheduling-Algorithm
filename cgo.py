import random

from common_scheduling_tools import generate_random_schedules
from job_utils import make_start_times_after_realise_time


def cgo_algorithm(config, jobs, fitness_func):
    cgo_max_iterations = config['cgo_max_iterations']
    cgo_population_size = config['cgo_population_size']
    cgo_job_mutation_size = config['cgo_job_mutation_size']
    cgo_order_mutation_size = config['cgo_order_mutation_size']

    population = generate_random_schedules(jobs, cgo_population_size)

    for iteration in range(cgo_max_iterations):

        all_mutated_schedules = list(population)
        for schedule in population:
            schedule = clone_schedule(schedule)
            for j in range(cgo_job_mutation_size):
                mutated_schedule = mutate_job(schedule)
                all_mutated_schedules.append(mutated_schedule)
            for j in range(cgo_order_mutation_size):
                mutated_schedule = mutate_order(schedule)
                all_mutated_schedules.append(mutated_schedule)

        population = sorted(all_mutated_schedules, key=lambda s: fitness_func(s))[:len(population)]

    # Select the best schedule as the result
    best_schedule = population[0]
    return best_schedule


def mutate_order(schedule):
    if len(schedule) <= 1:
        return schedule
    index = random.randint(0, len(schedule) - 2)
    job1 = schedule[index]
    job2 = schedule[index + 1]
    job2['s'] = job1['s']
    job1['s'] = job2['s'] + job2['e']
    schedule[index] = job2
    schedule[index + 1] = job1
    make_start_times_after_realise_time(schedule)
    return schedule


def mutate_job(schedule):
    index = random.randint(0, len(schedule) - 1)
    if bool(random.getrandbits(1)):
        # try to move schedule frontend
        if index == len(schedule) - 1 or schedule[index + 1]['s'] != schedule[index]['s'] + schedule[index]['e']:
            schedule[index]['s'] += 1
    else:
        # try to move backend
        if index == 0 or schedule[index - 1]['s'] + schedule[index - 1]['e'] != schedule[index]['s']:
            schedule[index]['s'] -= 1
    make_start_times_after_realise_time(schedule)
    return schedule


def clone_schedule(schedule):
    return [dict(j) for j in schedule]
