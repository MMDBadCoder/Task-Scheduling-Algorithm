import random


def generate_jobs(tasks, time_limit):
    jobs = []
    for task in tasks:
        current_time = 0
        while current_time < time_limit:
            job = {
                'r': current_time,
                's': current_time,
                'e': task['e'],
                'd': current_time + task['p'],
                't': task
            }
            jobs.append(job)
            current_time += task['p']
    return jobs


def make_start_times_sorted(schedule):
    schedule = clone_schedule(schedule)
    current_time = 0
    for job in schedule:
        job['s'] = max(current_time, job['r'], job['s'])
        current_time = job['s'] + job['e']
    return schedule


def generate_random_schedules(jobs, population_size):
    population = []
    population.append(make_start_times_sorted(jobs))
    for _ in range(population_size - 1):
        schedule = random.sample(jobs, len(jobs))
        schedule = make_start_times_sorted(schedule)
        population.append(schedule)

    return population


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
    schedule = make_start_times_sorted(schedule)
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
    schedule = make_start_times_sorted(schedule)
    return schedule


def clone_schedule(schedule):
    return [dict(j) for j in schedule]


def get_k_best_items(population, fitness_func, k):
    return sorted(population, key=lambda s: fitness_func(s))[:k]
