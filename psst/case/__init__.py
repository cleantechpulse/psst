import os
import six
import pandas as pd

from .descriptors import (Version, BaseMVA, BusName, Bus, Branch,
                        Gen, GenName, GenCost, _Attributes)

from . import matpower


class PSSTCase(object):

    version = Version()
    baseMVA = BaseMVA()
    bus = Bus()
    bus_name = BusName()
    branch = Branch()
    gen = Gen()
    gencost = GenCost()
    gen_name = GenName()
    _attributes = _Attributes()

    def __init__(self, filename, mode='r'):
        self._attributes = list()
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

        for attribute in matpower.find_attributes(string):
            _list = matpower.parse_file(attribute, string)
            if _list is not None:
                if len(_list) == 1:
                    setattr(mpc, attribute, _list[0][0])
                else:
                    cols = max([len(l) for l in _list])
                    columns = matpower.COLUMNS.get(attribute, [i for i in range(0, cols)])
                    columns = columns[:cols]
                    if cols > len(columns):
                        columns = columns[:-1] + ['{}_{}'.format(columns[-1], i) for i in range(0, cols - len(columns) + 1)]
                    df = pd.DataFrame(_list, columns=columns)
                    setattr(mpc, attribute, df)
                mpc._attributes.append(attribute)

        return mpc


read_matpower = PSSTCase._read_matpower
