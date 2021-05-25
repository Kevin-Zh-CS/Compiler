import json
from typing import Literal
from llvmlite import ir
from ply import yacc
from lexer import Lexer
from ast import *

from llvmlite import ir

class Parser:
    def __init__(self):
        # Build the lexer
        self.parser = yacc.yacc(module=self)

        # Declare module
        self.module = ir.Module()
        # Declare main function
        func_type = ir.FunctionType(ir.VoidType(), [])
        main_func = ir.Function(self.module, func_type, "main")
        block = main_func.append_basic_block()
        # Declare builder
        self.builder = ir.IRBuilder(block)
        # Declare symbol_table
        self.symbol_table = None
        Node.init_nodes((self.builder, self.module, self.symbol_table))
    

    
    def parse(self, input):
        return self.parser.parse(input)

    tokens = Lexer.tokens
    lexer = Lexer()

    precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('nonassoc', 'EQ', 'NEQ'),   # nonassociative operators
        ('nonassoc', 'LT', 'GT', 'LEQ', 'GEQ'),
        ('left', '+', '-'),
        ('left', '*', '/', '%'),
        ('right', 'UMINUS', 'NOT'),    # Unary minus operator
        ('nonassoc', 'BRACKETS'),
        ('nonassoc', 'DANGLING'),
    )

    def p_program(self, p):
        '''program : PROGRAM ID ';' body '.'
        '''
        p[0] = Program(name=p[2], body=p[4])

    def p_body(self, p):
        '''body : local_list compound_stmt
        '''
        p[0] = Body(local_list=p[1], block=p[2])
    
    def p_local_list(self, p):
        '''local_list : local_list local
                      | empty
        '''
        if len(p) == 2:
            p[0] = []
        else: 
            p[1].append(p[2])
            p[0] = p[1]
    
    def p_local1(self, p):
        '''local : VAR var_list
        '''
        p[0] = VarList(var_list=p[2])
    
    def p_local2(self, p):
        '''local : LABEL id_list ';'
        '''
        p[0] = LabelList(label_list=p[2])

    def p_local3(self, p):
        '''local : CONST const_exp_list
        '''
        p[0] = ConstList(const_list=p[2])
    
    def p_local4(self, p):
        '''local : header ';' body ';'
        '''
        p[0] = LocalHeader(header=p[0], body=p[3])
    
    def p_var_list(self, p):
        '''var_list : var_list var
                    | var
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1]
            p[0].append(p[2])

    def p_var(self, p):
        '''var : id_list ':' vartype ';'
               | id_list ':' vartype EQ exp ';'
        '''
        # id_list is a list of strings
        if len(p) == 5:
            p[0] = Var(id_list=p[1], vartype=p[3], var=None)
        else:
            p[0] = Var(id_list=p[1], vartype=p[3], var=p[5])

    def p_const_exp_list(self, p):
        '''const_exp_list : const_exp_list const_exp
                          | const_exp
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1]
            p[0].append(p[2])
    
    def p_const_exp(self, p):
        '''const_exp : id_list EQ literal ';'
        '''
        p[0] = ConstExp(id_list=p[1], var=p[3])

    def p_id_list(self, p):
        '''id_list : ID comma_id_list
        '''
        p[2].insert(0, p[1])
        p[0] = p[2]
    
    def p_comma_id_list(self, p):
        '''comma_id_list : comma_id_list ',' ID
                         | empty
        '''
        if len(p) == 2:
            p[0] = []
        else:
            p[1].append(p[3])
            p[0] = p[1]
            
    def p_header1(self, p):
        '''header : PROCEDURE ID '(' formal_list ')'
                  | PROCEDURE ID '(' ')'
        '''
        if len(p) == 5: # no fomal_list
            p[0] = ProcHeader(id=p[2], formal_list=p[4])
        else:
            p[0] = ProcHeader(id=p[2], formal_list=[])
    
    def p_header2(self, p):
        '''header : FUNCTION ID '(' formal_list ')' ':' vartype
                    | FUNCTION ID '(' ')' ':' vartype
        '''
        if len(p) == 7: # no fomal_list
            p[0] = FuncHeader(id=p[2], formal_list=p[4], ret_type=p[7])
        else:
            p[0] = FuncHeader(id=p[2], formal_list=[], ret_type=p[6])
    
    def p_formal_list(self, p):
        '''formal_list : formal semicolon_formal_list
        '''
        p[2].insert(0, p[1])
        p[0] = p[2]
    
    def p_formal(self, p):
        '''formal : id_list ':' vartype
        '''
        p[0] = Formal(id_list=p[1], para_type=p[3])
    
    def p_semicolon_formal_list(self, p):
        '''semicolon_formal_list : semicolon_formal_list ';' formal
                                 | empty
        '''
        if len(p) == 2:
            p[0] = []
        else:
            p[1].append(p[3])
            p[0] = p[1]

    ######
    def p_vartype1(self, p):
        '''vartype : INT
                   | REAL
                   | BOOL
                   | CHAR
                   | STRING
        '''
        p[0] = Type(type=p[1])
    
    def p_vartype2(self, p):
        '''vartype : ARRAY '[' LITERAL_INT ']' OF vartype
                   | ARRAY OF vartype
        '''
        if len(p) == 4:
            p[0] = ArrayType(length=p[3], type=p[6])
        else:
            p[0] = ArrayType(length=0, type=p[3])
    
    def p_semicolon_stmt_list(self, p):
        '''semicolon_stmt_list : semicolon_stmt_list ';' stmt
                               | empty
        '''
        if len(p) == 2:
            p[0] = []
        else:
            p[1].append(p[3])
            p[0] = p[1]
    
    def p_stmt(self, p):
        '''stmt : ID ':' non_label_stmt
                | non_label_stmt
        '''
        if len(p) == 4: # statement with label
            p[0] = LabelStmt(id=p[1], non_label_stmt=p[3])
        else:
            p[0] = p[1]
    
    def p_non_label_stmt(self, p):
        '''non_label_stmt : assign_stmt
                          | call_stmt
                          | for_stmt
                          | if_stmt
                          | while_stmt
                          | repeat_stmt
                          | case_stmt
                          | goto_stmt
                          | compound_stmt
        '''
        p[0] = p[1]
    
    def p_assign_stmt(self, p):
        '''assign_stmt : lvalue ASSIGN exp
        '''
        p[0] = Assign(lvalue=p[1], exp=p[3])
    
    def p_for_stmt(self, p):
        '''for_stmt : FOR ID ASSIGN exp direction exp DO stmt
        '''
        # derect is either 0 or 1, 0 means increase
        p[0] = For(id=p[2], exp1=p[4], direct=p[5], exp2=p[6], stmt=p[8])
    
    def p_direction(self, p):
        '''direction : DOWNTO
                     | TO
        '''
        p[0] = 0 if p[1] == 'to' else 1

    def p_while_stmt(self, p):
        '''while_stmt : WHILE exp DO stmt
        '''
        p[0] = While(exp=p[2], stmt=p[4])
    
    def p_repeat_stmt(self, p):
        '''repeat_stmt : REPEAT stmt semicolon_stmt_list UNTIL exp
        '''
        p[3].insert(0, p[2])
        p[0] = Repeat(stmt_list=p[3], exp=p[5])
    
    def p_case_stmt(self, p):
        '''case_stmt : CASE exp OF case_exp_list END
        '''
        p[0] = Case(exp=p[2], case_exp_list=p[4])
    
    def p_case_exp_list(self, p):
        '''case_exp_list : case_exp_list case_exp
                         | case_exp
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            if p[1] is None:
                p[1] = []
            p[1].append(p[2])
            p[0] = p[1]
    
    def p_case_exp(self, p):
        '''case_exp : literal ':' stmt ';'
                    | ID ':' stmt ';'
        '''
        # name is either identifier or constant
        p[0] = CaseExp(name=p[1], stmt=p[3])
    
    def p_goto_stmt(self, p):
        '''goto_stmt : GOTO ID
        '''
        p[0] = Goto(id=p[2])
    
    def p_compound_stmt(self, p):
        '''compound_stmt : BEGIN stmt semicolon_stmt_list END
        '''
        p[3].insert(0, p[2])
        p[0] = Compound(stmt_list=p[3])
    
    def p_call_stmt(self, p):
        '''call_stmt : ID '(' exp comma_exp_list ')'
                     | ID '(' ')'
        '''
        if len(p) == 4: # no arguments
            p[0] = Call(id=p[1], exp=[])
        else:
            p[4].insert(0, p[3])
            p[0] = Call(id=p[1], exp=p[4])
    
    def p_comma_exp_list(self, p):
        '''comma_exp_list : comma_exp_list ',' exp
                          | empty
        '''
        if len(p) == 2:
            p[0] = []
        else:
            p[1].append(p[3])
            p[0] = p[1]
    
    def p_if_stmt(self, p):
        '''if_stmt : IF exp THEN stmt else_stmt
        '''
        p[0] = If(exp=p[2], stmt=p[4], else_stmt=p[5])
    
    def p_else_stmt(self, p):
        '''else_stmt : ELSE stmt ';'
                     | empty %prec DANGLING
        '''
        # precedence ???
        if p[1] == 'else':
            p[0] = p[2]
        else:
            p[0] = None 
    
    def p_lvalue(self, p):
        '''lvalue : ID
                  | ID '[' exp ']' %prec BRACKETS         
        '''
        if len(p) == 2:
            p[0] = LValue(id=p[1], exp=None)
        else:
            p[0] = LValue(id=p[1], exp=p[3])
    
    def p_literal(self, p):
        '''literal : LITERAL_INT
                   | LITERAL_REAL
                   | LITERAL_BOOL
                   | LITERAL_CHAR
                   | LITERAL_STRING
        '''
        p[0] = LiteralVar(var=p[1], type=p.slice[1].type[8:].lower())

    def p_exp1(self, p):
        '''exp : call_stmt
        '''
        p[0] = p[1]
    
    def p_exp2(self, p):
        '''exp : exp '+' exp
               | exp '-' exp
               | exp '*' exp
               | exp '/' exp
               | exp '%' exp
               | exp EQ exp
               | exp NEQ exp
               | exp LT exp
               | exp GT exp
               | exp LEQ exp
               | exp GEQ exp
               | exp AND exp
               | exp OR exp
        '''
        p[0] = BinExp(operant=p[2], exp1=p[1], exp2=p[3])
    
    def p_exp3(self, p):
        '''exp : NOT exp
        '''
        p[0] = UniExp(operant=p[1], exp=p[2])

    def p_exp_uminus(self, p):
        "exp : '-' exp %prec UMINUS"
        p[0] = UniExp(operant=p[1], exp=p[2])

    def p_exp4(self, p):
        '''exp : '(' exp ')'
        '''
        p[0] = p[2]
    
    def p_exp5(self, p):
        '''exp : ID
               | literal
        '''
        # p[0] is a string or a constant value
        p[0] = p[1]
    
    def p_exp6(self, p):
        '''exp : ID '[' LITERAL_INT ']'
        '''
        # p[0] is a string or a constant value
        p[0] = Array(id=p[1], index=p[3])
    
        
    def p_empty(self, p):
        'empty :'
        p[0] = None

    def p_error(self, p):
        print('Syntax error! Line:', self.lexer.lexer.lineno)

if __name__ == '__main__':
    parser = Parser()

    fin = open("/Users/xy/Compiler/src/test_sample.txt")
    root = parser.parse(fin.read().lower())
    fin.close()
    # root = parser.parse('''program sample;
    #                     { ------------------------------------------------------------ }
    #                     var
    #                     i : char;
    #                     { ------------------------------ }
    #                     BEGIN 
    #                     i := not(5.0*(1--4)+2.1 and 123) 
    #                     end.'''.lower())

    print(type(root))