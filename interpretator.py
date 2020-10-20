import sys
from Parser.parser import Parser
from typing import Dict
from syntax_tree import Node
import robot as rb
import copy
import numpy as np

debug_prints = False

menu_main = ['1. Functions',
             '2. Robot',
             '3. Other',
             '0. Nothing, thank you']
menu_functions = ['1. Bubble sort',
                  '2. Fibonacci (with cycle)',
                  '3. Fibonacci (with recursion)',
                  '0. Exit']
functions_set = ['', 'tests/bubble_sort.txt',
                 'tests/fibonacci_cycle.txt',
                 'tests/fibonacci_recursion.txt']
menu_robot = ['1. Tiny map',
              '2. Big map',
              '0. Exit']
map_set = ['', 'Maps/test_map.txt',
           'Maps/big_map.txt']

menu_other = ['1. Logic operations',
              '2. Arithmetic operations',
              '3. Array operations',
              '4. Dotted operations (multi typical)',
              '5. Errors',
              '5. Syntax Errors',
              '0. Exit']
other_set = ['', 'tests/logic_operations_test.txt',
             'tests/arithm_operations_test.txt',
             'tests/arrays_test.txt',
             'tests/dotted_test.txt',
             'tests/errors.txt',
             'tests/synt_errors.txt']


class Exit(Exception):
    pass

# Item of symbol table
class Variable:
    def __init__(self, var_type='UNDEF', var_value=None, l_flag=False, r_flag=False):
        self.left = l_flag
        self.right = r_flag
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
        if self.type == 'STRING' and self.value:
            return f'{self.type},"{self.value}"'
        else:
            return f'{self.type},{self.value}'


# Conversion of types
class Conversion:

    def converse_(self, var, _type):
        if _type == var.type:
            return var
        elif _type == 'LOGIC':
            if var.type == 'NUMERIC':
                return self.num_to_logic(var)
            if var.type == 'STRING':
                return self.string_to_logic(var)
        elif _type == 'NUMERIC':
            if var.type == 'LOGIC':
                return self.logic_to_num(var)
            if var.type == 'STRING':
                return self.string_to_num(var)
        elif _type == 'STRING':
            if var.type == 'LOGIC':
                return self.logic_to_string(var)
            if var.type == 'NUMERIC':
                return self.num_to_string(var)
        elif _type == 'UNDEF':
            return var

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
        self.robot = rb.Robot()

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
        if debug_prints:
            print("Program tree:")
            _tree.print()
            print("\n")

    def interpreter_node(self, node):

        if self.robot.found_exit:
            raise Exit

        if node is None:
            return
        # program

        if node.type == 'program':
            try:
                self.interpreter_node(node.child)
            except Exit:
                pass

        # program -> statements
        elif node.type == 'statements':
            for ch in node.child:
                try:
                    self.interpreter_node(ch)
                except Exit:
                    raise Exit

        elif node.type == 'error':
            sys.stderr.write(f'UNEXPECTED ERROR\n')

        # STATEMENTS BLOCK

        # statements -> declaration
        elif node.type == 'declaration':
            declaration_type=node.value
            declaration_child=node.child
            if (declaration_type in ['NUMERIC', 'LOGIC', 'STRING']) or (declaration_type in self.recs):
                if declaration_child.type == 'component_of':
                        if declaration_type in self.recs:
                            elem=[declaration_type, copy.deepcopy(self.recs[declaration_type][0])]
                        else:
                            elem=Variable(declaration_type)
                        size=declaration_child.child.value
                        if isinstance(size, str):
                            size=(self.get_variable(size)).value
                        res=[]
                        for i in range(size):
                            res.append(copy.deepcopy(elem))
                        declaration_type = ["ARRAY", declaration_type]
                        self.declare_array(declaration_child.value, declaration_type, np.array(res))
                else:
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
                self.recs[node.value] = self.describe_record(self.parser.get_recs()[node.value])

        # statements -> procedure
        elif node.type == 'procedure_description':
            if node.value in self.procs.keys():
                sys.stderr.write(f'Can\'t redeclare the procedure\n')
            elif (node.value in self.procs.keys()) or (node.value in self.sym_table[self.scope].keys()):
                sys.stderr.write(f'Can\'t declare the procedure: name is taken\n')
            else:
                self.procs[node.value] = self.parser.get_proc()[node.value]

        # statements -> procedure call
        elif node.type == 'procedure_call':
            if not (node.value in self.procs.keys()):
                sys.stderr.write(f'Undeclared procedure\n')
            else:
                self.run_procedure(node)

        # statements -> assignment
        elif node.type == 'assignment':
            name = node.value.value
            if name not in self.sym_table[self.scope].keys():
                sys.stderr.write(f'Undeclared variable\n')
            else:
                expression = self.interpreter_node(node.child)
                if type(self.sym_table[self.scope][name]) == Variable:
                    res = self.sym_table[self.scope][name]
                elif node.value.type == 'component_of':
                    res = self.sym_table[self.scope][name]
                    index = node.value.child
                    while not isinstance(index, list):
                        res = res[1]
                        if isinstance(res, dict) and isinstance(index.value, str):
                            res = res[index.value]
                        else:
                            if isinstance(index.value, str):
                                res = res[(self.get_variable(index.value)).value]
                            else:
                                res = res[index.value]
                        index = index.child
                elif isinstance(node.value.child, dict):
                    res = self.sym_table[self.scope][name]
                    if isinstance(expression, list):
                        if res[0] == expression[0]:
                            res[1] = copy.deepcopy(expression[1])
                        else:
                            sys.stderr.write(f'DIFFERENT TYPES FOR RECORDS ARE ILLEGAL YET\n')
                        return expression
                    else:
                        index = node.value.child
                        while index:
                            if 'ARRAY' in res[0]:
                                index = node.value.child
                                if isinstance(index.value, str):
                                    index=(self.get_variable(index)).value
                                else:
                                    index=index.value
                                res=self.sym_table[self.scope][name][1]
                                res=res[index]
                                self.assign(res, expression)
                                return expression
                else:
                    if isinstance(node.value.child, list):
                        res = self.sym_table[self.scope][name][1]
                        if isinstance(expression, np.ndarray):
                            for i in range(min(len(res), len(expression))):
                                self.assign(res[i], expression[i])
                        else:
                            for i in range(len(res)):
                                self.assign(res[i], expression)
                        return expression
                    else:
                        index = node.value.child
                        if isinstance(index.value, str):
                            index = (self.get_variable(index)).value
                        else:
                            index = index.value
                        res = self.sym_table[self.scope][name][1]
                        res = res[index]
                        self.assign(res, expression)
                        return expression
                self.assign(res, expression)
                return expression


        # statements -> cycle
        elif node.type == 'cycle':
            self.op_cycle(node)

        # statements -> command
        elif node.type == 'command':
            ##########################################
            name = node.child.value
            if name not in self.sym_table[self.scope].keys():
                sys.stderr.write(f'Undeclared variable\n')
            else:
                exp = self.sym_table[self.scope][name]
                if type(self.sym_table[self.scope][name]) == Variable:
                    pass
                elif node.child.type == 'component_of':
                    index = node.child.child
                    while not isinstance(index, list):
                        exp = exp[1]
                        if isinstance(exp, dict) and isinstance(index.value, str):
                            exp = exp[index.value]
                        else:
                            if isinstance(index.value, str):
                                exp = exp[(self.get_variable(index.value)).value]
                            else:
                                exp = exp[index.value]
                        index = index.child
            ##########################################
            if node.value == 'MOVEUP':
                if exp.type == 'NUMERIC':
                    exp.value = self.robot.move_up(exp.value)
                else:
                    sys.stderr.write(f'ILLEGAL COMMAND PARAMETER TYPE')
            elif node.value == 'MOVEDOWN':
                if exp.type == 'NUMERIC':
                    exp.value = self.robot.move_down(exp.value)
                else:
                    sys.stderr.write(f'ILLEGAL COMMAND PARAMETER TYPE')
            elif node.value == 'MOVERIGHT':
                if exp.type == 'NUMERIC':
                    exp.value = self.robot.move_right(exp.value)
                else:
                    sys.stderr.write(f'ILLEGAL COMMAND PARAMETER TYPE')
            elif node.value == 'MOVELEFT':
                if exp.type == 'NUMERIC':
                    exp.value = self.robot.move_left(exp.value)
                else:
                    sys.stderr.write(f'ILLEGAL COMMAND PARAMETER TYPE')
            elif node.value == 'PINGUP':
                if exp.type == 'NUMERIC':
                    exp.value = self.robot.ping_up(exp.value)
                else:
                    sys.stderr.write(f'ILLEGAL COMMAND PARAMETER TYPE')
            elif node.value == 'PINGDOWN':
                if exp.type == 'NUMERIC':
                    exp.value = self.robot.ping_down(exp.value)
                else:
                    sys.stderr.write(f'ILLEGAL COMMAND PARAMETER TYPE')
            elif node.value == 'PINGRIGHT':
                if exp.type == 'NUMERIC':
                    exp.value = self.robot.ping_right(exp.value)
                else:
                    sys.stderr.write(f'ILLEGAL COMMAND PARAMETER TYPE')
            elif node.value == 'PINGLEFT':
                if exp.type == 'NUMERIC':
                    exp.value = self.robot.ping_left(exp.value)
                else:
                    sys.stderr.write(f'ILLEGAL COMMAND PARAMETER TYPE')
            elif node.value == 'VISION':
                if isinstance(exp, list):
                    if exp[0][1] == 'STRING':
                        pasws = self.robot.vision()
                        for i in range(len(pasws)):
                            exp[1][i].value = pasws[i]
                else:
                    sys.stderr.write(f'ILLEGAL COMMAND PARAMETER TYPE')
            elif node.value == 'VOICE':
                if exp.type == 'STRING':
                    self.robot.voice(exp.value)
                else:
                    sys.stderr.write(f'ILLEGAL COMMAND PARAMETER TYPE')
            else:
                sys.stderr.write(f'UNEXPECTED ERROR')

        # EXPRESSION BLOCK

        elif node.type == 'unary_expression':
            exp = self.interpreter_node(node.child)
            if exp.value is None:
                return Variable(exp.type)
            else:
                if exp.type == 'NUMERIC':
                    return Variable('NUMERIC', -exp.value)
                elif exp.type == 'LOGIC':
                    return Variable('LOGIC', not exp.value)
                else:
                    sys.stderr.write(f'Illegal operation: illegal type\n')
                    return Variable()

        # expression -> complex_expression
        elif node.type == 'binary_expression':
            exp1 = self.interpreter_node(node.child[0])
            exp2 = self.interpreter_node(node.child[1])
            if debug_prints:
                print()
                print('exp1: ' + str(exp1))
                print('exp2: ' + str(exp2))
            if node.value == '+':
                result = self.bin_plus(exp1, exp2)
            elif node.value == '-':
                result = self.bin_minus(exp1, exp2)
            elif node.value == '*':
                result = self.bin_star(exp1, exp2)
            elif node.value == '/':
                result = self.bin_slash(exp1, exp2)
            elif node.value == '^':
                result = self.bin_caret(exp1, exp2)
            elif node.value == '>':
                result = self.bin_greater(exp1, exp2)
            elif node.value == '<':
                result = self.bin_less(exp1, exp2)
            elif node.value == '?':
                result = self.bin_equal(exp1, exp2)
            elif node.value == '!':
                result = self.bin_not_equal(exp1, exp2)
            if type(exp1) == Variable:
                if exp1.right:
                    result.right = True
                if exp2.left:
                    result.left = True
            return result

        # binary_expression -> part_expression
        elif node.type == 'part_expression':
            exp = self.interpreter_node(node.child)
            if type(exp) == Variable:
                if exp:
                    if node.value:
                        if node.value == "right":
                            exp.right = True
                            if debug_prints:
                                print('right up')
                        elif node.value == "left":
                            exp.left = True
                            if debug_prints:
                                print('left up')
            else:
                for elem in exp:
                    if node.value:
                        if node.value == "right":
                            elem.right=True
                            if debug_prints:
                                print('right up')
                        elif node.value == "left":
                            elem.left = True
                            if debug_prints:
                                print('left up')
            return exp

        # expression -> const
        elif node.type == 'const':
            return self.const_val(node.value)

        # expression -> variable
        elif node.type == 'variable':
            return self.get_value(node)

        # expression -> component_of
        elif node.type == 'component_of':
            return self.get_component(node)

    # for assign
    def assign(self, variable: Variable, expression: Variable):
        if expression is None:
            return
        expression = self.converse.converse_(expression, variable.type)
        if expression:
            if variable.type == expression.type:
                variable.value = expression.value
            elif expression.type == 'UNDEF':
                variable.value = None
        else:
            variable.value = None

    # for cycle
    def op_cycle(self, node):
        while self.converse.converse_(self.interpreter_node(node.child['condition']), 'LOGIC').value:
            self.interpreter_node(node.child['body'])

    #### BINARY EXPRESSIONS ####
    # binary plus -- ADDITION or OR
    def bin_plus(self, _val1, _val2):
        no_error = True
        res_type = 'UNDEF'
        if type(_val1) == list:
            _val1=_val1[1]
            res=copy.deepcopy(_val1)
            if type(_val2) == list:
                _val2=_val2[1]
                for i in range(min(len(_val1), len(_val2))):
                    res[i] = self.bin_plus(_val1[i], _val2[i])
            else:
                for i in range(len(_val1)):
                    res[i] = self.bin_plus(_val1[i], _val2)
            return res
        else:
            if (_val1.type == 'UNDEF') and not (_val2.type == 'UNDEF'):
                _val1.type = _val2.type
            if (_val2.type == 'UNDEF') and not (_val1.type == 'UNDEF'):
                _val2.type = _val1.type
            if (_val2.type == 'UNDEF') and (_val1.type == 'UNDEF'):
                return Variable()
            x1 = _val1.value
            x2 = _val2.value
            if _val1.type == _val2.type:
                if _val1.type == "NUMERIC":
                    return Variable('NUMERIC', x1 + x2)
                elif _val1.type == "LOGIC":
                    if (x1 != None) and (x2 != None):
                        return Variable('LOGIC', bool(x1) or bool(x2))
                    else:
                        if x1 or x2:
                            return Variable('LOGIC', True)
                        else:
                            return Variable('LOGIC', None)

                elif _val1.type == "STRING":
                    no_error = False
                    sys.stderr.write(f'Illegal operation: type STRING\n')
            else:
                if _val1.left and _val2.right:
                    no_error = False
                    sys.stderr.write(f'Illegal operation: type conversion double definition is illegal\n')
                elif _val1.left:
                    res_type = _val1.type
                    _val1.left = False
                elif _val2.right:
                    res_type = _val2.type
                    _val2.right = False
                else:
                    no_error = False
                    sys.stderr.write(f'Illegal operation: type conversion required\n')
                if no_error:
                    if res_type == "NUMERIC":
                        return Variable('NUMERIC', self.converse.converse_(_val1, 'NUMERIC').value + self.converse.converse_(_val2, 'NUMERIC').value)
                    elif res_type == "LOGIC":
                        x1 = bool(self.converse.converse_(_val1, 'LOGIC').value)
                        x2 = bool(self.converse.converse_(_val2, 'LOGIC').value)
                        if (x1 != None) and (x2 != None):
                            return Variable('LOGIC', bool(x1) or bool(x2))
                        else:
                            if x1 or x2:
                                return Variable('LOGIC', True)
                            else:
                                return Variable('LOGIC', None)
                    elif res_type == "STRING":
                        sys.stderr.write(f'Illegal operation: type STRING\n')

    # binary minus -- SUBTRACTION or XOR
    def bin_minus(self, _val1, _val2):
        no_error=True
        res_type='UNDEF'
        if type(_val1) == np.ndarray:
            res=copy.deepcopy(_val1)
            if type(_val2) == np.ndarray:
                for i in range(min(len(_val1), len(_val2))):
                    res[i]=self.bin_minus(_val1[i], _val2[i])
            else:
                for i in range(len(_val1)):
                    res[i]=self.bin_minus(_val1[i], _val2)
            return res
        else:
            if (_val1.type == 'UNDEF') and not (_val2.type == 'UNDEF'):
                _val1.type=_val2.type
            if (_val2.type == 'UNDEF') and not (_val1.type == 'UNDEF'):
                _val2.type=_val1.type
            if (_val2.type == 'UNDEF') and (_val1.type == 'UNDEF'):
                return Variable()
            x1=_val1.value
            x2=_val2.value
            if _val1.type == _val2.type:
                if _val1.type == "NUMERIC":
                    return Variable('NUMERIC', x1 - x2)
                elif _val1.type == "LOGIC":
                    if (x1 != None) and (x2 != None):
                        return Variable('LOGIC', (bool(x1) and not bool(x2)) or (bool(x2) and not bool(x1)))
                    else:
                        return Variable('LOGIC', None)
                elif _val1.type == "STRING":
                    no_error=False
                    sys.stderr.write(f'Illegal operation: type STRING\n')
            else:
                if _val1.left and _val2.right:
                    no_error=False
                    sys.stderr.write(f'Illegal operation: type conversion double definition is illegal\n')
                elif _val1.left:
                    res_type=_val1.type
                    _val1.left=False
                elif _val2.right:
                    res_type=_val2.type
                    _val2.right=False
                else:
                    no_error=False
                    sys.stderr.write(f'Illegal operation: type conversion required\n')
                if no_error:
                    if res_type == "NUMERIC":
                        return Variable('NUMERIC',
                                        self.converse.converse_(_val1, 'NUMERIC').value + self.converse.converse_(_val2,
                                                                                                                  'NUMERIC').value)
                    elif res_type == "LOGIC":
                        x1=bool(self.converse.converse_(_val1, 'LOGIC').value)
                        x2=bool(self.converse.converse_(_val2, 'LOGIC').value)
                        if (x1 != None) and (x2 != None):
                            return Variable('LOGIC', (bool(x1) and not bool(x2)) or (bool(x2) and not bool(x1)))
                        else:
                            return Variable('LOGIC', None)
                    elif res_type == "STRING":
                        sys.stderr.write(f'Illegal operation: type STRING\n')

    # binary star -- MULTIPLICATION or AND
    def bin_star(self, _val1, _val2):
        no_error = True
        res_type='UNDEF'
        if type(_val1) == list:
            _val1 = _val1[1]
            res=copy.deepcopy(_val1)
            if type(_val2) == list:
                _val2 = _val2[1]
                for i in range(min(len(_val1), len(_val2))):
                    res[i]=self.bin_star(_val1[i], _val2[i])
            else:
                for i in range(len(_val1)):
                    res[i]=self.bin_star(_val1[i], _val2)
            return res
        else:
            if (_val1.type == 'UNDEF') and not (_val2.type == 'UNDEF'):
                _val1.type = _val2.type
            if (_val2.type == 'UNDEF') and not (_val1.type == 'UNDEF'):
                _val2.type = _val1.type
            if (_val2.type == 'UNDEF') and (_val1.type == 'UNDEF'):
                return Variable()
            x1 = _val1.value
            x2 = _val2.value
            if _val1.type == _val2.type:
                if _val1.type == "NUMERIC":
                    return Variable('NUMERIC', x1 * x2)
                elif _val1.type == "LOGIC":
                    if (x1 != None) and (x2 != None):
                        return Variable('LOGIC', bool(x1) or bool(x2))
                    else:
                        if (not x1 or not x2) or (x1 == x2):
                            return Variable('LOGIC', None)
                        else:
                            return Variable('LOGIC', False)

                elif _val1.type == "STRING":
                    no_error = False
                    sys.stderr.write(f'Illegal operation: type STRING\n')
            else:
                if _val1.left and _val2.right:
                    no_error = False
                    sys.stderr.write(f'Illegal operation: type conversion double definition is illegal\n')
                elif _val1.left:
                    res_type = _val1.type
                    _val1.left = False
                elif _val2.right:
                    res_type = _val2.type
                    _val2.right = False
                else:
                    no_error = False
                    sys.stderr.write(f'Illegal operation: type conversion required\n')
                if no_error:
                    if res_type == "NUMERIC":
                        return Variable('NUMERIC', self.converse.converse_(_val1, 'NUMERIC').value + self.converse.converse_(_val2, 'NUMERIC').value)
                    elif res_type == "LOGIC":
                        x1 = bool(self.converse.converse_(_val1, 'LOGIC').value)
                        x2 = bool(self.converse.converse_(_val2, 'LOGIC').value)
                        if (x1 != None) and (x2 != None):
                            return Variable('LOGIC', bool(x1) or bool(x2))
                        else:
                            if (not x1 or not x2) or (x1 == x2):
                                return Variable('LOGIC', None)
                            else:
                                return Variable('LOGIC', False)
                    elif res_type == "STRING":
                        sys.stderr.write(f'Illegal operation: type STRING\n')

    # binary slash -- DIVISION or NAND (Sheffer's stroke)
    def bin_slash(self, _val1, _val2):
        no_error = True
        res_type = 'UNDEF'
        if type(_val1) == np.ndarray:
            res=copy.deepcopy(_val1)
            if type(_val2) == np.ndarray:
                for i in range(min(len(_val1), len(_val2))):
                    res[i] = self.bin_slash(_val1[i], _val2[i])
            else:
                for i in range(len(_val1)):
                    res[i]=self.bin_slash(_val1[i], _val2)
            return res
        else:
            if (_val1.type == 'UNDEF') and not (_val2.type == 'UNDEF'):
                _val1.type = _val2.type
            elif (_val2.type == 'UNDEF') and not (_val1.type == 'UNDEF'):
                _val2.type = _val1.type
            elif (_val2.type == 'UNDEF') and (_val1.type == 'UNDEF'):
                return Variable()
            x1 = _val1.value
            x2 = _val2.value
            if _val1.type == _val2.type:
                if _val1.type == "NUMERIC":
                    return Variable('NUMERIC', x1 // x2)
                elif _val1.type == "LOGIC":
                    if (x1 != None) and (x2 != None):  #bcoz False and None are too close
                        return Variable('LOGIC', not(bool(x1) and bool(x2)))
                    else:
                        if (x1 or x2) or (x1 == x2):
                            return Variable('LOGIC', None)
                        else:
                            return Variable('LOGIC', True)

                elif _val1.type == "STRING":
                    no_error = False
                    sys.stderr.write(f'Illegal operation: type STRING\n')
            else:
                if _val1.left and _val2.right:
                    no_error = False
                    sys.stderr.write(f'Illegal operation: type conversion double definition is illegal\n')
                elif _val1.left:
                    res_type = _val1.type
                    _val1.left = False
                elif _val2.right:
                    res_type = _val2.type
                    _val2.right = False
                else:
                    no_error = False
                    sys.stderr.write(f'Illegal operation: type conversion required\n')
                if no_error:
                    if res_type == "NUMERIC":
                        return Variable('NUMERIC', self.converse.converse_(_val1, 'NUMERIC').value + self.converse.converse_(_val2, 'NUMERIC').value)
                    elif res_type == "LOGIC":
                        x1 = bool(self.converse.converse_(_val1, 'LOGIC').value)
                        x2 = bool(self.converse.converse_(_val2, 'LOGIC').value)
                        if (x1 != None) and (x2 != None):
                            return Variable('LOGIC', not (bool(x1) or bool(x2)))
                        else:
                            if (x1 or x2) or (x1 == x2):
                                return Variable('LOGIC', None)
                            else:
                                return Variable('LOGIC', True)
                    elif res_type == "STRING":
                        sys.stderr.write(f'Illegal operation: type STRING\n')

    # binary caret -- EXPONENTIATION or NOR (Peirce's arrow)
    def bin_caret(self, _val1, _val2):
        no_error=True
        res_type='UNDEF'
        if type(_val1) == np.ndarray:
            res=copy.deepcopy(_val1)
            if type(_val2) == np.ndarray:
                for i in range(min(len(_val1), len(_val2))):
                    res[i]=self.bin_caret(_val1[i], _val2[i])
            else:
                for i in range(len(_val1)):
                    res[i]=self.bin_caret(_val1[i], _val2)
            return res
        else:
            if (_val1.type == 'UNDEF') and not (_val2.type == 'UNDEF'):
                _val1.type=_val2.type
            elif (_val2.type == 'UNDEF') and not (_val1.type == 'UNDEF'):
                _val2.type=_val1.type
            elif (_val2.type == 'UNDEF') and (_val1.type == 'UNDEF'):
                return Variable()
            x1 = _val1.value
            x2 = _val2.value
            if _val1.type == _val2.type:
                if _val1.type == "NUMERIC":
                    return Variable('NUMERIC', x1 ** x2)
                elif _val1.type == "LOGIC":
                    if (x1 != None) and (x2 != None):
                        return Variable('LOGIC', not (bool(x1) or bool(x2)))
                    else:
                        if (x1 == x2) or (x1 == False) or (x2 == False):
                            return Variable('LOGIC', None)
                        else:
                            return Variable('LOGIC', False)

                elif _val1.type == "STRING":
                    no_error = False
                    sys.stderr.write(f'Illegal operation: type STRING\n')
            else:
                if _val1.left and _val2.right:
                    no_error=False
                    sys.stderr.write(f'Illegal operation: type conversion double definition is illegal\n')
                elif _val1.left:
                    res_type=_val1.type
                    _val1.left=False
                elif _val2.right:
                    res_type=_val2.type
                    _val2.right=False
                else:
                    no_error=False
                    sys.stderr.write(f'Illegal operation: type conversion required\n')
                if no_error:
                    if res_type == "NUMERIC":
                        return Variable('NUMERIC',
                                        self.converse.converse_(_val1, 'NUMERIC').value + self.converse.converse_(_val2,
                                                                                                                  'NUMERIC').value)
                    elif res_type == "LOGIC":
                        x1=bool(self.converse.converse_(_val1, 'LOGIC').value)
                        x2=bool(self.converse.converse_(_val2, 'LOGIC').value)
                        if (x1 != None) and (x2 != None):
                            return Variable('LOGIC', not (bool(x1) and bool(x2)))
                        else:
                            if (x1 == x2) or (x1 == False) or (x2 == False):
                                return Variable('LOGIC', None)
                            else:
                                return Variable('LOGIC', False)
                    elif res_type == "STRING":
                        sys.stderr.write(f'Illegal operation: type STRING\n')

    def bin_greater(self, _val1, _val2):
        no_error=True
        res_type='LOGIC'
        if type(_val1) == np.ndarray:
            res=copy.deepcopy(_val1)
            if type(_val2) == np.ndarray:
                for i in range(min(len(_val1), len(_val2))):
                    res[i]=self.bin_greater(_val1[i], _val2[i])
            else:
                for i in range(len(_val1)):
                    res[i]=self.bin_greater(_val1[i], _val2)
            return res
        else:
            if (_val1.type == 'UNDEF') and not (_val2.type == 'UNDEF'):
                _val1.type=_val2.type
            elif (_val2.type == 'UNDEF') and not (_val1.type == 'UNDEF'):
                _val2.type=_val1.type
            elif (_val2.type == 'UNDEF') and (_val1.type == 'UNDEF'):
                return Variable()
            x1=_val1.value
            x2=_val2.value
            if _val1.type == _val2.type:
                return Variable('LOGIC', x1 > x2)
            else:
                if _val1.left and _val2.right:
                    no_error=False
                    sys.stderr.write(f'Illegal operation: type conversion double definition is illegal\n')
                elif _val1.left:
                    res_type=_val1.type
                    _val1.left=False
                elif _val2.right:
                    res_type=_val2.type
                    _val2.right=False
                else:
                    no_error=False
                    sys.stderr.write(f'Illegal operation: type conversion required\n')
                if no_error:
                    return Variable('LOGIC', self.converse.converse_(_val1, res_type).value > self.converse.converse_(_val2, res_type).value)

    def bin_less(self, _val1, _val2):
        no_error=True
        res_type='LOGIC'
        if type(_val1) == np.ndarray:
            res=copy.deepcopy(_val1)
            if type(_val2) == np.ndarray:
                for i in range(min(len(_val1), len(_val2))):
                    res[i]=self.bin_less(_val1[i], _val2[i])
            else:
                for i in range(len(_val1)):
                    res[i]=self.bin_less(_val1[i], _val2)
            return res
        else:
            if (_val1.type == 'UNDEF') and not (_val2.type == 'UNDEF'):
                _val1.type=_val2.type
            elif (_val2.type == 'UNDEF') and not (_val1.type == 'UNDEF'):
                _val2.type=_val1.type
            elif (_val2.type == 'UNDEF') and (_val1.type == 'UNDEF'):
                return Variable()
            x1=_val1.value
            x2=_val2.value
            if _val1.type == _val2.type:
                return Variable('LOGIC', x1 < x2)
            else:
                if _val1.left and _val2.right:
                    no_error=False
                    sys.stderr.write(f'Illegal operation: type conversion double definition is illegal\n')
                elif _val1.left:
                    res_type=_val1.type
                    _val1.left=False
                elif _val2.right:
                    res_type=_val2.type
                    _val2.right=False
                else:
                    no_error=False
                    sys.stderr.write(f'Illegal operation: type conversion required\n')
                if no_error:
                    return Variable('LOGIC', self.converse.converse_(_val1, res_type).value < self.converse.converse_(_val2, res_type).value)

    def bin_equal(self, _val1, _val2):
        no_error=True
        res_type='LOGIC'
        if type(_val1) == list:
            _val1=_val1[1]
            res=copy.deepcopy(_val1)
            if type(_val2) == list:
                _val2=_val2[1]
                for i in range(min(len(_val1), len(_val2))):
                    res[i]=self.bin_equal(_val1[i], _val2[i])
            else:
                for i in range(len(_val1)):
                    res[i]=self.bin_equal(_val1[i], _val2)
            return res
        else:
            if (_val1.type == 'UNDEF') and not (_val2.type == 'UNDEF'):
                _val1.type = _val2.type
            if (_val2.type == 'UNDEF') and not (_val1.type == 'UNDEF'):
                _val2.type = _val1.type
            if (_val2.type == 'UNDEF') and (_val1.type == 'UNDEF'):
                return Variable()
            x1 = _val1.value
            x2 = _val2.value
            if _val1.type == _val2.type:
                return Variable('LOGIC', x1 == x2)
            else:
                if _val1.left and _val2.right:
                    no_error=False
                    sys.stderr.write(f'Illegal operation: type conversion double definition is illegal\n')
                elif _val1.left:
                    res_type=_val1.type
                    _val1.left=False
                elif _val2.right:
                    res_type=_val2.type
                    _val2.right=False
                else:
                    no_error=False
                    sys.stderr.write(f'Illegal operation: type conversion required\n')
                if no_error:
                    return Variable('LOGIC', self.converse.converse_(_val1, res_type).value == self.converse.converse_(_val2, res_type).value)

    def bin_not_equal(self, _val1, _val2):
        no_error=True
        res_type='LOGIC'
        if type(_val1) == np.ndarray:
            res=copy.deepcopy(_val1)
            if type(_val2) == np.ndarray:
                for i in range(min(len(_val1), len(_val2))):
                    res[i]=self.bin_not_equal(_val1[i], _val2[i])
            else:
                for i in range(len(_val1)):
                    res[i]=self.bin_not_equal(_val1[i], _val2)
            return res
        else:
            if (_val1.type == 'UNDEF') and not (_val2.type == 'UNDEF'):
                _val1.type=_val2.type
            if (_val2.type == 'UNDEF') and not (_val1.type == 'UNDEF'):
                _val2.type=_val1.type
            if (_val2.type == 'UNDEF') and (_val1.type == 'UNDEF'):
                return Variable()
            x1=_val1.value
            x2=_val2.value
            if _val1.type == _val2.type:
                return Variable('LOGIC', x1 != x2)
            else:
                if _val1.left and _val2.right:
                    no_error=False
                    sys.stderr.write(f'Illegal operation: type conversion double definition is illegal\n')
                elif _val1.left:
                    res_type=_val1.type
                    _val1.left=False
                elif _val2.right:
                    res_type=_val2.type
                    _val2.right=False
                else:
                    no_error=False
                    sys.stderr.write(f'Illegal operation: type conversion required\n')
                if no_error:
                    return Variable('LOGIC', self.converse.converse_(_val1, res_type).value != self.converse.converse_(_val2, res_type).value)

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

    def declare_array(self, _name, _type, _value):
        if (_name in self.recs.keys()) or (_name in self.procs.keys()) or (_name in self.sym_table[self.scope].keys()):
            sys.stderr.write(f'The name is already taken\n')
        else:
            self.sym_table[self.scope][_name]=[_type, _value]
        return

    def declare(self, _type, _value):
        if (_value in self.recs.keys()) or (_value in self.procs.keys()) or (_value in self.sym_table[self.scope].keys()):
            sys.stderr.write(f'The variable is already declared\n')
        if _type in ['NUMERIC', 'LOGIC', 'STRING']:
            self.sym_table[self.scope][_value] = Variable(_type, None)
        elif _type in self.recs.keys():
            self.sym_table[self.scope][_value] = [_type, copy.deepcopy(self.recs[_type][0])]

    def get_value(self, node, sc=None):
        if sc is None:
            sc = self.scope
        if node.type == 'variable':
            return self.get_variable(node.value, sc)
        elif node.type == 'component_of':
            return self.get_component(node, sc)
        else:
            sys.stderr.write(f'Illegal value\n')
        return Variable()

    def get_variable(self, name, sc=None):
        if sc is None:
            sc = self.scope
        if name in self.sym_table[sc].keys():
            if type(self.sym_table[sc][name]) == Variable:
                return copy.copy(self.sym_table[sc][name])
            elif isinstance(self.sym_table[sc][name], list):
                return self.sym_table[sc][name]
            else:
                return self.sym_table[sc][name]
        else:
            sys.stderr.write(f' Scope {sc}: Undeclared variable\n')
        return Variable()

    def get_component(self, node, sc=None):
        if sc is None:
            sc = self.scope
        if node.type == 'component_of':
            if node.value in self.sym_table[sc].keys():
                res = self.sym_table[sc][node.value]
                index = node.child
                n = 0
                while not isinstance(index, list):
                    if debug_prints:
                        print(n, ' ', res)
                        n += 1
                    if isinstance(res, list):
                        res = res[1]
                    if debug_prints:
                        print('->', n, ' ', res)
                    if type(index.value) == int:
                        if index.value not in range(len(res)):
                            sys.stderr.write(f'Out of index range\n')
                            return Variable()
                        else:
                            if not isinstance(res, dict):
                                res = res[index.value]
                            else:
                                sys.stderr.write(f'Index instead of field name\n')
                                return Variable()
                    else:
                        if index.value in self.sym_table[sc].keys():
                            if type(self.sym_table[sc][index.value]) == Variable:
                                res = res[self.converse.converse_(self.sym_table[sc][index.value], 'NUMERIC').value]
                            else:
                                new_array = []
                                def_var = copy.deepcopy(res[0])
                                def_var.value = None
                                index_array = self.sym_table[sc][index.value][1]
                                for i in range(len(index_array)):
                                    num = self.converse.converse_(index_array[i], 'NUMERIC').value
                                    if num in range(len(res)):
                                        new_array.append(copy.deepcopy(res[num]))
                                    else:
                                        new_array.append(def_var)
                                res = np.array(new_array)
                                #return res
                        else:
                            if index.value in res.keys():
                                res = res[index.value]
                                #return res
                            else:
                                sys.stderr.write(f'Illegal data field\n')
                    index = index.child
                return res
            else:
                sys.stderr.write(f'Undeclared variable\n')
        else:
            sys.stderr.write(f'Illegal value\n')
        return Variable()

    def run_procedure(self, node):
        self.sym_table.append(dict())
        self.scope += 1
        data = node.child.child
        params = self.procs[node.value].child['parameters'].child
        if debug_prints:
            print('DATA: ', data)
            print('PAR: ', params)
        code = self.procs[node.value].child['body']
        i = 0
        name = None
        ref_arr = dict()
        while params and data:
            if isinstance(data, list):
                if data[0]:
                    res = self.get_value(data[0], self.scope-1)
                    if debug_prints:
                        print('GOT VAL', res)
                name = [data[0].value]
                if data[0].type == 'component_of':
                    indexing = data[0].child.value
                    if not type(indexing) == int:
                        indexing=self.get_variable(indexing, self.scope - 1).value
                    name.append(indexing)
                data = data[len(data) - 1]
            else:
                name = [data.value]
                if data.type == 'variables':
                    pass
                else:
                    if type(data) == Node:
                        res = self.get_value(data, self.scope - 1)
                        if debug_prints:
                            print("\nFROM ", data)
                            print('GOT VAL HERE', res)
                    else:
                        if debug_prints:
                            print('hiiiiiiii')
                    if data.type == 'component_of':
                        indexing = data.child.value
                        if not type(indexing) == int:
                            indexing = self.get_variable(indexing, self.scope-1).value
                        name.append(indexing)
                        data = data.child
                data = data.child
            if isinstance(params, list):
                self.interpreter_node(params[0].value)
                if params[0].type == 'ref_parameter':
                    ref_arr[params[0].value.child.value] = name
                self.sym_table[self.scope][params[0].value.child.value] = copy.deepcopy(res)
                params = params[len(params)-1]
            else:
                params = params.child
            i += 1
        for var in self.sym_table[self.scope]:
            if var in ref_arr.keys():
                if len(ref_arr[var]) == 2:
                    self.sym_table[self.scope-1][ref_arr[var][0]][1][ref_arr[var][1]]=self.sym_table[self.scope][var]
                else:
                    self.sym_table[self.scope-1][ref_arr[var][0]] = self.sym_table[self.scope][var]
        if debug_prints:
            print(self.sym_table[self.scope])
        self.interpreter_node(code)
        if debug_prints:
            print(self.sym_table[self.scope])
        self.sym_table.pop()
        self.scope -= 1
        return

    def describe_record(self, node):
        self.scope += 1
        self.sym_table.append(dict())
        p_params = node.child['parameters']
        p_convs = node.child['conversions']
        res_params = dict()
        res_convs = dict()
        while p_params:
            if isinstance(p_params, list):
                self.interpreter_node(p_params[0].value)
                res_params[p_params[0].value.child.value] = self.sym_table[self.scope].pop(p_params[0].value.child.value)
                p_params = p_params[len(p_params)-1]
            else:
                p_params = p_params.child
        self.sym_table.pop()
        self.scope -= 1
        return res_params, res_convs

    def create_robot(self, file_name):
        # MAP FILE DESCRIPTION
        # < start coordinate >
        # < field size >
        # < FIELD >
        # 'X' - wall
        # 'E' - exit
        # ' ' - empty
        # < /FIELD >
        # < PASSWORDS >
        # < password coordinate > < exit coordinate > < password >
        # < /PASSWORDS >

        fl = open(file_name)
        _text = fl.readlines()
        robot_info = _text.pop(0).rstrip().split(" ")
        map_size = _text.pop(0).rstrip().split(" ")

        # robot set
        x = int(robot_info[0])
        y = int(robot_info[1])
        _map = [0] * int(map_size[0])

        for i in range(int(map_size[0])):
            _map[i] = [0] * int((map_size[1]))
        for i in range(int(map_size[0])):
            for j in range(int(map_size[1])):
                _map[i][j] = rb.Cell("EMPTY")
        pos = 0
        for i in range(int(map_size[0])):
            line = list(_text.pop(0).rstrip())
            line = [rb.Cell(rb.types[i]) for i in line]
            _map[pos] = line
            pos += 1
        while len(_text) > 0:
            password_info = _text.pop(0).rstrip().split(" ")
            # PASSWORD
            passw = password_info[4]
            # WALL
            wall_x = int(password_info[0])
            wall_y = int(password_info[1])
            _map[wall_x][wall_y].passwords.append(passw)
            # EXIT
            exit_x = int(password_info[2])
            exit_y = int(password_info[3])
            _map[exit_x][exit_y].passwords.append(passw)
        self.robot = rb.Robot(_x=x, _y=y,  _map=_map)


if __name__ == '__main__':

    work = True

    while work:
        print('What do you want to test?')
        for msg in menu_main:
            print(msg)
        choice = int(input())
        if choice == 0:
            work = False
            print("Good bye")
        elif choice == 1:
            print('You\'ve chosen functions')
            work1 = True
            while work1:
                for msg in menu_functions:
                    print(msg)
                choice = int(input())
                if choice == 0:
                    work1 = False
                elif choice in range(len(functions_set)):
                    interpr=Interpreter()
                    f = open(functions_set[choice])
                    text=f.read()
                    f.close()
                    interpr.interpreter(text)
                    for sym_table in interpr.sym_table:
                        for keys, values in sym_table.items():
                            if isinstance(values, Variable):
                                if values.type == 'STRING':
                                    print(values.type, keys, '= \'', values.value, '\'')
                                else:
                                    print(values.type, keys, '=', values.value)
                            elif isinstance(values[1], dict):
                                print(values[0], keys, '=\n', values[1])
                            elif isinstance(values, list):
                                print(values[0][0], ' of ', values[0][1], keys, '=\n', values[1])

                    print('Records:')
                    print('"<name>" : <structure>')
                    for rec in interpr.recs:
                        print(f'"{rec}" : {interpr.recs[rec]}')
                    print('Procedures:')
                    print(interpr.procs)
        elif choice == 2:
            print('You\'ve chosen robot')
            work1=True
            while work1:
                for msg in menu_robot:
                    print(msg)
                choice=int(input())
                if choice == 0:
                    work1 = False
                elif choice in range(len(menu_robot)):
                    interpr=Interpreter()
                    interpr.create_robot(map_set[choice])
                    f=open('tests/Right_hand.txt')
                    text=f.read()
                    f.close()
                    interpr.interpreter(text)
                    for sym_table in interpr.sym_table:
                        for keys, values in sym_table.items():
                            if isinstance(values, Variable):
                                if values.type == 'STRING':
                                    print(values.type, keys, '= \'', values.value, '\'')
                                else:
                                    print(values.type, keys, '=', values.value)
                            elif isinstance(values[1], dict):
                                print(values[0], keys, '=\n', values[1])
                            elif isinstance(values, list):
                                print(values[0][0], ' of ', values[0][1], keys, '=\n', values[1])
                    print('Records:')
                    print('"<name>" : <structure>')
                    for rec in interpr.recs:
                        print(f'"{rec}" : {interpr.recs[rec]}')
                    print('Procedures:')
                    print(interpr.procs)
        elif choice == 3:
            print('You\'ve chosen other')
            work1 = True
            while work1:
                for msg in menu_other:
                    print(msg)
                choice=int(input())
                if choice == 0:
                    work1=False
                elif choice in range(len(other_set)):
                    interpr=Interpreter()
                    f=open(other_set[choice])
                    text=f.read()
                    f.close()
                    interpr.interpreter(text)
                    for sym_table in interpr.sym_table:
                        for keys, values in sym_table.items():
                            if isinstance(values, Variable):
                                if values.type == 'STRING':
                                    print(values.type, keys, '= \'', values.value, '\'')
                                else:
                                    print(values.type, keys, '=', values.value)
                            elif isinstance(values[1], dict):
                                print(values[0], keys, '=\n', values[1])
                            elif isinstance(values, list):
                                print(values[0][0], ' of ', values[0][1], keys, '=\n', values[1])
                    print('Records:')
                    print('"<name>" : <structure>')
                    for rec in interpr.recs:
                        print(f'"{rec}" : {interpr.recs[rec]}')
                    print('Procedures:')
                    print(interpr.procs)
        else:
            print('Incorrect input, try again')

