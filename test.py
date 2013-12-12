
reserved = {
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'for' : 'FOR',

    'in' : 'IN',
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
    'LBPAREN','RBPAREN',


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
t_LBPAREN  = r'\{'
t_RBPAREN  = r'\}'
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
lexer = lex.lex()
#lex.lex()

#simple

#test lex
"""

data = '''
val R = 1000
val rand = user_define "new Random(42)"
val K = 10
val converge_dist = 0.1
val lines = text_file("input.data")
for R in rand { user_define "R=R+1" }
'''

# Give the lexer some input
lexer.input(data)

# Tokenize

while True:
    tok = lexer.token()
    if not tok: break      # No more input
    print tok
#"""

#test parser
#"""

precedence = ( )
# dictionary of names
names = { }
def p_program(t):
    '''
    PROGRAM : BLOCK_STMT
    '''
    print t[1]
def p_block_stmt(t):
    '''
    BLOCK_STMT : LBPAREN VAL_DECL_INIT STMT_INIT RBPAREN
    '''
    t[0] = '{\n' + ''.join(val_decl) +'\n' + ''.join(stmt_init) + '\n}\n'

stmt_init = []
def p_statment_init(t):
    '''
    STMT_INIT : STMT_INIT STMT 
              |
    '''
    if len(t) > 1:
        stmt_init.append(t[2])

def p_statment(t):
    '''
    STMT : BLOCK_STMT
    '''
    t[0] = t[1]

def p_for_lopp(t):
    '''
    FOR_STMT : FOR ITERABLE LBPAREN USER_DEFINE_VALUE RBPAREN
             |
    '''
    t[0] = 'for' + '( ' + t[2] + ' )' + '{\n' + t[4] + '\n}'
def p_iterable(t):
    '''
    ITERABLE : ID IN CONTAINER
    '''
    t[0] = t[1] + ' <- ' + t[3]

def p_container(t):
    '''
    CONTAINER : ID
    '''
    t[0] = t[1]

val_decl = []

def p_val_declare_init(t):
    '''VAL_DECL_INIT : VAL_DECL_INIT VAL_DECL  
                     |
    '''
    if len(t) > 1 :
        val_decl.append(t[2]+'\n')

def p_val_declare(t):
    '''
    VAL_DECL : VAL ID EQUALS NUMBER
             | VAL ID EQUALS USER_DEFINE_VALUE
             | VAL ID EQUALS RDD_INIT
    '''
    t[0] = "var "+t[2]+" = "+t[4]
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
{
val R = 1000
val rand = user_define "new Random(42)"
val lines = text_file("input.data")

}
'''
#for R in rand { user_define "R=R+1" }


yacc.parse(data)

#"""


'''
def p_object_name(t):
    'OBJECT : OBJECT_ID BLOCKSTMT'
    object_name = t[1]

def p_block_stmt(t):
    """
    BLOCK_STMT : '{' VAR_DECL_INIT STMT_INIT '}'
              | '{' VAL_DECL_INIT STMT_INIT '}'
              ;
    """
'''



"""

BLOCK_STMT			:	'{' VAR_DECL_INIT STMT_INIT '}'
					|	'{' VAL_DECL_INIT STMT_INIT '}'
					;
STMT_INIT			:	STMT_INIT STMT
					|
					;

#todo
STMT				: 
					;

FOR_STMT : FOR ID IN CONTAINER '{' USER_DEFINE_VALUE '}'
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