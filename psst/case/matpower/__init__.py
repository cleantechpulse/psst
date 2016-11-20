# -*- coding: utf-8 -*-

"""
MATPOWER module in `psst`
Copyright (C) 2016 Dheepak Krishnamurthy
"""
from __future__ import print_function, absolute_import

import re
import logging
import os

import pandas as pd

from .reader import parse_file, find_attributes
from .utils import COLUMNS
from ...utils import int_else_float_except_string

logging.basicConfig()
logger = logging.getLogger(__file__)


class MPC(object):
    def __init__(self, filename=None, mode='r'):
        self._attributes = []
        if filename is not None:
            self._filename = filename
            if mode == 'r' or mode == 'read':
                self._read_matpower(self)

    @classmethod
    def _read_matpower(cls, mpc):

        if not isinstance(mpc, cls):
            filename = mpc
            mpc = cls(filename, mode=None)

        with open(os.path.abspath(mpc._filename)) as f:
            string = f.read()

        for attribute in find_attributes(string):
            _list = parse_file(attribute, string)
            if _list is not None:
                if len(_list) == 1:
                    setattr(mpc, attribute, _list[0][0])
                else:
                    cols = max([len(l) for l in _list])
                    columns = COLUMNS.get(attribute, [i for i in range(0, cols)])
                    columns = columns[:cols]
                    if cols > len(columns):
                        columns = columns[:-1] + ['{}_{}'.format(columns[-1], i) for i in range(0, cols - len(columns) + 1)]
                    df = pd.DataFrame(_list, columns=columns)
                    setattr(mpc, attribute, df)
                mpc._attributes.append(attribute)

        return mpc

    def _write_matpower(cls, filename, mpc=None):
        NotImplementedError('MATPOWER case writer is not implemented. Please contact the developer')


read_matpower = MPC._read_matpower
write_matpower = MPC._write_matpower
