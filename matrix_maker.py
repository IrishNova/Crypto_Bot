import itertools
import numpy as np


def rng_finder(df):
    mn = min(df)
    mx = max(df)
    return mn, mx


def matrix_maker(point_a, point_b, point_c=None, poind_d=None):
    a1 = float(point_a[0])
    a2 = float(point_a[1])
    a3 = float(point_a[2])
    b1 = float(point_b[0])
    b2 = float(point_b[1])
    b3 = float(point_b[2])

    combined = list(itertools.product(np.arange(a1, a2, a3), np.arange(b1, b2, b3)))
    return combined


def matrix_starter(data):
    mkt_c_rge = list(rng_finder(data.mkt_cap_z))
    mkt_c_rge.append(0.05)
    price_rge = list(rng_finder(data.price_z))
    price_rge.append(0.05)
    x = matrix_maker(mkt_c_rge, price_rge)
    return x
