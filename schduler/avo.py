import random

from schduler.job_utils import make_start_times_sorted, generate_random_schedules, mutate_order, mutate_job, \
    get_k_best_items



def crossover(parent1, parent2):
    sum_of_job_index = {}

    def get_id_of_job(job):
        return str(job['t']['id']) + '-' + str(job['r'])

    def add_index_to_dict(schedule):
        for index, job in enumerate(schedule):
            sum_of_job_index[get_id_of_job(job)] += index

    for job in parent1:
        sum_of_job_index[get_id_of_job(job)] = 0

    add_index_to_dict(parent1)
    add_index_to_dict(parent2)

    child = sorted(parent1, key=lambda job: sum_of_job_index[get_id_of_job(job)])
    make_start_times_sorted(child)
    return child


def avo_algorithm(config, jobs, fitness_func):
    avo_max_iterations = config['avo_max_iterations']
    avo_population_size = config['avo_population_size']

    population = generate_random_schedules(jobs, avo_population_size)

    for _ in range(avo_max_iterations):
        parent1 = random.choice(population)
        parent2 = random.choice(population)

        # Perform crossover operation
        child1 = crossover(parent1, parent2)

        child2 = mutate_job(child1)
        child3 = mutate_order(child1)

        population.append(child1)
        population.append(child2)
        population.append(child3)

        population = get_k_best_items(population, fitness_func, len(population))

    # Get the best solution from the final population
    best_schedule = min(population, key=lambda s: fitness_func(s))
    return best_schedule
