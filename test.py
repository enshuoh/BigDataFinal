
reserved = {
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'while' : 'WHILE',

    'object' : 'OBJECT',
    'val' : 'VAL',
    'new' : 'NEW',
    'user_define' : 'USER_DEFINE',
    'text_file' : 'TEXT_FILE',
    'sequence_file' : 'SEQUENCE_FILE'
}
tokens = [
    'ID','NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN',

    'TO',
    'DOT',
    'STRING'
    ]+ list(reserved.values())



# Tokens
t_TO = r'=>'
t_DOT = r'\.'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_NUMBER  = r'[-+]?\d*\.\d+|\d+'


t_STRING  = r'\".*?\"'
# Ignored characters

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

import ply.lex as lex
#lexer = lex.lex()
lex.lex()

#simple

"""


data = '''
val R = 1000
val rand = user_define "new Random(42)"
val K = 10
val converge_dist = 0.1
val lines = text_file("input.data")
val data = lines.map(line => new Vector(line.split(' ').map(_.toDouble)))

'''

# Give the lexer some input
lexer.input(data)

# Tokenize

while True:
    tok = lexer.token()
    if not tok: break      # No more input
    print tok
#"""


#"""

precedence = ( )
# dictionary of names
names = { }

def p_val_declare_init(t):
    '''VAL_DECL_INIT : VAL_DECL_INIT VAL_DECL
                     |
    '''
def p_val_declare(t):
    '''
    VAL_DECL : VAL ID EQUALS NUMBER
             | VAL ID EQUALS USER_DEFINE_VALUE
             | VAL ID EQUALS RDD_INIT
    '''
    print "var "+t[2]+" = "+t[4]
    names[len(names)+1] = t[2]

def p_user_define_value(t):
    '''
    USER_DEFINE_VALUE : USER_DEFINE STRING
    '''
    t[0] = t[2][1:-1]

def p_rdd_init(t):
    '''
    RDD_INIT : TEXT_FILE LPAREN STRING RPAREN
    '''
    t[0] = 'sc.textFile("%s")' % t[3][1:-1]

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
yacc.yacc()
data = '''
val R = 1000
val rand = user_define "new Random(42)"
val lines = text_file("input.data")
'''
yacc.parse(data)

#"""


'''
def p_object_name(t):
    'OBJECT : OBJECT_ID BLOCKSTMT'
    object_name = t[1]

def p_block_stmt(t):
    """
    BLOCKSTMT : '{' VAR_DECL_INIT STMT_INIT '}'
              | '{' VAL_DECL_INIT STMT_INIT '}'
              ;
    """
'''



"""
OBJECT : OBJECT_ID BLOCKSTMT
BLOCKSTMT			:	'{' VAR_DECL_INIT STMT_INIT '}'
					|	'{' VAL_DECL_INIT STMT_INIT '}'
					;
STMT_INIT			:	STMT_INIT STMT
					|
					;

#todo
STMT				:
					;



VAR_DECL_INIT		:	VAR_DECL_INIT VAR_DECL
					|
					;

VARDECL				:	VAR ID
					;

VAL_DECL_INIT		:	VAL_DECL_INIT VAL_DECL
					|
					;

VAL_DECL			:	VAL ID '=' NUMBER
					|	VAL ID '=' USER_DEFINE_VALUE
					;

USER_DEFINE_VALUE	:	USER_DEFINE STRING
					;


RDD_INIT			:	TEXT_FILE '(' PATH ')'
					:	SEQUENCE_FILE( PATH, CLASS , CLASS)
					;

PATH				:	STRING
CLASS				:	STRING
OBJECT_ID			:	STRING

"""