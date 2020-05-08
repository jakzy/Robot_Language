import sys
from Parser.parser import Parser
from typing import List, Dict, Optional
from syntax_tree import Node

# Item of symbol table
class Variable:
    def __init__(self, var_type='NUMERIC', var_value=None):
        self.type = var_type
        if self.type == 'LOGIC':
            if var_value == "FALSE":
                self.value = bool(False)
            elif var_value == "TRUE":
                self.value = bool(True)
            else:
                self.value = var_value
        else:
            self.value = var_value

    def __repr__(self):
        return f'{self.type}, {self.value}'


class Interpreter:

    def __init__(self, _parser=Parser()):
        self.parser = _parser
        self.sym_table = None
        self.scope = 0
        self.program = None
        self.fatal_error = False
        self.find_exit = False
        self.tree = None
        self.procs: Dict[str, Node] = dict()
        self.recs: Dict[str, Node] = dict()

    def interpreter(self,  program=None):
        self.program = program
        self.sym_table = [dict()]
        self.tree, _correctness = self.parser.parse(self.program)
        if _correctness:
            self.interpreter_tree(self.tree)
            self.interpreter_node(self.tree)
        else:
            sys.stderr.write(f'Can\'t intemperate incorrect input file\n')

    @staticmethod
    def interpreter_tree(_tree):
        print("Program tree:\n")
        _tree.print()
        print("\n")

    def interpreter_node(self, node):
        if node is None:
            return
        # program
        if node.type == 'program':
            self.interpreter_node(node.child)

        # program -> statements
        elif node.type == 'statements':
            for ch in node.child:
                self.interpreter_node(ch)

        elif node.type == 'error':
            self.error.call(self.error_types['UnexpectedError'], node)

        # STATEMENTS BLOCK

        # statements -> declaration
        elif node.type == 'declaration':
            declaration_type = node.value
            declaration_child = node.child
            if (declaration_type in ['NUMERIC', 'LOGIC', 'STRING']) or (declaration_type in self.recs):
                self.declare_variable(declaration_child, declaration_type)
            else:
                sys.stderr.write(f'Can\'t declare the variable: illegal type\n')


        # statements -> record
        elif node.type == 'record_description':
            if node.value in self.recs.keys():
                sys.stderr.write(f'Can\'t redeclare the record\n')
            elif (node.value in self.procs.keys()) or (node.value in self.sym_table[self.scope].keys()):
                sys.stderr.write(f'Can\'t declare the record: name is taken\n')
            else:
                self.recs[node.value] = self.parser.get_recs()[node.value]

        # for declaration

    def declare_variable(self, node, _type):
        if node.type == 'variable':
            if (node.value in self.recs.keys()) or (node.value in self.procs.keys()) or (node.value in self.sym_table[self.scope].keys()):
                sys.stderr.write(f'The name is already taken\n')
            else:
                self.declare(_type, node.value)
            return

    def declare(self, _type, _value):
        if (_value in self.recs.keys()) or (_value in self.procs.keys()) or (_value in self.sym_table[self.scope].keys()):
            sys.stderr.write(f'The variable is already declared\n')
        if (_type in ['NUMERIC', 'LOGIC', 'STRING']) or (_type in self.recs.keys()):
            self.sym_table[self.scope][_value] = Variable(_type, None)

if __name__ == '__main__':
    f = open("tiny_test.txt")
    #f = open(r'lexer_test.txt')
    #f = open(r'bubble_sort.txt')
    text = f.read()
    f.close()
    interpr = Interpreter()
    interpr.interpreter(text)
    for sym_table in interpr.sym_table:
        for keys, values in sym_table.items():
            if keys == "#result":
                continue
            if isinstance(values, Variable):
                print(values.type, keys, '=', values.value)
