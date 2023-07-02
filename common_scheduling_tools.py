import random
from job_utils import make_start_times_after_realise_time


def generate_random_schedules(jobs, population_size):
    population = []
    population.append(sorted(jobs, key=lambda job: job['r']))
    for _ in range(population_size - 1):
        schedule = random.sample(jobs, len(jobs))
        population.append(schedule)

    for schedule in population:
        make_start_times_after_realise_time(schedule)

    return population
