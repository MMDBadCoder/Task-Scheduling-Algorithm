from schduler.job_utils import generate_random_schedules, mutate_job, mutate_order, clone_schedule, get_k_best_items


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

        population = get_k_best_items(all_mutated_schedules, fitness_func, len(population))

    # Select the best schedule as the result
    best_schedule = population[0]
    return best_schedule