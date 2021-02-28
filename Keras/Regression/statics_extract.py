import os
import time
import tracemalloc
import random

USAGE_DEBUG = True


def is_csv(file_name, just_sep):
    ext = file_name.split('.')[-1]
    if not just_sep:
        if ext == 'csv':
            return True
        return False
    else:
        ext = file_name.split('.')[-1]
        sep = file_name.split('.')[-2]
        if ext == 'csv' and sep == 'sep':
            return True
        return False


def write_line(out_file, line):
    out_file.write(f'{line}')


def create_out_file_name(file_name):
    spr = file_name.split('.')
    spr = spr[:-1] + ['sep'] + [spr[-1]]
    return '.'.join(spr)


def main1():
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
        if not is_csv(file_name, False):
            continue
        file = open(file_name)
        headers = file.readline().split(',')
        print(headers)
        for line in file:
            data = dict([(d, h) for d, h in zip(headers, line.split(','))])
            steps[int(data["oStep"])] += 1

        file.close()

    n_data = sum(steps.values())
    print(f"N: {n_data}")
    for k in steps:
        print(f"{k}: {steps[k]} | {steps[k] / n_data * 100:.2f}%")

    if USAGE_DEBUG:
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"TIME: {end_time - start_time}| MEM: {peak}")

    return steps


def main2(steps):
    dir = '/mnt/f/2d/data'
    os.chdir(dir)
    files = os.listdir()

    n_data = sum(steps.values())
    min_type = min(steps.values())

    r_steps = {}
    for k in steps:
        r_steps[k] = min_type / steps[k]

    if USAGE_DEBUG:
        start_time = time.time()
        tracemalloc.start()

    for file_name in files:
        if not is_csv(file_name, False):
            continue
        out_file = open(create_out_file_name(file_name), 'w')
        file = open(file_name)
        line = file.readline()
        headers = line.split(',')
        write_line(out_file, line)
        for line in file:
            data = dict([(d, h) for d, h in zip(headers, line.split(','))])
            if random.random() < r_steps[int(data["oStep"])]:
                write_line(out_file, line)

    if USAGE_DEBUG:
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"TIME: {end_time - start_time}| MEM: {peak}")


if __name__ == '__main__':
    steps = main1()  # find out Numbers
    main2(steps)  # save equal data
