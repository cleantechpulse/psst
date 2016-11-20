# -*- coding: utf-8 -*-

"""
Python class to read a Matpower Case file
Copyright (C) 2016 Dheepak Krishnamurthy
"""

import os
from builtins import open
import logging

import numpy as np
from pyparsing import Word, nums, alphanums, LineEnd, Suppress, Literal, restOfLine, OneOrMore, Optional, Keyword, Group, printables


logger = logging.getLogger(__file__)


def parse_file(attribute, string):
    if attribute in ['gen', 'gencost', 'bus', 'branch']:
        return parse_table(attribute, string)
    elif attribute in ['version', 'baseMVA']:
        return parse_line(attribute, string)
    else:
        logger.debug("Parser for mpc.%s is not implemented. Please contact the developer", attribute)
        return None


def parse_line(attribute, string):
    Float = Word(nums + '.' + '-' + '+')
    Name = Word(alphanums)
    String = Optional(Suppress("'")) + Word(printables, alphanums) + Optional(Suppress("'"))
    NL = LineEnd()
    Comments = Suppress(Literal('%')) + restOfLine

    Grammar = Suppress(Keyword('mpc.{}'.format(attribute)) + Keyword('=')) + String('data') + Suppress(Literal(';'))
    result, i, j = Grammar.scanString(string).next()

    return [int_else_float(s) for s in result['data'].asList()]


def parse_table(attribute, string):
    Float = Word(nums + '.' + '-' + '+')
    Name = Word(alphanums)
    String = Optional(Suppress("'")) + Word(printables, alphanums) + Optional(Suppress("'"))
    NL = LineEnd()
    Comments = Suppress(Literal('%')) + restOfLine

    Line = OneOrMore(Float)('data') + Literal(';') + Optional(Comments, default='')('name')
    Grammar = Suppress(Keyword('mpc.{}'.format(attribute)) + Keyword('=') + Keyword('[') + Optional(Comments)) + OneOrMore(Group(Line)) + Suppress(Keyword(']') + Optional(Comments))

    result, i, j = Grammar.scanString(string).next()

    _list = list()
    for r in result:
        _list.append([int_else_float(s) for s in r['data'].asList()])

    return _list


def int_else_float(s):
    try:
        f = float(s)
        i = int(f)
        return i if i==f else f
    except ValueError:
        return s
