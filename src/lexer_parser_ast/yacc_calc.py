import ply.yacc as yacc
from ilex import tokens

precedence = (
    ('nonassoc', 'LT', 'GT', 'LEQ', 'GEQ'),   # nonassociative operators
    ('left', '+', '-'),
    ('left', '*', '/', '%'),
    ('right', 'UMINUS'),    # Unary minus operator
)

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
        p[0] = p[1]
    elif p[1] == '(':
        p[0] = p[2]
    elif p[2] == '+':
        p[0] = p[1] + p[3]  # rst = a + b
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    elif p[2] == '%':
        p[0] = p[1] % p[3]

def p_exp_uminus(p):
    "exp : '-' exp %prec UMINUS"
    p[0] = -1 * p[2]
    

# def p_exp_term(p):
#     "exp : term"
#     p[0] = p[1]

# def p_term_mul(p):
#     "term : term '*' factor"
#     p[0] = p[1] * p[3]

# def p_term_div(p):
#     "term : term '/' factor"
#     p[0] = p[1] / p[3]

# def p_term_mod(p):
#     "term : term '%' factor"
#     p[0] = p[1] % p[3]

# def p_term_factor(p):
#     "term : factor"
#     p[0] = p[1]

# def p_factor_num(p):
#     "factor : NUM"
#     p[0] = p[1]

# def p_factor_exp(p):
#     "factor : '(' exp ')'"
#     p[0] = p[2]

def p_error(p):
    print('Syntax error!')
    # while True:
    #     tok = yacc.token()
    #     if not tok or tok.type == ';': break
    # yacc.errok()

if __name__ == '__main__':
    parser = yacc.yacc()

    while True:
        try:
            s = input('calc > ')
        except EOFError:
            exit(0)
        if not s: continue
        result = parser.parse(s)
        if result:
            print(result)