#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from unittest import TestCase
from datetime import datetime

from pygithub3.resources.base import Resource, Raw, json
from pygithub3.tests.utils.resources import Nested, Simple, HasSimple

simple_resource = dict(type='simple')
has_simple = dict(type='has_simple', simple=simple_resource)
github_return = dict(
    id=1,
    name='name_test',
    date='2008-01-14T04:33:35Z',
    simple=simple_resource,
    list_collection=[has_simple] * 2,
    items_collections=dict(arg1=has_simple, arg2=has_simple)
    )


class TestResourceMapping(TestCase):

    def setUp(self):
        self.r = Nested.loads(github_return)

    def test_attrs_map(self):
        self.assertEqual(self.r.id, 1)
        self.assertEqual(self.r.name, 'name_test')
        self.assertEqual(self.r.date, datetime(2008, 1, 14, 4, 33, 35))

    def test_MAPS(self):
        self.assertIsInstance(self.r.simple, Simple)
        self.assertEqual(self.r.simple.type, 'simple')

    def test_LIST_collection_map(self):
        has_simple_objects = filter(lambda x: isinstance(x, HasSimple),
                                    self.r.list_collection)
        self.assertEqual(len(has_simple_objects), 2)
        self.assertEqual(self.r.list_collection[0].type, 'has_simple')
        self.assertEqual(self.r.list_collection[0].simple.type, 'simple')

    def test_DICT_collection_map(self):
        arg1_has_simple = self.r.items_collections['arg1']
        self.assertEqual(arg1_has_simple.type, 'has_simple')
        self.assertEqual(arg1_has_simple.simple.type, 'simple')


class TestRawResource(TestCase):
    """ Litle obvious :P """

    def test_return_original_copy(self):
        self.r = Raw.loads(github_return)
        self.assertEqual(id(self.r), id(github_return))