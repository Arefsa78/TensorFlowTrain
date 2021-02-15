import os
import time
import tracemalloc
import random

USAGE_DEBUG = True


def is_csv(file_name):
    ext = file_name.split('.')[-1]
    sep = file_name.split('.')[-2]
    if ext == 'csv' and sep != 'sep':
        return True
    return False


def create_out_file_name(file_name):
    spr = file_name.split('.')
    spr = spr[:-1] + ['sep'] + [spr[-1]]
    return '.'.join(spr)


def write_line(out_file, line):
    out_file.write(f'{line}')


def main():
    dir = '/mnt/f/2d/data'
    os.chdir(dir)
    files = os.listdir()

    steps = {
        0: 157258,
        1: 2539401,
        2: 337313,
        3: 166028,
    }
    n_data = sum(steps.values())
    min_type = min(steps.values())

    r_steps = {}
    for k in steps:
        r_steps[k] = min_type/steps[k]


    if USAGE_DEBUG:
        start_time = time.time()
        tracemalloc.start()

    for file_name in files:
        if not is_csv(file_name):
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
    main()
