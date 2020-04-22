# coding=utf8
import sys
import ply.lex as lex

reserved = {
    'TRUE': 'TRUE',
    'FALSE': 'FALSE',
    'LOGIC': 'LOGIC',
    'NUMERIC': 'NUMERIC',
    'STRING': 'STRING',
    'UNDEF': 'UNDEF',
    'RECORD': 'RECORD',
    'DATA': 'DATA',
    'CONVERSION': 'CONVERSION',
    'TO': 'TO',
    'FROM': 'FROM',
    'BLOCK': 'BLOCK',
    'UNBLOCK': 'UNBLOCK',
    'PROC': 'PROC',
    # robot
    'MOVEUP': 'MOVEUP',
    'MOVEDOWN': 'MOVEDOWN',
    'MOVERIGHT': 'MOVERIGHT',
    'MOVELEFT': 'MOVELEFT',
    'PINGUP': 'PINGUP',
    'PINGDOWN': 'PINGDOWN',
    'PINGRIGHT': 'PINGRIGHT',
    'PINGLEFT': 'PINGLEFT',
    'VISION': 'VISION',
    'VOICE': 'VOICE'
}


class Lexer(object):
    def __init__(self):
        self.lexer = lex.lex(module=self)

    tokens = ['DECIMAL',  'VARIABLE',
              'ASSIGNMENT', 'PLUS', 'MINUS', 'STAR',
              'SLASH', 'CARET',
              'DOUBLE_QUOTE',
              'LESS', 'GREATER', 'EQ', 'NOTEQ',
              #'R_BRACKET', 'L_BRACKET',
              'R_QBRACKET', 'L_QBRACKET',
              'R_FBRACKET', 'L_FBRACKET',
              'COMMA', 'DOT', 'NEWLINE'] + list(reserved.values())

    t_ASSIGNMENT = r'\='
    t_PLUS = r'\+'
    t_MINUS = r'\-'
    t_STAR = r'\*'
    t_SLASH = r'\/'
    t_CARET = r'\^'
    t_DOUBLE_QUOTE = r'\"'
    t_LESS = r'\<'
    t_GREATER = r'\>'
    t_EQ = r'\?'
    t_NOTEQ = r'\!'
    #t_R_BRACKET=r'\)'
    #t_L_BRACKET=r'\('
    t_R_QBRACKET = r'\]'
    t_L_QBRACKET = r'\['
    t_R_FBRACKET=r'\}'
    t_L_FBRACKET=r'\{'
    t_COMMA = r'\,'
    t_DOT = r'\.'
