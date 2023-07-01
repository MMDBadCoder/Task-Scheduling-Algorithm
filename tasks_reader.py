import csv


def read_csv_file(file_path):
    tasks = []
    incremental_id = 0
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            task = {
                'id': incremental_id,  # task id
                'e': int(row[0]),  # execution time
                'p': int(row[1]),  # period
            }
            task['u'] = float(task['e']) / float(task['p'])
            tasks.append(task)
            incremental_id += 1
    return tasks
