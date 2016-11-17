# -*- coding: utf-8 -*-

"""
Python class to read a Matpower Case file
Copyright (C) 2016 Dheepak Krishnamurthy
"""



import os
import re
from builtins import open

import numpy as np


def parse_file(attribute, string):

    match = search_file(attribute, string)

    if match is not None:
        match = match.strip("'").strip('"')

        _list = list()
        for line in match.splitlines():
            if line.strip():
                _list.append(line.strip().strip(';').strip().split())

        array = np.array(_list)
        return array
    else:
        return match


def search_file(attribute, string):
    pattern = 'mpc\.{}\s*=\s*[\[]?[\n]?(?P<data>.*?)[\n]?[\]]?;\n\n'.format(attribute)

    match = re.search(pattern, string, re.DOTALL )
    if match is not None:
        return match.groupdict().get('data', None)
    else:
        return match


