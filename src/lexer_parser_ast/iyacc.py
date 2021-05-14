import json
import ply.yacc as yacc
from ilex import tokens
from iast import Node

precedence = (
    ('nonassoc', 'LT', 'GT', 'LEQ', 'GEQ'),   # nonassociative operators
    ('left', '+', '-'),
    ('left', '*', '/', '%'),
    ('right', 'UMINUS'),    # Unary minus operator
)

def p_program(p):
    '''program : head_block decl_block main_block
    '''
    p[0] = p[3]

def p_head_block(p):
    '''head_block : PROGRAM ID ';'
    '''

def p_decl_block(p):    # ...
    '''decl_block : empty
    '''

def p_main_block(p):
    '''main_block : BEGIN exp END '.'
    '''
    p[0] = p[2]

def p_exp(p):
    '''exp : exp '+' exp
           | exp '-' exp
           | exp '*' exp
           | exp '/' exp
           | exp '%' exp
           | '(' exp ')'
           | LITERAL_INT
           | LITERAL_REAL'''
    if len(p) == 2: # NUM
        if type(p[1]) == int:
            p[0] = Node('<int>', p[1], None)
        else:
            p[0] = Node('<real>', p[1], None)
    elif p[1] == '(':
        p[0] = p[2]
    elif p[2] == '+':
        p[0] = Node('+', p[1].val+p[3].val, [p[1], p[3]])   # rst = a + b
    elif p[2] == '-':
        p[0] = Node('-', p[1].val-p[3].val, [p[1], p[3]])
    elif p[2] == '*':
        p[0] = Node('*', p[1].val*p[3].val, [p[1], p[3]])
    elif p[2] == '/':
        p[0] = Node('/', p[1].val/p[3].val, [p[1], p[3]])
    elif p[2] == '%':
        p[0] = Node('%', p[1].val%p[3].val, [p[1], p[3]])

def p_exp_uminus(p):
    "exp : '-' exp %prec UMINUS"
    p[2].val *= -1
    p[0] = p[2]
    
def p_empty(p):
    'empty :'

def p_error(p):
    print('Syntax error!')
    # while True:
    #     tok = yacc.token()
    #     if not tok or tok.type == ';': break
    # yacc.errok()

if __name__ == '__main__':
    parser = yacc.yacc()

    root = parser.parse('''program hi;
                             BEGIN 
                             5*(1--4)+2.1 
                             end.'''.lower())
    print(root.val)
    result = json.dumps(root.get_json())
    file = open("./AST.json", "w")
    file.write(result)
    file.close()
    print(result)