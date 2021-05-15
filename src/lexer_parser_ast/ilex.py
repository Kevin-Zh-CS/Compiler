import ply.lex as lex

reserve_words = {
    'program' : 'PROGRAM',
    'const' : 'CONST',
    'type' : 'TYPE',
    'var' : 'VAR',
    'array' : 'ARRAY',
    'integer' : 'INT',  # data type
    'real' : 'REAL',
    'boolean' : 'BOOL',
    'char' : 'CHAR',
    'string' : 'STRING',
    'array' : 'ARRAY',
    'record' : 'RECORD',
    'begin' : 'BEGIN',  # begin ... end;
    'end' : 'END',
    'if' : 'IF',    # condition [if, case]
    'then' : 'THEN',
    'else' : 'ELSE',
    'case' : 'CASE',
    'of' : 'OF',
    'while' : 'WHILE',  # loop  [while, for, repeat]
    'do' : 'DO',
    'for' : 'FOR',
    'to' : 'TO',
    'repeat' : 'REPEAT',
    'until' : 'UNTIL',
    'break' : 'BREAK',  # loop control  [break, continue, eixt, (goto)]
    'continue' : 'CONTINUE',
    'exit' : 'EXIT',
    'goto' : 'GOTO',
    'function' : 'FUNCTION',    # sub program
    'procedure' : 'PROCEDURE',
    'and' : 'AND',   # boolean operators
    'or' : 'OR',
    'not' : 'NOT',
}

# list of tokens
tokens = [
    'LITERAL_INT', 'LITERAL_REAL', 'LITERAL_CHAR', 'LITERAL_STRING', 'LITERAL_BOOL',
    'EQ', 'NEQ', 'LT', 'GT', 'LEQ', 'GEQ', # relational operators
    'ID',
    'ASSIN',
    'RANGE',
    'COMMENT'
]
tokens += list(reserve_words.values())

# regular expression rules start with t_
t_EQ = r'\='
t_NEQ = r'\<\>'
t_LT = r'\<'
t_GT = r'\>'
t_LEQ = r'\<\='
t_GEQ = r'\>\='

t_ASSIN = r'\:\='

t_RANGE = r'\.\.'

literals = ['+', '-', '*', '/', '%', '(', ')', '[', ']', ',', ';', '.', ':']

# action code
def t_LITERAL_REAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_LITERAL_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_LITERAL_BOOL(t):
    r'(true)|(false)'
    return t

def t_LITERAL_CHAR(t):
    r'\'.\''
    t.value = t.value[1]
    return t

def t_LITERAL_STRING(t):
    r'\'.*?\''  # '?' find shortest match
    t.value = t.value[1:-1] # delete ''
    return t

def t_ID(t):
    r'[_a-zA-Z][_a-zA-Z0-9]*'
    t.type = reserve_words.get(t.value, 'ID')   # reserve words or identifier
    return t

# track the number of lines
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'
t_ignore_COMMENT = r'\{.*\}'

# Error handling rule
def t_error(t):
    print("LexError: %s (Line %d, Colummn %d)" % (t.value[0], t.lineno, t.lexpos))
    # print ("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

if __name__ == '__main__':
    # Test it out
    data = '''IF { comment } 'c'
    <> > < >=
    3 + 4 * 10
    + -20 *2
    '''.lower()

    # Give the lexer some input
    lexer.input(data)
    # lexer.input('false program begin \'\' \'c\' -7.0 1..2 \'str\' end.')
    

    # Tokenize
    for tok in lexer:   # same as tok = lexer.token() and tok != None
        print(tok)  # (type, value, lineno, pos)