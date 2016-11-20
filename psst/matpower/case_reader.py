from __future__ import print_function, absolute_import

import re
import logging

import numpy as np

from ..utils import int_else_float_except_string

logging.basicConfig()
logger = logging.getLogger(__file__)


def find_attributes(string):
    pattern = 'mpc\.(?P<attribute>.*?)\s*=\s*'
    return re.findall(pattern, string, re.DOTALL)


def parse_file(attribute, string):

    match = search_file(attribute, string)

    if match is not None:
        match = match.strip("'").strip('"')

        _list = list()
        for line in match.splitlines():
            line = line.split('%')[0]
            if line.strip():
                _list.append([int_else_float_except_string(s) for s in line.strip().strip(';').strip().split()])

        return _list
    else:
        return match


def search_file(attribute, string):

    if attribute in ['gen', 'gencost', 'bus', 'branch'] and attribute in string:
        pattern = 'mpc\.{}\s*=\s*\[[\n]?(?P<data>.*?)[\n]?\];'.format(attribute)
    elif attribute in ['version', 'baseMVA'] and attribute in string:
        pattern = 'mpc\.{}\s*=\s*(?P<data>.*?);'.format(attribute)
    else:
        logger.warning('Unable to parse mpc.%s. Please contact the developer.', attribute)
        return None

    match = re.search(pattern, string, re.DOTALL)
    if match is not None:
        return match.groupdict().get('data', None)
    else:
        return match


