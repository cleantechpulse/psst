# -*- coding: utf-8 -*-

"""
MATPOWER module in `psst`
Copyright (C) 2016 Dheepak Krishnamurthy
"""


import os

import pandas as pd

from .case_reader import parse_file
from .utils import COLUMNS, ATTRIBUTES


class MPCDataFrame(object):
    _attributes = ATTRIBUTES

    def __init__(self, filename=None, mode='r'):
        if filename is not None:
            self._filename = filename
            if mode == 'r' or mode == 'read':
                read_matpower(self)


def read_matpower(mpc):

    if not isinstance(mpc, MPCDataFrame):
        filename = mpc
        mpc = MPCDataFrame(filename)

    with open(os.path.abspath(mpc._filename)) as f:
        string = f.read()

    for attribute in mpc._attributes:
        _list = parse_file(attribute, string)
        if _list is not None:
            if len(_list) == 1:
                setattr(mpc, attribute, _list[0])
            else:
                cols = _max_cols(_list)
                columns = COLUMNS.get(attribute, [i for i in range(0, cols)])
                columns = columns[:cols]
                if cols > len(columns):
                    columns = columns[:-1] + ['{}_{}'.format(columns[-1], i) for i in range(0, cols - len(columns) + 1)]
                df = pd.DataFrame(_list, columns=columns)
                setattr(mpc, attribute, df)

    return mpc


def _max_cols(_list):
    return max([len(l) for l in _list])


def write_matpower(mpc):
    NotImplementedError("write_matpower is not implemented yet")


