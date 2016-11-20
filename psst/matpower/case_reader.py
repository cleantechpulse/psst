# -*- coding: utf-8 -*-

"""
Python class to read a Matpower Case file
Copyright (C) 2016 Dheepak Krishnamurthy
"""

import os
from builtins import open

import numpy as np
from pyparsing import Word, nums, alphanums, LineEnd, Suppress, Literal, restOfLine, OneOrMore, Optional, Keyword, Group, printables


def parse_file(attribute, string):
    if attribute in ['gen', 'gencost', 'bus', 'branch']:
        return parse_table(attribute, string)
    else:
        return parse_line(attribute, string)


def parse_line(attribute, string):
    Float = Word(nums + '.' + '-' + '+')
    Name = Word(alphanums)
    String = Optional(Suppress("'")) + Word(printables, alphanums) + Optional(Suppress("'"))
    NL = LineEnd()
    Comments = Suppress(Literal('%')) + restOfLine

    Grammar = Suppress(Keyword('mpc.{}'.format(attribute)) + Keyword('=')) + String('data') + Suppress(Literal(';'))
    result, i, j = Grammar.scanString(string).next()

    return result['data'].asList()


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
    f = float(s)
    i = int(f)
    return i if i==f else f
