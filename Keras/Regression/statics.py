import os
import time
import tracemalloc

USAGE_DEBUG = True
JUST_SEP = True


def is_csv(file_name):
    ext = file_name.split('.')[-1]
    if not JUST_SEP:
        if ext == 'csv':
            return True
        return False
    else:
        ext = file_name.split('.')[-1]
        sep = file_name.split('.')[-2]
        if ext == 'csv' and sep == 'sep':
            return True
        return False


def main():
    dir = '/mnt/f/2d/data'
    os.chdir(dir)
    files = os.listdir()
    print(files)

    steps = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
    }

    if USAGE_DEBUG:
        start_time = time.time()
        tracemalloc.start()

    for file_name in files:
        if not is_csv(file_name):
            continue
        file = open(file_name)
        headers = file.readline().split(',')
        print(headers)
        for line in file:
            data = dict([(d, h) for d, h in zip(headers, line.split(','))])
            steps[int(data["oStep"])] += 1

    n_data = sum(steps.values())
    print(f"N: {n_data}")
    for k in steps:
        print(f"{k}: {steps[k]} | {steps[k] / n_data * 100:.2f}%")

    if USAGE_DEBUG:
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"TIME: {end_time - start_time}| MEM: {peak}")


if __name__ == '__main__':
    main()
