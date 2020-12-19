import csv
import os


def normalizerPosX(x):
    return float(x) / 52.5


def normalizerPosY(x):
    return float(x) / 34


def normalizerVel(x):  # todo no need to divide, i think
    return float(x)


def normalizerAngle(x):
    return float(x) / 180


def normalizerRelPosX(x):
    return float(x) / 10


def normalizerRelPosY(x):
    return float(x) / 10


def normalizerUnum(x):
    return float(x) / 11


normalizers = {
    "selfunum": normalizerUnum,
    "selfposx": normalizerRelPosX,
    "selfposy": normalizerRelPosY,
    "selfvelx": normalizerVel,
    "selfvely": normalizerVel,
    "selfbody": normalizerAngle,
    "ballposx": normalizerPosX,
    "ballposy": normalizerPosY,
    "ballvelx": normalizerVel,
    "ballvely": normalizerVel,
    "oppu": normalizerUnum,
    "opppos1x": normalizerRelPosX,
    "opppos1y": normalizerRelPosY,
    "opppos2x": normalizerRelPosX,
    "opppos2y": normalizerRelPosY,
    "oppvelx": normalizerVel,
    "oppvely": normalizerVel,
    "oppbody": normalizerAngle,
}

skip_keys = [
    'cycle',
    'selfunum',
    'selfvelx',
    'selfvely',
    'oppu',
    'opppos2x',
    'opppos2y',
]
y_keys = [
    'opppos2x',
    'opppos2y',
]

test_percent = 0.20


def make_all():
    all_x = []
    all_y = []

    dir = '/mnt/f/2d/train-hold-ball/TensorFlowTrain/data'
    os.chdir(dir)
    files = os.listdir()
    for file in files:
        data_file = open(file, 'r')
        csv_table = csv.DictReader(data_file)
        table = []
        row_tmp = list()
        for row in csv_table:
            if row['cycle'] == 'state change':
                if len(row_tmp) > 2:
                    table.append(row_tmp)
                row_tmp = list()
            else:
                row_tmp.append(row)

        for sets in table:
            for i, data in enumerate(sets[:-1]):
                new_x = [normalizers[key](value)
                         for key, value
                         in data.items()
                         if key not in skip_keys]
                new_y = [normalizers[key](sets[i + 1][key])
                         for key in y_keys]

                all_x.append(new_x)
                all_y.append(new_y)

    n_data = len(new_x)
    print(f"DATA: {len(all_x)}*{n_data}")
    n_divider = n_data - int(n_data * test_percent)
    return all_x, all_y
    # return all_x[:n_divider], all_y[:n_divider], all_x[n_divider:], all_y[n_divider:]

make_all()