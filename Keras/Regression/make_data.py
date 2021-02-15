import csv
import math
import os
import random


def normalizerPosX(x):
    return float(x) / 52.5


def normalizerPosY(x):
    return float(x) / 34


def normalizerVel(x):  # todo no need to divide, i think
    return float(x) / 3


def normalizerAngle(x):
    return float(x) / 180


def normalizerRelPosX(x):
    return float(x) / 10


def normalizerRelPosY(x):
    return float(x) / 10


def normalizerUnum(x):
    return float(x) / 11


def normalizerNone(x):
    return float(x)


def normalizerStep(x, one_key=True):
    if one_key:
        return oneKey(int(x), 3)
    else:
        return int(x) / 3


def normalizerPossible(x):
    return int(x)


def oneKey(i, max):
    x = [0] * 4
    if i == 0:
        x[3] = 1
    else:
        x[i - 1] = 1
    return x


def findAngle(s, c):
    deg = math.asin(s) / math.pi * 180
    if c > 0:
        return deg
    else:
        if deg > 0:
            return 180 - deg
        else:
            return -180 + deg


def find_polar(x, y):
    c = (x ** 2 + y ** 2) ** 0.5
    if c == 0:
        return 0, 0, 0
    return x / c, y / c, c


def filter_step(X, Y):
    new_x = [[], [], [], []]
    new_y = [[], [], [], []]
    for i in range(len(Y)):
        n = -1
        for j in range(4):
            if Y[i][j] == 1:
                n = j
                break
        new_x[n].append(X[i])
        new_y[n].append(Y[i])

    for i in range(4):
        print(f"sizes({i}): {len(new_x[i])}, {len(new_y[i])}")

    n = min(len(new_x[0]), len(new_x[1]), len(new_x[2]), len(new_x[3]))

    return (new_x[0][:n] + new_x[1][:n] + new_x[2][:n] + new_x[3][:n],
            new_y[0][:n] + new_y[1][:n] + new_y[2][:n] + new_y[3][:n])


normalizers = {
    "pSize": normalizerNone,
    "pKickMargin": normalizerNone,
    "pKickRand": normalizerNone,
    "pKickRate": normalizerNone,
    "pKickPower": normalizerNone,
    "pBody": normalizerAngle,
    "pVelx": normalizerVel,
    "pVely": normalizerVel,
    "bRelX": normalizerNone,
    "bRelY": normalizerNone,
    "bRelDeg": normalizerAngle,
    "bRelSin": normalizerNone,
    "bRelCos": normalizerNone,
    "bRelDist": normalizerNone,
    "bVelX": normalizerNone,
    "bVelY": normalizerNone,
    "bVelSin": normalizerNone,
    "bVelCos": normalizerNone,
    "bVelR": normalizerVel,
    "tRelX": normalizerRelPosX,
    "tRelY": normalizerRelPosY,
    "tRelDeg": normalizerAngle,
    "tRelSin": normalizerNone,
    "tRelCos": normalizerNone,
    "tVel": normalizerVel,
    "oVelX": normalizerVel,
    "oVelY": normalizerVel,
    "oVelSin": normalizerNone,
    "oVelCos": normalizerNone,
    "oVelR": normalizerVel,
    "oStep": normalizerStep,
    "oPossible": normalizerPossible,
}
skip_keys = [
    "cycle",
    "pSize",
    "pKickPower",
    "bRelY",
    "bRelX",
    "bRelDeg",
    "tRelX",
    "tRelY",
    "tRelDeg",
    "oVelX",
    "oVelY",
    "oVelSin",
    "oVelCos",
    "oVelR",
    "oStep",
    "oPossible",
    "pBody",
    "bVelX",
    "bVelY",
]

y_keys = [
    # "oVelX",
    # "oVelY",
    # "oVelSin",
    # "oVelCos",
    # "oVelR",
    "oStep",
    # "oPossible"
]
not_possible_skip = False

test_percent = 0.20


def displayInfo(all_x, all_y):
    s0, s1, s2, s3 = 0, 0, 0, 0
    for y in all_y:
        if y[0] == 1:
            s1 += 1
        elif y[1] == 1:
            s2 += 1
        elif y[2] == 1:
            s3 += 1
        elif y[3] == 1:
            s0 += 1
    print(f"Y Varient: {s1}, {s2}, {s3}, {s0}")


def make_all(lst=[]):
    X_KEYS = set(normalizers) - set(skip_keys)
    print(f"X keys: "
          f"{X_KEYS}")

    all_x = []
    all_y = []

    dir = '/mnt/f/2d/data'
    os.chdir(dir)
    files = os.listdir()
    for file in files:
        if file.split('.')[-1] != 'csv':
            continue
        if file.split('.')[-2] != 'sep':
            continue
        data_file = open(file, 'r')
        csv_table = csv.DictReader(data_file)
        table = []
        for row in csv_table:
            row['tRelDeg'] = findAngle(float(row['tRelSin']), float(row['tRelCos']))
            row['bVelSin'], row['bVelCos'], row['bVelR'] = find_polar(float(row['bVelX']), float(row['bVelY']))
            table.append(row)
        s = len(table)
        first_time = True
        for i, data in enumerate(table):
            print(f"{i}/{s}")
            if first_time:
                for k in data.keys():
                    if k in X_KEYS:
                        lst.append(k)
                first_time = False
            if not_possible_skip and int(data["oPossible"]) == 0:
                continue
            new_x = [normalizers[key.strip(' ')](value)
                     for key, value
                     in data.items()
                     if key not in skip_keys + y_keys]
            new_y = [normalizers[key.strip(' ')](data[key])
                     for key in y_keys]

            all_x.append(new_x)
            all_y.append(new_y[0])

    n_data = len(new_x)
    print(f"DATA: {len(all_x)}*{n_data}")
    n_divider = n_data - int(n_data * test_percent)

    # displayInfo(all_x, all_y)
    return all_x, all_y
    # return all_x[:n_divider], all_y[:n_divider], all_x[n_divider:], all_y[n_divider:]

# make_all()
