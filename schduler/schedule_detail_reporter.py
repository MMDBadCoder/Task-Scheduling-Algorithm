from statistics import mean

from fitness_funcs import missed_deadlines_num


def make_report_json(schedules):
    jobs = []
    for schedule in schedules:
        jobs += schedule

    params = {
        'wait_time': [],
        'response_time': [],
        'delay_time': [],
        'finish_time': [],
        'start_time': []
    }

    for schedule in schedules:
        for job in schedule:
            params['wait_time'].append(job['s'] - job['r'])
            params['response_time'].append(job['s'] + job['e'] - job['r'])
            params['delay_time'].append(max(0, job['s'] + job['e'] - job['d']))
            params['finish_time'].append(job['s'] + job['e'])
            params['start_time'].append(job['s'])

    statistics = {
        'avg_wait_time': mean(params['wait_time']),
        'sum_wait_time': sum(params['wait_time']),
        'avg_response_time': mean(params['response_time']),
        'sum_response_time': sum(params['response_time']),
        'avg_delay_time': mean(params['delay_time']),
        'sum_delay_time': sum(params['delay_time']),
        'avg_finish_time': mean(params['finish_time']),
        'sum_finish_time': sum(params['finish_time']),
        'avg_start_time': mean(params['start_time']),
        'sum_start_time': sum(params['start_time'])
    }

    slack = {
        'sum': 0
    }
    for schedule in schedules:
        current_time = 0
        last_job = None
        for job in schedule:
            if current_time < job['s']:
                slack_value = job['s'] - current_time
                slack['sum'] += slack_value
                if last_job is not None:
                    slack_label = 'slack between task {} and {}'.format(job['t']['id'], last_job['t']['id'])
                    if not slack.__contains__(slack_label):
                        slack[slack_label] = 0
                    slack[slack_label] += slack_value
            current_time = job['s'] + job['e']
            last_job = job

    missed_deadlines = 0
    for schedule in schedules:
        missed_deadlines += missed_deadlines_num(schedule)

    return {
        'stat': statistics,
        'slack': slack,
        'missed deadlines': missed_deadlines
    }
