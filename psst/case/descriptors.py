from __future__ import print_function
from collections import OrderedDict
import logging

from builtins import super
import six

import pandas as pd


logger = logging.getLogger(__name__)
logging.basicConfig()


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
        if self._is_valid(instance, value):
            instance.__dict__[self.name] = value
        else:
            raise AttributeError('Validation for {} failed. Please check {}'.format(self.name, value))

    def __delete__(self, instance):
        raise AttributeError("Cannot delete attribute {}".format(self.name))

    def _is_valid(self, instance, value):
        return True


class IndexDescriptor(Descriptor):

    def __get__(self, instance, cls):
        try:
            index = self.getattributeindex(instance)
            return index
        except AttributeError:
            super().__get__(instance, cls)

    def __set__(self, instance, value):
        if isinstance(value, pd.Series) or isinstance(value, list):
            value = pd.Index(value)
        elif isinstance(value, pd.DataFrame):
            # Assume the first column in the dataframe as index.
            value = pd.Index(value.iloc[:, 0].rename(self.name))

        try:
            self.setattributeindex(instance, value)
        except AttributeError:
            logger.debug('AttributeError on instance.{} when setting index as {}'.format(self.name.replace('_name', ''), self.name))

        super().__set__(instance, value)

    def getattributeindex(self, instance):
        raise AttributeError('IndexDescriptor does not have attribute')

    def setattributeindex(self, instance):
        raise AttributeError('IndexDescriptor does not have attribute')


class Name(Descriptor):
    name = 'name'
    ty = str


class Version(Descriptor):
    name = 'version'
    ty = str


class BaseMVA(Descriptor):
    name = 'baseMVA'
    ty = float


class Bus(Descriptor):
    name = 'bus'
    ty = pd.DataFrame


class BusName(IndexDescriptor):
    name = 'bus_name'
    ty = pd.Index

    def getattributeindex(self, instance):
        return instance.bus.index

    def setattributeindex(self, instance, value):
        # instance.bus.index = value
        pass


class Branch(Descriptor):
    name = 'branch'
    ty = pd.DataFrame


class BranchName(IndexDescriptor):
    name = 'branch_name'
    ty = pd.Index

    def getattributeindex(self, instance):
        return instance.branch.index

    def setattributeindex(self, instance, value):
        instance.branch.index = value


class Gen(Descriptor):
    name = 'gen'
    ty = pd.DataFrame


class GenCost(Descriptor):
    name = 'gencost'
    ty = pd.DataFrame


class GenName(IndexDescriptor):
    name = 'gen_name'
    ty = pd.Index

    def getattributeindex(self, instance):
        try:
            if not all(instance.gen.index == instance.gencost.index):
                logger.warning('Indices for attributes `gen` and `gencost` do not match. `gen` index will be mapped to `gencost` index')
                instance.gencost.index = instance.gen.index
        except AttributeError:
            logger.debug('Unable to map `gen` indices to `gencost`')
        return instance.gen.index

    def setattributeindex(self, instance, value):
        instance.gen.index = value
        instance.gencost.index = value


class _Attributes(Descriptor):
    name = '_attributes'
    ty = list
