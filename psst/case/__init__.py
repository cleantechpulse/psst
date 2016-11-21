import os
from builtins import super
import pandas as pd

from .descriptors import (Name, Version, BaseMVA, BusName, Bus, Branch, BranchName,
                        Gen, GenName, GenCost, _Attributes)

from . import matpower


class PSSTCase(object):

    name = Name()
    version = Version()
    baseMVA = BaseMVA()
    bus = Bus()
    bus_name = BusName()
    branch = Branch()
    branch_name = BranchName()
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

    def __repr__(self):
        gen_name = getattr(self, 'gen_name', None)
        bus_name = getattr(self, 'bus_name', None)
        branch_name = getattr(self, 'branch_name', None)
        gen_string = '{} Generators'.format(len(gen_name)) if gen_name is not None else ''
        bus_string = '{} Buses'.format(len(bus_name)) if bus_name is not None else ''
        branch_string = '{} Branches'.format(len(branch_name)) if branch_name is not None else ''
        l = [s for s in [gen_string, bus_string, branch_string] if s != '']
        if len(l) > 1:
            repr_string = ' with ' + ', '.join(l[:-1]) + ' and ' + l[-1]
        elif len(l) == 1:
            repr_string = ' with ' + l[0]
        else:
            repr_string = ''

        return '<{}.{} object{} at {}>'.format(
                    self.__class__.__module__,
                    self.__class__.__name__,
                    repr_string,
                    hex(id(self))
                )

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

        mpc.name = matpower.find_name(string)

        return mpc


read_matpower = PSSTCase._read_matpower
