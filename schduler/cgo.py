from schduler.job_utils import generate_random_schedules, mutate_job, mutate_order, clone_schedule, get_k_best_items


def cgo_algorithm(config, jobs, fitness_func):
    if len(jobs) == 0:
        return []

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
                all_mutated_schedules += mutate_job(schedule)
            for j in range(cgo_order_mutation_size):
                all_mutated_schedules.append(mutate_order(schedule))

        population = get_k_best_items(all_mutated_schedules, fitness_func, len(population))

    # Select the best schedule as the result
    best_schedule = population[0]
    return best_schedule
