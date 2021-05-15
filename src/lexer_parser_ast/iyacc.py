import json
import ply.yacc as yacc
from ilex import tokens
from iast import Node

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'EQ', 'NEQ'),   # nonassociative operators
    ('nonassoc', 'LT', 'GT', 'LEQ', 'GEQ'),
    ('left', '+', '-'),
    ('left', '*', '/', '%'),
    ('right', 'UMINUS', 'NOT'),    # Unary minus operator
)

def p_program(p):
    '''program : head_block decl_block main_block
    '''
    p[0] = Node('program', p[3].val, [p[1], p[2], p[3]])

def p_head_block(p):
    '''head_block : PROGRAM ID ';'
    '''
    p[0] = Node('program_head', p[2], None)

def p_decl_block(p):    # ...
    #'''decl_block : const_part type_part var_part routine_part
    '''decl_block : const_part type_part
    '''
    p[0] = Node('program_declaration', None, [p[1], p[2]])
    # p[0] = Node('program_declaration', None, [p[1], p[2], p[3], p[4]])

def p_const_part(p):
    '''const_part : CONST const_exp_list
                  | empty
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_const_exp_list(p):
    '''const_exp_list : const_exp const_exp_list
                      | const_exp
    '''
    if len(p) == 2:
        p[0] = Node('const_exp_list', None, [p[1]])
    else:
        p[0] = Node('const_exp_list', None, [p[1]] + p[2].children)

def p_const_exp(p):
    '''const_exp : ID EQ exp ';'
    '''
    p[0] = Node('const_exp', (p[1], p[3]), None)

def p_type_part(p):
    '''type_part : TYPE type_decl_list
                 | empty
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_type_decl_list(p):
    '''type_decl_list : type_decl type_decl_list
                      | type_decl
    '''
    if len(p) == 2:
        p[0] = Node('type_decl_list', None, [p[1]])
    else:
        p[0] = Node('type_decl_list', None, [p[1]] + p[2].children)

def p_type_decl(p):
    '''type_decl : ID EQ type_def ';'
    '''
    p[0] = Node(p[3].type, (p[1], p[3]), None)

def p_type_def(p):
    '''type_def : sys_type_def
                | enum_type_def
    '''
                #     | array_type_def
                # | record_type_def
    p[0] = p[1]

def p_sys_type_def(p):
    '''sys_type_def : INT
                    | REAL
                    | BOOL
                    | CHAR
                    | STRING
                    | ID
    '''
    # value is the name of type
    p[0] = Node('sys_type', p.slice[1].type.lower(), None)

def p_enum_type_def(p):
    '''enum_type_def : '(' enum_elem_list ')'
    '''
    # value is the list of elements' name
    p[0] = Node('enum_type', p[2].val, None)

def p_enum_elem_list(p):
    '''enum_elem_list : enum_elem ',' enum_elem_list
                      | enum_elem
    '''
    if len(p) == 2:
        p[0] = Node('', [p[1].val], None)
    else:
        p[0] = Node('', [p[1].val] + p[3].val, None)

def p_enum_elem(p):
    '''enum_elem : ID
    '''
    p[0] = Node('', p[1], None)

def p_array_type_def(p):
    '''
    '''

def p_record_type_def(p):
    '''
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
           | relat_exp
           | LITERAL_INT
           | LITERAL_REAL
           | LITERAL_BOOL
           | LITERAL_CHAR
           | LITERAL_STRING
           '''
    if len(p) == 2: 
        if p.slice[1].type == 'relat_exp':
            p[0] = p[1]
        else:   # LITERAL
            p[0] = Node(p.slice[1].type[8:].lower(), p[1], None)
    elif p[1] == '(':
        p[0] = p[2]
    else:
        p[0] = Node(p[2], eval("p[1].val" + p[2] + "p[3].val"), [p[1], p[3]])

def p_relat_exp(p):
    '''relat_exp : exp EQ exp
                 | exp NEQ exp
                 | exp LT exp
                 | exp GT exp
                 | exp LEQ exp
                 | exp GEQ exp
                 | exp AND exp
                 | exp OR exp
                 | NOT exp
    '''
    operator = p.slice[2].type.lower()
    if len(p) == 3: # NOT
        p[0] = Node('not', bool(not p[2].val), [p[2]])
    elif operator == 'and':
        p[0] = Node(operator, bool(p[1].val and p[3].val), [p[1], p[3]])
    elif operator == 'or':
        p[0] = Node(operator, bool(p[1].val or p[3].val), [p[1], p[3]])
    elif operator == 'eq':
        p[0] = Node('==', p[1].val == p[3].val, [p[1], p[3]])
    elif operator == 'neq':
        p[0] = Node('!=', p[1].val != p[3].val, [p[1], p[3]])
    elif operator == 'lt':
        p[0] = Node('<', p[1].val < p[3].val, [p[1], p[3]])
    elif operator == 'gt':
        p[0] = Node('>', p[1].val > p[3].val, [p[1], p[3]])
    elif operator == 'leq':
        p[0] = Node('<=', p[1].val <= p[3].val, [p[1], p[3]])
    elif operator == 'geq':
        p[0] = Node('>=', p[1].val >= p[3].val, [p[1], p[3]])

def p_exp_uminus(p):
    "exp : '-' exp %prec UMINUS"
    p[2].val *= -1
    p[0] = p[2]
    
def p_empty(p):
    'empty :'
    p[0] = None

def p_error(p):
    print('Syntax error!')
    # while True:
    #     tok = yacc.token()
    #     if not tok or tok.type == ';': break
    # yacc.errok()

if __name__ == '__main__':
    parser = yacc.yacc()  

    fin = open("./test_sample.txt")
    root = parser.parse(fin.read().lower())
    fin.close()
    # root = parser.parse('''program hi;
    #                          BEGIN 
    #                          5.0*(1--4)+2.1 
    #                          end.'''.lower())

    print(root.val)
    json_str = json.dumps(root.get_json())
    fout = open("./AST.json", "w")
    fout.write(json_str)
    fout.close()
    # print(json_str)