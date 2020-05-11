import sys
from Parser.parser import Parser
from typing import List, Dict, Optional
from syntax_tree import Node

# Item of symbol table
class Variable:
    def __init__(self, var_type='UNDEF', var_value=None):
        if var_value == "UNDEF":
            var_value = None
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


class UserConversion:
    def __init__(self):
        self.TO: Dict[str, Node] = dict()
        self.FROM: Dict[str, Node] = dict()


# Conversion of types
class Conversion:
    def __init__(self):
        self.user_conversions: Dict[str, UserConversion] = dict()

    def converse_(self, var, _type):
        if _type == var.type:
            return var
        if _type == 'LOGIC':
            if var.type == 'NUMERIC':
                return self.num_to_logic(var)
            if var.type == 'STRING':
                return self.string_to_logic(var)
        if _type == 'NUMERIC':
            if var.type == 'LOGIC':
                return self.logic_to_num(var)
            if var.type == 'STRING':
                return self.string_to_num(var)
        if _type == 'STRING':
            if var.type == 'LOGIC':
                return self.logic_to_string(var)
            if var.type == 'NUMERIC':
                return self.num_to_string(var)
        else:
            print('LATER')

    def add_converse(self, _type_from, _type_to, _func):
        pass

    @staticmethod
    def logic_to_num(value):
        if value.value == bool(True):
            return Variable('NUMERIC', 1)
        elif value.value == bool(False):
            return Variable('NUMERIC', 0)
        elif value.value == 'UNDEF':
            return Variable('NUMERIC', 'UNDEF')
        else:
            sys.stderr.write(f'Illegal conversion\n')

    @staticmethod
    def num_to_logic(value):
        if int(value.value) == 0:
            return Variable('LOGIC', False)
        elif isinstance(value.value, int):
            return Variable('LOGIC', True)
        elif value.value == 'UNDEF':
            return Variable('LOGIC', 'UNDEF')
        else:
            sys.stderr.write(f'Illegal conversion\n')

    @staticmethod
    def string_to_logic(value):
        if value.value.lower() == "true":
            return Variable('LOGIC', bool(True))
        elif value.value in ['UNDEF', None]:
            return Variable('LOGIC', None)
        else:
            return Variable('LOGIC', bool(False))

    @staticmethod
    def logic_to_string(value):
        return Variable('STRING', str(value.value))

    @staticmethod
    def string_to_num(value):
        if len(value.value) == 1:
            return Variable('NUMERIC', ord(value.value))
        else:
            return Variable('NUMERIC', 0)

    @staticmethod
    def num_to_string(value):
        return Variable('STRING', str(value.value))


class Interpreter:

    def __init__(self, _parser=Parser(), _converse=Conversion()):
        self.parser = _parser
        self.converse = _converse
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
        print("Program tree:")
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

        # statements -> procedure
        elif node.type == 'procedure_description':
            if node.value in self.procs.keys():
                sys.stderr.write(f'Can\'t redeclare the procedure\n')
            elif (node.value in self.procs.keys()) or (node.value in self.sym_table[self.scope].keys()):
                sys.stderr.write(f'Can\'t declare the procedure: name is taken\n')
            else:
                self.procs[node.value] = self.parser.get_proc()[node.value]

        # statements -> assignment
        elif node.type == 'assignment':
            variable = node.value.value
            if variable not in self.sym_table[self.scope].keys():
                sys.stderr.write(f'Undeclared variable\n')
            else:
                _type = self.sym_table[self.scope][variable].type
                expression = self.interpreter_node(node.child)
                self.assign(_type, variable, expression)
                #what s this?
                self.sym_table[self.scope]['#result'] = expression
                return expression

        # EXPRESSION BLOCK

        # expression -> const
        elif node.type == 'const':
            return self.const_val(node.value)

    # for assign
    def assign(self, _type, variable, expression: Variable):
        if expression is None:
            return
        expression = self.converse.converse_(expression, self.sym_table[self.scope][variable].type)
        if variable not in self.sym_table[self.scope].keys():
            sys.stderr.write(f'Undeclared variable\n')
        if _type == expression.type:
            self.sym_table[self.scope][variable] = expression
        elif expression.type == 'UNDEF':
            self.sym_table[self.scope][variable].value = None

    # for const
    @staticmethod
    def const_val(value):
        if (str(value)).isdigit():
            return Variable('NUMERIC', int(value))
        elif value in ['TRUE', 'FALSE', True, False]:
            return Variable('LOGIC', value)
        elif value in ['UNDEF', None]:
            return Variable('UNDEF', None)
        else:
            return Variable('STRING', value)

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
                if values.type == 'STRING':
                    print(values.type, keys, '= \'', values.value,'\'')
                else:
                    print(values.type, keys, '=', values.value)
    print('Records:')
    print(interpr.recs)
    print('Procedures:')
    print(interpr.procs)
