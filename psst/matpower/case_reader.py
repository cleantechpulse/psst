# -*- coding: utf-8 -*-

"""
Python class to read a Matpower Case file
Copyright (C) 2016 Dheepak Krishnamurthy
"""



import os
from builtins import open
import numpy as np
import pandas as pd


class MPC(object):
    _attributes = ['version', 'baseMVA', 'areas', 'bus', 'gen', 'gencost', 'branch']

    def __init__(self, filename):

        self._filename = filename

        with open(os.path.abspath(self._filename)) as f:
            self._original_mpc = f.read()

        self._mpc = []
        for line in self._original_mpc.splitlines():
            self._mpc.append(line)

        self._mpc = '\n'.join(self._mpc)
        self._parse_file()

        self.gen['name'] = ["GenCo{}".format(i) for i in range(0, self.gen.shape[0])]
        self.gen.set_index('name', inplace=True)

        self.gencost['name'] = ["GenCo{}".format(i) for i in range(0, self.gen.shape[0])]
        self.gencost.set_index('name', inplace=True)

        self.gen = pd.concat([self.gen, self.gencost], axis=1)

    def _parse_file(self):

        position = {}

        for linenumber, line in enumerate(self._mpc.splitlines()):
            attribute = line.split('=')[0]
            if attribute == line or line.startswith('%'):
                continue
            else:
                attribute = attribute.strip().replace('mpc.', '')
            if 'function' in attribute:
                continue
            if attribute:
                position[attribute] = linenumber

        for attribute in position.keys():

            linenumber = position[attribute]
            columns = self._mpc.splitlines()[linenumber - 1].strip('%').strip().split('%')[0].strip().split('\t')

            line = self._mpc.splitlines()[linenumber]
            if '[' not in line:
                array = float(line.split('=')[1].strip(';').replace("'", '').strip())
                setattr(self, attribute, np.array(array))
            else:
                array = []
                for i, line in enumerate(self._mpc.splitlines()[linenumber:]):
                    if '[' in line:
                        continue
                    if ']' in line:
                        break
                    line = line.split('%')[0]
                    row = [float(item.strip().replace(';', '')) for item in line.strip(';').strip().split('\t')]

                    array.append(row)

                if attribute=='gencost':
                    columns=['cost_model', 'startup_cost', 'shutdown_cost', 'N'] + ['C{}'.format(i - 1) for i in range(np.array(array).shape[1] - 4, 0, -1)]
                setattr(self, '_columns_{}'.format(attribute), columns)
                setattr(self, attribute, pd.DataFrame(np.array(array), columns=columns))
