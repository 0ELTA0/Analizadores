import ply.yacc as yacc
from ply.lex import lex

# List of token names
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
)

# Regular expression rules for tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t

# Ignored characters (whitespace)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print("Carácter no reconocido '%s'" % t.value[0])
    t.lexer.skip(1)

# Parsing rules
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_expression_parentheses(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_term(p):
    '''
    term : term TIMES factor
         | term DIVIDE factor
         | factor
    '''
    if len(p) == 4:
        if p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            if p[3] != 0:
                p[0] = p[1] / p[3]
            else:
                raise ZeroDivisionError("Error: División por cero")
    else:
        p[0] = p[1]

def p_factor(p):
    '''
    factor : NUMBER
           | LPAREN expression RPAREN
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


# Build the lexer
lexer = lex()

# Build the parser
parser = yacc.yacc()
data = "3 + 4 * (2 - 1)"
result = parser.parse(data)
print(result)