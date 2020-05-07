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
            return res, self._procedures, self._records
        except LexError:
            sys.stderr.write(f'Illegal token {s}\n')

    @staticmethod
    def p_program(p):
        """program : statements"""
        p[0] = Node(t='program', ch=p[1], no=p.lineno(1), pos=p.lexpos(1))

    @staticmethod
    def p_statements(p):
        """statements : statements statement
                      | statement"""
        if len(p) == 2:
            p[0] = Node(t='statements', ch=p[1])
        else:
            p[0] = Node(t='statements', ch=[p[1], p[2]])

    @staticmethod
    def p_statement(p):
        """statement : declaration NEWLINE
                     | assignment NEWLINE
                     | cycle NEWLINE
                     | command NEWLINE
                     | procedure NEWLINE
                     | call NEWLINE
                     | record NEWLINE
                     | empty NEWLINE"""
        p[0] = p[1]

    @staticmethod
    def p_declaration(p):
        """declaration : type variable"""
        p[0] = Node(t='declaration', val=p[1], ch=p[2])

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
        """command : MOVEUP      L_QBRACKET variable R_QBRACKET
                   | MOVEDOWN    L_QBRACKET variable R_QBRACKET
                   | MOVERIGHT   L_QBRACKET variable R_QBRACKET
                   | MOVELEFT    L_QBRACKET variable R_QBRACKET
                   | PINGUP      L_QBRACKET variable R_QBRACKET
                   | PINGDOWN    L_QBRACKET variable R_QBRACKET
                   | PINGRIGHT   L_QBRACKET variable R_QBRACKET
                   | PINGLEFT    L_QBRACKET variable R_QBRACKET
                   | VISION      L_QBRACKET variable R_QBRACKET
                   | VOICE       L_QBRACKET expression R_QBRACKET"""
        p[0] = Node(t='command', val=p[1], ch=p[3], no=p.lineno(1), pos=p.lexpos(1))

    def p_procedure(self, p):
        """procedure : PROC VARIABLE L_QBRACKET parameters R_QBRACKET statements_group"""
        self._procedures[p[2]] = Node(t='procedure', val=p[2], ch={'parameters': p[4], 'body': p[6]})
        p[0] = Node(t='procedure_description', val=p[2], no=p.lineno(1), pos=p.lexpos(1))

    @staticmethod
    def p_call(p):
        """call : VARIABLE L_QBRACKET variables R_QBRACKET"""
        p[0] = Node(t='procedure_call', val=p[1], ch=p[3])

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
        """variables : variables COMMA variable
                    | variable"""
        if len(p) == 2:
            p[0] = Node(t='variables', ch=p[1])
        else:
            p[0] = Node(t='variables', ch=[p[1], p[3]])

    @staticmethod
    def p_variable(p):
        """variable : VARIABLE L_QBRACKET expression R_QBRACKET
                    | VARIABLE"""
        if len(p) == 2:
            p[0] = Node(t='variable', val=p[1])
        else:
            p[0] = Node(t='component', val=p[1], ch=p[3], no=p.lineno(1), pos=p.lexpos(1))

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
                              | MINUS expression"""
        if len(p) == 3:
            p[0] = Node(t='unary_expression', val=p[1], ch=p[2], no=p.lineno(1), pos=p.lexpos(1))
        else:
            p[0] = Node(t='binary_expression', val=p[2], ch=[p[1], p[3]], no=p.lineno(1), pos=p.lexpos(1))

    @staticmethod
    def p_part_expression_right(p):
        """part_expression : DOT expression"""
        p[0] = Node(t='expression', val='right', ch=p[2], no=p.lineno(1), pos=p.lexpos(1))

    @staticmethod
    def p_part_expression_left(p):
        """part_expression : expression DOT"""
        p[0] = Node(t='expression', val='left', ch=p[1], no=p.lineno(1), pos=p.lexpos(1))

    @staticmethod
    def p_part_expression(p):
        """part_expression : expression"""
        p[0] = Node(t='expression', val=None, ch=p[1], no=p.lineno(1), pos=p.lexpos(1))

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
    def p_statement_error(p):
        """statement : errors NEWLINE"""
        sys.stderr.write(f'Syntax error: "{p[1][0].value}" at {p[1][0].lineno}:{p[1][0].lexpos}\n')

    @staticmethod
    def p_statement_error_no_nl(p):
        """statement : errors"""
        sys.stderr.write(f'Syntax error: "{p[1][0].value}" at {p[1][0].lineno}:{p[1][0].lexpos}\n')

    @staticmethod
    def p_errors(p):
        """errors : errors error
        | error"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + p[2]

    def p_error(self, p):
        print(f'Syntax error at {p}')
        self.correct = False

    def get_f(self):
        return self._procedures


if __name__ == '__main__':
    f = open("tiny_test.txt")
    #f = open(r'lexer_test.txt')
    #f = open(r'bubble_sort.txt')
    text = f.read()
    f.close()
    parser = Parser()
    tree, proc_table, rec_table = parser.parse(text)
    print('Code tree: ')
    tree.print()
    print('Procedures: ')
    print(proc_table)
    print('Records: ')
    print(rec_table)