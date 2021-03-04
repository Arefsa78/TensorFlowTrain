import csv
import math
import os
import random
import pandas
from multiprocessing import Pool


def normalizerPosX(row, c):
    return row[c] / 52.5


def normalizerPosY(row, c):
    return row[c] / 34


def normalizerVel(row, c):  # todo no need to divide, i think
    return row[c] / 3


def normalizerAngle(row, c):
    return row[c] / 180


def normalizerRelPosX(row, c):
    return row[c] / 10


def normalizerRelPosY(row, c):
    return row[c] / 10


def normalizerUnum(row, c):
    return row[c] / 11



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
    "pSize": None,
    "pKickMargin": None,
    "pKickRand": None,
    "pKickRate": None,
    "pKickPower": None,
    "pDecay": None,
    "pBody": normalizerAngle,
    "pVelx": normalizerVel,
    "pVely": normalizerVel,
    "bRelX": None,
    "bRelY": None,
    "bRelDeg": normalizerAngle,
    "bRelSin": None,
    "bRelCos": None,
    "bRelDist": None,
    "bVelX": None,
    "bVelY": None,
    "bVelSin": None,
    "bVelCos": None,
    "bVelR": normalizerVel,
    "tRelX": normalizerRelPosX,
    "tRelY": normalizerRelPosY,
    "tRelDeg": normalizerAngle,
    "tRelSin": None,
    "tRelCos": None,
    "tVel": normalizerVel,
    "oVelX": normalizerVel,
    "oVelY": normalizerVel,
    "oVelSin": None,
    "oVelCos": None,
    "oVelR": normalizerVel,
    "oStep": None,
    "oPossible": None,
}
skip_keys = [
    "cycle",
    "pSize",
    # "pKickPower",
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
    # "oStep",
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


def find_angle(row):
    s = row['tRelSin']
    c = row['tRelCos']
    deg = math.asin(s) / math.pi * 180
    if c > 0:
        return deg
    else:
        if deg > 0:
            return 180 - deg
        else:
            return -180 + deg


def find_polar(row):
    x = row['bVelX']
    y = row['bVelY']
    c = (x ** 2 + y ** 2) ** 0.5
    if c == 0:
        return 0, 0, 0

    return x / c, y / c, c


def normalize_file(arr):
    path = arr[0]
    file = arr[1]
    print(path, file)
    df = pandas.read_csv(os.path.join(path, file))

    df['tRelDeg'] = df.apply(find_angle, axis=1)

    df[['bVelSin', 'bVelCos', 'bVelR']] = df.apply(find_polar, axis=1, result_type="expand")
    if not_possible_skip:
        df = df[df['oPossible'] != 0]
    df_y = df[y_keys[0]]
    df = df.drop(columns=skip_keys + y_keys, axis=1)
    for c in df.columns:
        if normalizers[c] is not None:
            df[c] = df.apply(normalizers[c], axis=1, args=[c])
    out_file_name = file.split('.')[0]
    df.to_csv(os.path.join(path, 'input_normal_' + out_file_name + '.csv'), index=False)
    df_y.to_csv(os.path.join(path, 'output_normal_' + out_file_name + '.csv'), index=False)


def make_all_new():
    path = './data'
    files = os.listdir(path)
    sep_files = []
    for file in files:
        if file.split('.')[-1] != 'csv':
            continue
        if file.split('.')[-2] != 'sep':
            continue
        if not file in ['kick-1613589756.sep.csv', 'kick-1613589770.sep.csv']:
            continue
        sep_files.append([path, file])
    pool = Pool(2)
    pool.map(normalize_file, sep_files)


make_all_new()
