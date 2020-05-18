import sys
from Parser.parser import Parser
from typing import List, Dict, Optional
from syntax_tree import Node
import copy
import numpy as np


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
        if type(var) == np.ndarray:
            print('LATER')
            return Variable()
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
            sys.stderr.write(f'UNEXPECTED ERROR\n')

        # STATEMENTS BLOCK

        # statements -> declaration
        elif node.type == 'declaration':
            declaration_type = node.value
            declaration_child = node.child
            if (declaration_type in ['NUMERIC', 'LOGIC', 'STRING']) or (declaration_type in self.recs):
                if node.child.type == 'component_of':
                    if not isinstance(node.child.child.child, list):
                        sys.stderr.write('ERROR, multidimensional arrays are illegal\n')
                    else:
                        size = node.child.child.value
                        if isinstance(size, str):
                            size = (self.get_variable(size)).value
                        elem = Variable(declaration_type)
                        res = []
                        for i in range(size):
                            res.append(copy.deepcopy(elem))
                        declaration_child.child = res
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
            name = node.value.value
            if name not in self.sym_table[self.scope].keys():
                sys.stderr.write(f'Undeclared variable\n')
            else:
                expression = self.interpreter_node(node.child)
                if type(self.sym_table[self.scope][name]) == Variable:
                    res = self.sym_table[self.scope][name]
                else:
                    if isinstance(node.value.child, list):
                        res = self.sym_table[self.scope][name][1]
                        if isinstance(expression, np.ndarray) :
                            for i in range(min(len(res), len(expression))):
                                self.assign(res[i], expression[i])
                        else:
                            for i in range(len(res)):
                                self.assign(res[i], expression)
                        return expression
                    else:
                        index = node.value.child
                        if isinstance(index, str):
                            index = (self.get_variable(index)).value
                        res = self.sym_table[self.scope][name][1]
                        res = res[index.value]
                self.assign(res, expression)
                return expression


        # statements -> cycle
        elif node.type == 'cycle':
            self.op_cycle(node)

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
        if node.type == 'part_expression':
            exp = self.interpreter_node(node.child)
            if type(exp) == Variable:
                if exp:
                    if node.value:
                        if node.value == "right":
                            exp.right = True
                            print('right up')
                        elif node.value == "left":
                            exp.left = True
                            print('left up')
            else:
                for elem in exp:
                    if node.value:
                        if node.value == "right":
                            elem.right=True
                            print('right up')
                        elif node.value == "left":
                            elem.left = True
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

        # expression -> component_of

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
        if type(_val1) == np.ndarray:
            res = copy.deepcopy(_val1)
            if type(_val2) == np.ndarray:
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
        if type(_val1) == np.ndarray:
            res=copy.deepcopy(_val1)
            if type(_val2) == np.ndarray:
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
        res_type='UNDEF'
        if type(_val1) == np.ndarray:
            res=copy.deepcopy(_val1)
            if type(_val2) == np.ndarray:
                for i in range(min(len(_val1), len(_val2))):
                    res[i]=self.bin_slash(_val1[i], _val2[i])
            else:
                for i in range(len(_val1)):
                    res[i]=self.bin_slash(_val1[i], _val2)
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
                    return Variable('NUMERIC', x1 // x2)
                elif _val1.type == "LOGIC":
                    if (x1 != None) and (x2 != None):
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
            if (_val2.type == 'UNDEF') and not (_val1.type == 'UNDEF'):
                _val2.type=_val1.type
            if (_val2.type == 'UNDEF') and (_val1.type == 'UNDEF'):
                return Variable()
            x1=_val1.value
            x2=_val2.value
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
            if (_val2.type == 'UNDEF') and not (_val1.type == 'UNDEF'):
                _val2.type=_val1.type
            if (_val2.type == 'UNDEF') and (_val1.type == 'UNDEF'):
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
            if (_val2.type == 'UNDEF') and not (_val1.type == 'UNDEF'):
                _val2.type=_val1.type
            if (_val2.type == 'UNDEF') and (_val1.type == 'UNDEF'):
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
        if type(_val1) == np.ndarray:
            res=copy.deepcopy(_val1)
            if type(_val2) == np.ndarray:
                for i in range(min(len(_val1), len(_val2))):
                    res[i]=self.bin_equal(_val1[i], _val2[i])
            else:
                for i in range(len(_val1)):
                    res[i]=self.bin_equal(_val1[i], _val2)
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
        if (_type in ['NUMERIC', 'LOGIC', 'STRING']) or (_type in self.recs.keys()):
            self.sym_table[self.scope][_value] = Variable(_type, None)

    def get_value(self, node):
        if node.type == 'variable':
            return self.get_variable(node.value)
        else:
            sys.stderr.write(f'Illegal value\n')
        return Variable()

    def get_variable(self, name):
        if name in self.sym_table[self.scope].keys():
            if type(self.sym_table[self.scope][name]) == Variable:
                return self.const_val(self.sym_table[self.scope][name].value)
            else:
                return self.sym_table[self.scope][name][1]
        else:
            sys.stderr.write(f'Undeclared variable\n')
        return Variable()

    def get_component(self, node):
        if node.type == 'component_of':
            if node.value in self.sym_table[self.scope].keys():
                res = self.sym_table[self.scope][node.value][1]
                index = node.child
                dims = len(res.shape)
                while index and dims:
                    dims -= 1
                    if index.value not in range(len(res)):
                        sys.stderr.write(f'Out of index range\n')
                        return Variable()
                    else:
                        res = res[index.value]
                    index = index.child
                if index:
                    sys.stderr.write(f'Out of dimension range\n')
                    return Variable()
                return res
            else:
                sys.stderr.write(f'Undeclared variable\n')
        else:
            sys.stderr.write(f'Illegal value\n')
        return Variable()


if __name__ == '__main__':
    f = open("tiny_test.txt")
    #f = open("logic_operations_test.txt")
    #f = open(r'lexer_test.txt')
    #f = open(r'bubble_sort.txt')
    text = f.read()
    f.close()
    interpr = Interpreter()
    interpr.interpreter(text)
    for sym_table in interpr.sym_table:
        for keys, values in sym_table.items():
            if isinstance(values, Variable):
                if values.type == 'STRING':
                    print(values.type, keys, '= \'', values.value, '\'')
                else:
                    print(values.type, keys, '=', values.value)
            elif isinstance(values, list):
                print(values[0][0], ' of ', values[0][1], keys, '= \n', values[1])
    print('Records:')
    print(interpr.recs)
    print('Procedures:')
    print(interpr.procs)
