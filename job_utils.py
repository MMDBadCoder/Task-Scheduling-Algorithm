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
    make_start_times_after_realise_time(jobs)
    return jobs


def make_start_times_after_realise_time(schedule):
    current_time = 0
    for job in sorted(schedule, key= lambda j: j['s']):
        job['s'] = max(current_time, job['r'], job['s'])
        current_time = job['s'] + job['e']
