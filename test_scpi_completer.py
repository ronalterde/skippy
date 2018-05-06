#!/usr/bin/env python3

# skippy - SCPI shell with readline-based line-editing
# Copyright (C) 2018  Steffen Ronalter
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
from scpi_completer import ScpiCompleter, ReadlineAdapter
from anytree import Node


class ScpiCompleterTest(unittest.TestCase):
    def setUp(self):
        self._build_test_tree()

    def _build_test_tree(self):
        self.root_node = Node('')
        stat = Node('stat', parent=self.root_node)
        stat_ques = Node('ques', parent=stat)
        stat_ques_cond = Node('cond', parent=stat_ques)
        syst = Node('syst', parent=self.root_node)
        syst_err = Node('err', parent=syst)
        syst_err_all = Node('all', parent=syst_err)
        syst_err_foo = Node('foo', parent=syst_err)
        syst_err_all_baz = Node('baz', parent=syst_err_all)
        foo = Node('foo', parent=self.root_node)
        bar = Node('bar', parent=self.root_node)

    def test_first_level(self):
        completer = ScpiCompleter(self.root_node)
        self.assertEqual(completer.complete(''), ['stat:', 'syst:', 'foo', 'bar'])
        self.assertEqual(completer.complete('s'), ['stat:', 'syst:'])
        self.assertEqual(completer.complete('st'), ['stat:'])
        self.assertEqual(completer.complete('sy'), ['syst:'])

    def test_second_level(self):
        completer = ScpiCompleter(self.root_node)
        self.assertEqual(completer.complete('stat:'), ['stat:ques:'])
        self.assertEqual(completer.complete('syst:'), ['syst:err:'])

    def test_third_level(self):
        completer = ScpiCompleter(self.root_node)
        self.assertEqual(completer.complete('stat:ques:'), ['stat:ques:cond'])
        self.assertEqual(completer.complete('syst:err:'), ['syst:err:all:', 'syst:err:foo'])

    def test_fourth_level(self):
        completer = ScpiCompleter(self.root_node)
        self.assertEqual(completer.complete('syst:err:all:'), ['syst:err:all:baz'])

    def test_empty_matches_if_no_completion_found(self):
        completer = ScpiCompleter(self.root_node)
        self.assertEqual(completer.complete('a'), [])
        self.assertEqual(completer.complete('a:b'), [])
        self.assertEqual(completer.complete('a:b:'), [])


class ReadlineAdapterTest(unittest.TestCase):
    def setUp(self):
        self.root_node = Node('')
        foo = Node('foo', parent=self.root_node)
        bar = Node('bar', parent=self.root_node)
        self.completer = ScpiCompleter(self.root_node)

    def test_one_match(self):
        adapter = ReadlineAdapter(self.completer.complete)
        self.assertEqual('foo', adapter.complete('f', 0))
        self.assertEqual(None, adapter.complete('f', 1))

    def test_two_matches(self):
        adapter = ReadlineAdapter(self.completer.complete)
        self.assertEqual('foo', adapter.complete('', 0))
        self.assertEqual('bar', adapter.complete('', 1))
        self.assertEqual(None, adapter.complete('', 2))
