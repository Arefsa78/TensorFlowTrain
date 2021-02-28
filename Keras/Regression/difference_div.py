import os
import time
import tracemalloc

USAGE_DEBUG = True
JUST_SEP = False


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

    n = 0
    dic = {}
    for i in range(4):
        for j in range(4):
            if i == j:
                continue

            dic[(i, j)] = 0

    if USAGE_DEBUG:
        start_time = time.time()
        tracemalloc.start()

    for file_name in files:
        if not is_csv(file_name):
            continue
        file = open(file_name)
        headers = file.readline().split(',')
        print(headers)
        last_data = None
        for line in file:
            data = dict([(d, h) for d, h in zip(headers, line.split(','))])
            if last_data is None:
                last_data = data
                continue

            if last_data['cycle'] != f"#{data['cycle']}":
                last_data = data
                continue

            if last_data['oStep'] == data['oStep']:
                last_data = data
                continue
            n += 1
            dic[int(last_data['oStep']), int(data['oStep'])] += 1
            last_data = data
            print(n)

    for k, v in dic.items():
        print(f"({k[0]}, {k[1]}): {v}")
    if USAGE_DEBUG:
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"TIME: {end_time - start_time}| MEM: {peak}")


if __name__ == '__main__':
    main()
