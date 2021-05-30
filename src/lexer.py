from ply import lex

class Lexer:
    def __init__(self):
        # Build the lexer
        self.lexer = lex.lex(self)
    
    def __iter__(self):
        return iter(self.lexer)

    def input(self, data):
        self.lexer.input(data)

    reserve_words = {
        'program' : 'PROGRAM',
        'const' : 'CONST',
        'type' : 'TYPE',
        'var' : 'VAR',
        'array' : 'ARRAY',
        'label' : 'LABEL',
        'int' : 'INT',  # data type
        'real' : 'REAL',
        'bool' : 'BOOL',
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
        'downto' : 'DOWNTO',
        'repeat' : 'REPEAT',
        'until' : 'UNTIL',
        'break' : 'BREAK',  # loop control  [break, continue, eixt, (goto)]
        'continue' : 'CONTINUE',
        'exit' : 'EXIT',
        'goto' : 'GOTO',
        'function' : 'FUNCTION',    # sub program
        'procedure' : 'PROCEDURE',
        'return' : 'RETURN',
        'and' : 'AND',   # boolean operators
        'or' : 'OR',
        'not' : 'NOT',
    }

    # list of tokens
    tokens = [
        'LITERAL_INT', 'LITERAL_REAL', 'LITERAL_CHAR', 'LITERAL_STRING', 'LITERAL_BOOL',
        'EQ', 'NEQ', 'LT', 'GT', 'LEQ', 'GEQ', # relational operators
        'ID',
        'ASSIGN',
        'RANGE'
    ]
    tokens += list(reserve_words.values())

    # regular expression rules start with t_
    t_EQ = r'\='
    t_NEQ = r'\<\>'
    t_LT = r'\<'
    t_GT = r'\>'
    t_LEQ = r'\<\='
    t_GEQ = r'\>\='

    t_ASSIGN = r'\:\='

    t_RANGE = r'\.\.'

    literals = ['+', '-', '*', '/', '%', '(', ')', '[', ']', ',', ';', '.', ':']

    # action code
    def t_LITERAL_REAL(self, t):
        r'\d+\.\d+'
        t.value = float(t.value)
        return t

    def t_LITERAL_INT(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_LITERAL_BOOL(self, t):
        r'(true)|(false)'
        return t

    def t_LITERAL_CHAR(self, t):
        r'\'.\''
        t.value = t.value[1]
        return t

    def t_LITERAL_STRING(self, t):
        r'\'.*?\''  # '?' find shortest match
        t.value = t.value[1:-1] # delete ''
        return t

    def t_ID(self, t):
        r'[_a-zA-Z][_a-zA-Z0-9]*'
        t.type = self.reserve_words.get(t.value, 'ID')   # reserve words or identifier
        return t

    # track the number of lines
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'
    t_ignore_COMMENT = r'\{.*\}'

    # Error handling rule
    def t_error(self, t):
        print("LexError: %s (Line %d, Colummn %d)" % (t.value[0], t.lineno, t.lexpos))
        # print ("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)
    


if __name__ == '__main__':
    # Test it out
    data = '''IF { comment } 'c'
    <> > < >=
    3 + 4 * 10
    + -20 *2
    '''.lower()

    # Give the lexer some input
    lexer = Lexer()
    lexer.input(data)
    # lexer.input('false program begin \'\' \'c\' -7.0 1..2 \'str\' end.')
    

    # Tokenize
    for tok in lexer:   # same as tok = lexer.token() and tok != None
        print(tok)  # (type, value, lineno, pos)()