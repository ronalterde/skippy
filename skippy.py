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

import readline
from anytree import Node
from scpi_completer import ScpiCompleter, ReadlineAdapter
import vxi11
import argparse


def create_example_tree():
    root_node = Node('')

    # IEEE 488.2 mandatory commands
    Node('*CLS', parent=root_node)
    Node('*ESE', parent=root_node)
    Node('*ESE?', parent=root_node)
    Node('*ESR?', parent=root_node)
    Node('*IDN?', parent=root_node)
    Node('*OPC', parent=root_node)
    Node('*OPC?', parent=root_node)
    Node('*RST', parent=root_node)
    Node('*SRE', parent=root_node)
    Node('*SRE?', parent=root_node)
    Node('*STB?', parent=root_node)
    Node('*TST?', parent=root_node)
    Node('*WAI', parent=root_node)

    # SCPI-99 mandatory commands
    syst = Node('SYSTem', parent=root_node)
    syst_err = Node('ERRor', parent=syst)
    syst_err_next = Node('NEXT?', parent=syst_err) # optional
    vers = Node('VERSion?', parent=root_node)
    stat = Node('STATus', parent=root_node)
    stat_oper = Node('OPERation', parent=stat)
    stat_oper_event = Node('EVENt?', parent=stat_oper) # optional
    stat_oper_cond = Node('CONDition?', parent=stat_oper)
    stat_oper_enab = Node('ENABle', parent=stat_oper)
    stat_oper_enab_q = Node('ENABle?', parent=stat_oper)
    stat_ques = Node('QUEStionable', parent=stat)
    stat_ques_event = Node('EVENt?', parent=stat_ques) # optional
    stat_ques_cond = Node('CONDition?', parent=stat_ques)
    stat_ques_enab = Node('ENABle', parent=stat_ques)
    stat_ques_enab_q = Node('ENABle?', parent=stat_ques)
    stat_pres = Node('PRESet', parent=stat)

    return root_node


def parse_commandline_args():
    arg_parser = argparse.ArgumentParser(description='skippy -- SCPI shell with readline-based auto-completion')
    arg_parser.add_argument('hostname', help='host name or IP of the target device')
    args = arg_parser.parse_args()
    return args


def init_readline():
    readline.parse_and_bind("tab: complete")
    readline.set_completer_delims(' \t\n')

    completer = ScpiCompleter(create_example_tree())
    adapter = ReadlineAdapter(completer.complete)
    readline.set_completer(adapter.complete)


def is_question(command):
    return len(command) > 0 and command[-1] == '?'


if __name__ == "__main__":
    args = parse_commandline_args()
    init_readline()
    instrument = vxi11.Instrument(args.hostname)

    while True:
        user_input = input("skippy@{}> ".format(args.hostname))
        if is_question(user_input):
            reply = instrument.ask(user_input)
            print(reply)
        else:
            instrument.write(user_input)
