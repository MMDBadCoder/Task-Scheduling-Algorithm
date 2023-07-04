import yaml

from main import run_with_config

if __name__ == "__main__":
    with open('./config.yml', "r") as f:
        config = yaml.safe_load(f)
        config['show_plots'] = False
        config['save_plots'] = False
        config['save_result'] = False

    fitness_by_core_number = {}

    for core_num in range(1, 16):
        config['cores_number'] = core_num
        try:
            result = run_with_config(config)
            fitness_by_core_number[core_num] = result['fitness_sum']
        except Exception as e:
            print("Not feasible for {}".format(core_num))
            pass

    print(fitness_by_core_number)
