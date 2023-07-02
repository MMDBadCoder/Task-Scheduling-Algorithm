import random

from common_scheduling_tools import generate_random_schedules


def fitness_evaluation(solution):
    # Calculate the fitness value for the solution
    # Here, the fitness value represents the total completion time of all tasks
    total_completion_time = sum(solution)
    return total_completion_time


def parent_selection(population):
    # Select parents for crossover operation
    # Here, we use tournament selection with a tournament size of 2
    parent1 = random.choice(population)
    parent2 = random.choice(population)
    return parent1, parent2


def crossover(parent1, parent2):
    # Perform crossover operation to create new solutions
    # Here, we use a simple one-point crossover
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2


def mutation(solution, mutation_rate):
    # Introduce random changes to the solution
    # Here, we randomly select a task and change its assigned core
    if random.random() < mutation_rate:
        task_index = random.randint(0, len(solution) - 1)
        new_core = random.randint(1, num_cores)
        solution[task_index] = new_core
    return solution


def replacement(population, new_solutions):
    # Replace the worst solutions in the population with the new solutions
    population.sort(key=fitness_evaluation)
    population[:len(new_solutions)] = new_solutions
    return population


def avo_algorithm(config, jobs, fitness_func):
    # Example usage
    avo_max_iterations = config['avo_max_iterations']
    avo_population_size = config['avo_population_size']
    avo_mutation_rate = config['avo_mutation_rate']

    population = generate_random_schedules(jobs, avo_population_size)

    # Perform AVO iterations
    for _ in range(avo_max_iterations):
        # Evaluate fitness for each solution in the population
        fitness_values = [fitness_evaluation(solution) for solution in population]

        # Select parents for crossover
        parent1, parent2 = parent_selection(population)

        # Perform crossover operation
        child1, child2 = crossover(parent1, parent2)

        # Perform mutation on the new solutions
        child1 = mutation(child1, mutation_rate)
        child2 = mutation(child2, mutation_rate)

        # Replace the worst solutions in the population with the new solutions
        population = replacement(population, [child1, child2])

    # Get the best solution from the final population
    best_solution = min(population, key=fitness_evaluation)
