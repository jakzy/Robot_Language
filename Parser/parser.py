import ply.yacc as yacc
from ply.lex import LexError
import sys
from typing import List, Dict, Optional

# outer classes
from lexer import Lexer
from syntax_tree import Node


class Parser(object):

    tokens = Lexer.tokens
    precedence = Lexer.precedence

    def __init__(self):
        self.correct = True
        self.lexer = Lexer()
        self.parser = yacc.yacc(module=self)
        self._procedures: Dict[str, Node] = dict()
        self._records: Dict[str, Node] = dict()

    def parse(self, s) -> List:
        try:
            res = self.parser.parse(s)
            return res,  self.correct
        except LexError:
            sys.stderr.write(f'Illegal token {s}\n')

    def get_proc(self):
        return self._procedures

    def get_recs(self):
        return self._records

    @staticmethod
    def p_program(p):
        """program : statements"""
        p[0] = Node(t='program', ch=p[1], no=p.lineno(1), pos=p.lexpos(1))

    @staticmethod
    def p_statements(p):
        """statements : statements statement
                      | statement"""
        if len(p) == 2:
            p[0] = Node(t='statements', ch=[p[1]])
        else:
            p[0] = Node(t='statements', ch=[p[1], p[2]])

    @staticmethod
    def p_statement(p):
        """statement : call NEWLINE
                     | declaration NEWLINE
                     | assignment NEWLINE
                     | cycle NEWLINE
                     | command NEWLINE
                     | procedure NEWLINE
                     | record NEWLINE
                     | empty NEWLINE"""
        p[0] = p[1]

    @staticmethod
    def p_declaration(p):
        """declaration : type variable"""
        p[0] = Node(t='declaration', val=p[1], ch=p[2])

    @staticmethod
    def p_call(p):
        """call : VARIABLE L_RBRACKET variables R_RBRACKET"""
        p[0] = Node(t='procedure_call', val=p[1], ch=p[3])

    @staticmethod
    def p_assignment(p):
        """assignment : variable ASSIGNMENT expression
                      | variable ASSIGNMENT assignment"""
        p[0] = Node(t='assignment', val=p[1], ch=p[3], no=p.lineno(1), pos=p.lexpos(1))

    @staticmethod
    def p_cycle(p):
        """ cycle : L_FBRACKET expression R_FBRACKET BLOCK inner_statements UNBLOCK"""
        p[0] = Node('cycle', ch={'condition':p[2], 'body':p[5]})

    @staticmethod
    def p_command(p):
        """command : MOVEUP      L_RBRACKET variable R_RBRACKET
                   | MOVEDOWN    L_RBRACKET variable R_RBRACKET
                   | MOVERIGHT   L_RBRACKET variable R_RBRACKET
                   | MOVELEFT    L_RBRACKET variable R_RBRACKET
                   | PINGUP      L_RBRACKET variable R_RBRACKET
                   | PINGDOWN    L_RBRACKET variable R_RBRACKET
                   | PINGRIGHT   L_RBRACKET variable R_RBRACKET
                   | PINGLEFT    L_RBRACKET variable R_RBRACKET
                   | VISION      L_RBRACKET variable R_RBRACKET
                   | VOICE       L_RBRACKET expression R_RBRACKET"""
        p[0] = Node(t='command', val=p[1], ch=p[3], no=p.lineno(1), pos=p.lexpos(1))

    def p_procedure(self, p):
        """procedure : PROC VARIABLE L_QBRACKET parameters R_QBRACKET statements_group"""
        self._procedures[p[2]] = Node(t='procedure', val=p[2], ch={'parameters': p[4], 'body': p[6]})
        p[0] = Node(t='procedure_description', val=p[2], no=p.lineno(1), pos=p.lexpos(1))

    def p_record(self, p):
        """record : RECORD VARIABLE DATA L_QBRACKET parameters R_QBRACKET
                  | RECORD VARIABLE DATA L_QBRACKET parameters R_QBRACKET conversions"""
        if len(p) == 8:
            self._records[p[2]] = Node(t='record',  val=p[2], ch={'parameters': p[5], 'conversions': p[7]})
        else:
            self._records[p[2]] = Node(t='record',  val=p[2], ch={'parameters': p[5], 'conversions': None})
        p[0] = Node(t='record_description', val=p[2], no=p.lineno(1), pos=p.lexpos(1))

    @staticmethod
    def p_conversions(p):
        """conversions :  conversions conversion
                       | conversion"""
        if len(p) == 2:
            p[0] = Node(t='conversions', ch=p[1])
        else:
            p[0] = Node(t='conversions', ch=[p[1], p[2]])

    @staticmethod
    def p_conversion(p):
        """conversion : CONVERSION TO   type VARIABLE
                      | CONVERSION FROM type VARIABLE"""
        p[0] = Node(t='conversion', val=p[2], ch=[p[3], p[4]])

    @staticmethod
    def p_empty(p):
        """empty : """
        pass

    @staticmethod
    def p_type(p):
        """type : NUMERIC
                | STRING
                | LOGIC
                | VARIABLE"""
        p[0] = p[1]

    @staticmethod
    def p_expression(p):
        """expression : variable
                      | const
                      | complex_expression"""
        p[0] = p[1]

    @staticmethod
    def p_variables(p):
        """variables :  expression
                     |  expression COMMA variables """
        if len(p) == 2:
            p[0] = Node(t='variables', ch=p[1])
        else:
            p[0] = Node(t='variables', ch=[p[1], p[3]])

    @staticmethod
    def p_variable(p):
        """variable : VARIABLE indexing
                    | VARIABLE"""
        if len(p) == 2:
            p[0] = Node(t='variable', val=p[1])
        else:
            p[0] = Node(t='component_of', val=p[1], ch=p[2], no=p.lineno(1), pos=p.lexpos(1))

    @staticmethod
    def p_indexing(p):
        """indexing : L_QBRACKET DECIMAL R_QBRACKET indexing
                    | L_QBRACKET DECIMAL R_QBRACKET
                    | L_QBRACKET VARIABLE R_QBRACKET indexing
                    | L_QBRACKET VARIABLE R_QBRACKET"""
        if len(p) == 5:
            p[0] = Node(t='indexing', val=p[2], ch=p[4], no=p.lineno(2), pos=p.lexpos(2))
        else:
            p[0] = Node(t='indexing', val=p[2], no=p.lineno(2), pos=p.lexpos(2))

    @staticmethod
    def p_const(p):
        """const : TRUE
                 | FALSE
                 | UNDEF
                 | DECIMAL
                 | TEXT
                 """
        p[0] = Node(t='const', val=p[1])

    @staticmethod
    def p_complex_expression(p):
        """complex_expression : part_expression PLUS    part_expression   %prec PLUS
                              | part_expression MINUS   part_expression   %prec MINUS
                              | part_expression STAR    part_expression   %prec STAR
                              | part_expression SLASH   part_expression   %prec SLASH
                              | part_expression CARET   part_expression   %prec CARET
                              | part_expression GREATER part_expression   %prec GREATER
                              | part_expression LESS    part_expression   %prec LESS
                              | part_expression EQ      part_expression   %prec EQ
                              | part_expression NOTEQ   part_expression   %prec NOTEQ
                              | MINUS expression %prec UMINUS"""
        if len(p) == 3:
            p[0]=Node(t='unary_expression', val=p[1], ch=p[2], no=p.lineno(1), pos=p.lexpos(1))
        else:
            p[0]=Node(t='binary_expression', val=p[2], ch=[p[1], p[3]], no=p.lineno(1), pos=p.lexpos(1))

    @staticmethod
    def p_part_expression_right(p):
        """part_expression : DOT expression"""
        p[0]=Node(t='expression', val='right', ch=p[2], no=p.lineno(1), pos=p.lexpos(1))

    @staticmethod
    def p_part_expression_left(p):
        """part_expression : expression DOT"""
        p[0]=Node(t='expression', val='left', ch=p[1], no=p.lineno(1), pos=p.lexpos(1))

    @staticmethod
    def p_part_expression(p):
        """part_expression : expression"""
        p[0]=Node(t='expression', val=None, ch=p[1], no=p.lineno(1), pos=p.lexpos(1))

    @staticmethod
    def p_parameters(p):
        """parameters : parameter COMMA parameters
                      | parameter"""
        if len(p) == 2:
            p[0] = Node(t='parameters', ch=p[1])
        else:
            p[0] = Node(t='parameters', ch=[p[1], p[3]])

    @staticmethod
    def p_parameter(p):
        """parameter : type VARIABLE AMPERSAND
                     | type VARIABLE"""
        if len(p) == 3:
            p[0] = Node(t='parameter', val=p[1])
        else:
            p[0] = Node(t='ref_parameter', val=p[1])

    @staticmethod
    def p_statements_group(p):
        """statements_group : BLOCK inner_statements UNBLOCK
                            | inner_statement"""
        if len(p) == 4:
            p[0] = p[2]
        else:
            p[0] = p[1]

    @staticmethod
    def p_inner_statements(p):
        """inner_statements :  inner_statement inner_statements
                            | inner_statement"""
        if len(p) == 3:
            p[0] = Node(t='inner_statement', ch=[p[1], p[2]])
        else:
            p[0] = Node(t='inner_statement', ch=p[1])

    @staticmethod
    def p_inner_statement(p):
        """inner_statement : declaration NEWLINE
                           | assignment NEWLINE
                           | cycle NEWLINE
                           | command NEWLINE
                           | call NEWLINE
                           | empty NEWLINE"""
        p[0] = p[1]

    @staticmethod
    def p_statement_error_no_nl(p):
        """statement : error"""
        p[0] = Node('error', val="Wrong syntax (test)", no=p.lineno(1), pos=p.lexpos(1))
        sys.stderr.write(f'>>> Wrong syntax. Check a NL\n')

    @staticmethod
    def p_declaration_error(p):
        """declaration : type error"""
        p[0] = Node('declaration', val=p[1], ch=p[2], no=p.lineno(2), pos=p.lexpos(2))
        sys.stderr.write(f'>>> Wrong name of declared value\n')

    @staticmethod
    def p_assignment_err(p):
        """assignment : variable ASSIGNMENT error"""
        p[0] = Node('error', val="Wrong assignment", no=p.lineno(1), pos=p.lexpos(1))
        sys.stderr.write(f'>>> Wrong assignment\n')

    @staticmethod
    def p_command_err(p):
        """command : MOVEUP      L_RBRACKET error R_RBRACKET
                   | MOVEDOWN    L_RBRACKET error R_RBRACKET
                   | MOVERIGHT   L_RBRACKET error R_RBRACKET
                   | MOVELEFT    L_RBRACKET error R_RBRACKET
                   | PINGUP      L_RBRACKET error R_RBRACKET
                   | PINGDOWN    L_RBRACKET error R_RBRACKET
                   | PINGRIGHT   L_RBRACKET error R_RBRACKET
                   | PINGLEFT    L_RBRACKET error R_RBRACKET
                   | VISION      L_RBRACKET error R_RBRACKET
                   | VOICE       L_RBRACKET error R_RBRACKET"""
        p[0] = Node('error', val="Command call error. Check the values in brackets", no=p.lineno(1), pos=p.lexpos(1))
        sys.stderr.write(f'>>> Command call error\n')

    def p_error(self, p):
        try:
            sys.stderr.write(f'Syntax error at {p.lineno} line\n')
        except:
            sys.stderr.write(f'Syntax error\n')
        self.correct = False




if __name__ == '__main__':
    f = open("../tiny_test.txt")
    #f = open(r'lexer_test.txt')
    #f = open(r'bubble_sort.txt')
    text = f.read()
    f.close()
    parser = Parser()
    tree, fl = parser.parse(text)
    print('Code tree: ')
    tree.print()
    print('Procedures: ')
    print(parser.get_proc())
    print('Records: ')
    print(parser.get_recs())