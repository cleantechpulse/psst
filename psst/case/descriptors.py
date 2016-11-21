from __future__ import print_function
from collections import OrderedDict

from builtins import super
import six


class Descriptor(object):
    name = None
    ty = None

    def __get__(self, instance, cls):
        try:
            return instance.__dict__[self.name]
        except KeyError:
            raise AttributeError("'{}' object has no attribute {}".format(instance.__class__.__name__, self.name))

    def __set__(self, instance, value):
        if self.ty is not None and not isinstance(value, self.ty):
            value = self.ty(value)
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        raise AttributeError("Cannot delete attribute {}".format(self.name))


class Version(Descriptor):
    name = 'version'
    ty = str


class BaseMVA(Descriptor):
    name = 'baseMVA'
    ty = float


class Bus(Descriptor):
    name = 'bus'


class BusName(Descriptor):
    name = 'bus_name'


class Branch(Descriptor):
    name = 'branch'


class Gen(Descriptor):
    name = 'gen'


class GenCost(Descriptor):
    name = 'gencost'


class GenName(Descriptor):
    name = 'gen_name'


class _Attributes(Descriptor):
    name = '_attributes'
