# -*- coding: utf-8 -*-

"""
MATPOWER module in `psst`
Copyright (C) 2016 Dheepak Krishnamurthy
"""


import os

import pandas as pd

from .case_reader import parse_file
from .utils import COLUMNS, ATTRIBUTES


class MPC(object):
    _attributes = ATTRIBUTES

    def __init__(self, filename, mode='r'):
        self._filename = filename
        if mode == 'r' or mode == 'read':
            read_matpower(self)


class MPCDataFrame(object):
    _attributes = ATTRIBUTES


def to_dataframe(mpc):
    mpc_df = MPCDataFrame()
    for attribute in mpc_df._attributes:
        array = getattr(mpc, attribute, None)
        if array is not None:
            if array.size == 1:
                setattr(mpc_df, attribute, array.tostring())
            else:
                columns = COLUMNS.get(attribute, [i for i in range(0, array.shape[1])])
                columns = columns[:array.shape[1]]
                if array.shape[1] > len(columns):
                    columns = columns[:-1] + ['{}_{}'.format(columns[-1], i) for i in range(0, array.shape[1] - len(columns) + 1)]
                df = pd.DataFrame(array, columns=columns)
                setattr(mpc_df, attribute, df)
    return mpc_df


def read_matpower(mpc):

    if isinstance(mpc, MPC):
        filename = mpc._filename
    else:
        filename = mpc
        mpc = MPC(filename)

    with open(os.path.abspath(mpc._filename)) as f:
        string = f.read()
    string = string + '\n\n'

    for attribute in mpc._attributes:
        array = parse_file(attribute, string)
        if array is not None:
            setattr(mpc, attribute, array)

    return mpc


def write_matpower(mpc):
    NotImplementedError("write_matpower is not implemented yet")


