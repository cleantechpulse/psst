from collections import OrderedDict

from builtins import super
import six


class Descriptor(object):
    def __init__(self, name=None):
        self.name = name

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        raise AttributeError("Cannot delete attribute {}".format(self.name))


class List(Descriptor):
    pass


class String(Descriptor):
    pass


class Float(Descriptor):
    pass


class StringList(Descriptor):
    pass


class DataFrame(Descriptor):
    pass
