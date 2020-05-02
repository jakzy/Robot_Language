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
              'ASSIGNMENT', 'PLUS', 'MINUS',
              'STAR', 'SLASH', 'CARET',
              'DOUBLE_QUOTE',
              'LESS', 'GREATER', 'EQ', 'NOTEQ',
              'R_QBRACKET', 'L_QBRACKET',
              'R_FBRACKET', 'L_FBRACKET',
              'AMPERSAND', 'COMMA', 'DOT','TEXT', 'NEWLINE'] + list(reserved.values())

    t_ASSIGNMENT = r'\='
    t_PLUS = r'\+'
    t_MINUS = r'\-'
    t_STAR = r'\*'
    t_SLASH = r'\/'
    t_CARET = r'\^'
   # t_DOUBLE_QUOTE = r'\"'
    t_LESS = r'\<'
    t_GREATER = r'\>'
    t_EQ = r'\?'
    t_NOTEQ = r'\!'
    t_R_QBRACKET = r'\]'
    t_L_QBRACKET = r'\['
    t_R_FBRACKET = r'\}'
    t_L_FBRACKET = r'\{'
    t_AMPERSAND = r'\&'
    t_COMMA = r'\,'
    t_DOT = r'\.'

    def t_VARIABLE(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = reserved.get(t.value, 'VARIABLE')
        return t

    def t_TEXT(self, t):
        r'".*?"'
        t.value = t.value[1:len(t.value)-1]
        return t

    def t_DECIMAL(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_NEWLINE(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        return t

    def t_error(self, t):
        sys.stderr.write(f'Illegal character: {t.value[0]} at line {t.lexer.lineno}\n')
        t.lexer.skip(1)

    t_ignore = ' \t'

    def input(self, info):
        return self.lexer.input(info)

    def token(self):
        return self.lexer.token()


if __name__ == '__main__':
    f = open(r'lexer_test.txt')
    #f = open(r'tiny_test.txt')
    #f = open(r'bubble_sort.txt')
    data = f.read()
    f.close()
    lexer = Lexer()
    lexer.input(data)
    while True:
        token = lexer.token()
        if token is None:
            break
        else:
            print(f"Line[{token.lineno}]: position[{token.lexpos}]: type = '{token.type}'\tvalue = '{token.value}'")
