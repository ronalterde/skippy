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

import anytree

class ScpiCompleter:
    def __init__(self, root_node):
        self.root_node = root_node

    def complete(self, prefix):
        """Returns list of matches"""
        prefix_list = prefix.split(':')
        last_node_before_leaf = self._walk_until_last_node_before_leaf(prefix_list)
        if last_node_before_leaf == None:
            return []
        return self._make_matches_from_leaf_nodes(last_node_before_leaf, prefix_list[-1])

    def _walk_until_last_node_before_leaf(self, prefix_list):
        start = self.root_node
        for item in prefix_list[:-1]:
            start = anytree.find(start, lambda node: node.name == item, maxlevel=2)
            if start == None:
                return None
        return start

    def _make_matches_from_leaf_nodes(self, last_node_before_leaf, prefix):
        nodes = anytree.findall(last_node_before_leaf, lambda node: node.name.startswith(prefix), maxlevel=2)
        matches = []
        for node in nodes:
            if node != last_node_before_leaf:
                this_match = ":".join([i.name for i in node.path if i.name != ''])
                if len(node.children) != 0:
                    this_match = this_match + ':'
                matches = matches + [this_match]
        return matches

class ReadlineAdapter:
    """Adapter for GNU Readline completion
    GNU Readline completion expects a complete() function and calls it until None is returned.
    (as opposed to just getting a list of completions for a given prefix)
    """

    def __init__(self, target_function):
        self.target_function = target_function

    def complete(self, prefix, index):
        try:
            return self.target_function(prefix)[index]
        except IndexError:
            return None

