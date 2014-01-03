
reserved = {
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'elseif' : 'ELSEIF',
    'while' : 'WHILE',
    'for' : 'FOR',

    'not' : 'NOT',
    'and' : 'AND',
    'or' : 'OR',
    'larger' : 'LARGER',
    "smaller" : 'SMALLER',
    "equal" : 'EQUAL',

    'in' : 'IN',
    'object' : 'OBJECT',
    'val' : 'VAL',
    'var' : 'VAR',

    'new' : 'NEW',
    'user_define' : 'USER_DEFINE',
    'text_file' : 'TEXT_FILE',
    'sequence_file' : 'SEQUENCE_FILE',
    'rdd' : 'RDD',
    'end' : 'END'
}
tokens = [
    'ID','NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',

    'LPAREN','RPAREN',

    'LBRACE',
    'RBRACE',


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
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
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



#===============================yacc========================================================
#"""

precedence = ( )

# dictionary of names
names = { }





class Scope:
    def __init__(self,parent_scope):
        self.parent_scope = parent_scope
        self.clean()

    def clean(self):
        self.id_table = {}
        self.decl = []
        self.stmt_init = []
        self.rdd_id = ""
        self.code = ""        
    def append_code(self,code):
        self.code = self.code + code;

scope_now = Scope(parent_scope = None)


#to-do have to finish the scope structure
#to-do change the VAL_DECL_INIT STMT_INIT mechanism


def p_program(p):
    '''
    PROGRAM : BLOCK_STMT
    '''
    print p[1]

def p_block_stmt(p):
    '''
    BLOCK_STMT : LBRACE enter_scope DECL_INIT STMT_INIT  RBRACE 
    '''
    global scope_now
    p[0] = '{\n\t' + ''.join(scope_now.decl).replace('\n','\n\t') + ''.join(scope_now.stmt_init).replace('\n','\n\t') + '\n}'
    scope_now = scope_now.parent_scope
    
def p_statment_init(p):
    '''
    STMT_INIT : STMT_INIT STMT 
    '''
    global scope_now
    scope_now.stmt_init.append('\n'+p[2])


def p_statment_end(p):
    '''
    STMT_INIT : 
    '''

def p_statment(p):
    '''
    STMT : BLOCK_STMT
         | FOR_STMT
         | WHILE_STMT 
         | IF_STMT 
         | ELSE_STMT 
         | ELSE_IF_STMT 
    '''
    p[0] = p[1]

def p_if_stmt(p):
    '''
    IF_STMT : IF LOGIC_EXPR BLOCK_STMT 
    ''' 
    p[0] = 'if' + '(' + p[2] + ')' + p[3]

def p_else_stmt(p): 
    ''' 
    ELSE_STMT : ELSE BLOCK_STMT 
    ''' 
    p[0] = 'else' + p[2]

def p_else_if_stmt(p): 
    ''' 
    ELSE_IF_STMT : ELSEIF LOGIC_EXPR BLOCK_STMT
    ''' 
    p[0] = 'else if' + '(' + p[2] + ')' + p[3]

def p_for_stmt(p):
    '''
    FOR_STMT : FOR ITERABLE BLOCK_STMT
    '''
    p[0] = 'for' + '( ' + p[2] + ' )' + p[3]


def p_while_stmt(p):
    '''
    WHILE_STMT : WHILE LOGIC_EXPR BLOCK_STMT
    '''
    p[0] = 'while'+'('+p[2]+')'+p[3]

def p_enter_scope(p):
    '''
    enter_scope :
    '''
    global scope_now
    scope_now = Scope(scope_now)


def p_iterable(p):
    '''
    ITERABLE : ID IN CONTAINER
    '''
#   to-do
#             | CONTAINER   

    p[0] = p[1] + ' <- ' + p[3]

def p_container(p):
    '''
    CONTAINER : ID
    '''
    p[0] = p[1]

def p_declare_init(p):
    '''
    DECL_INIT : DECL_INIT DECL
              | 
    '''

    if len(p) > 1 :
        global scope_now
        scope_now.decl.append(p[2]+'\n')


def p_declare(p):
    '''
    DECL : VAL_DECL
         | VAR_DECL
    '''
    p[0] = p[1]

def p_val_declare(p):
    '''
    VAL_DECL : VAL ID EQUALS NUMBER
             | VAL ID EQUALS USER_DEFINE_VALUE
             | VAL ID EQUALS RDD_INIT
    '''
    p[0] = "val "+p[2]+" = "+p[4]

def p_var_declare(p):
    '''
    VAR_DECL : VAR ID EQUALS NUMBER
             | VAR ID EQUALS USER_DEFINE_VALUE
             | VAR ID EQUALS RDD_INIT
    '''
    p[0] = "var " + p[2] + " = " + p[4]

def p_user_define_value(p):
    '''
    USER_DEFINE_VALUE : USER_DEFINE STRING
    '''
    p[0] = p[2][1:-1]

def p_rdd_init(p):
    '''
    RDD_INIT : TEXT_FILE LPAREN STRING RPAREN
    '''
    p[0] = 'sc.textFile("%s")' % p[3][1:-1]


def p_error(p):
    print("Syntax error at '%s'" % p.value)

def p_logic_expr(p):
    '''
    LOGIC_EXPR : ID 
               | NUMBER

    '''
    #to-do function call
    p[0] = p[1]

def p_logic_not_expr(p):
    '''
    LOGIC_EXPR : NOT LOGIC_EXPR
    '''
    p[0] = '!' + p[2]

def p_logic_op_expr(p):
    '''
    LOGIC_EXPR : ID AND LOGIC_EXPR
               | ID OR LOGIC_EXPR
               | ID LARGER LOGIC_EXPR
               | ID EQUAL LOGIC_EXPR
               | ID SMALLER LOGIC_EXPR
               | NUMBER AND LOGIC_EXPR
               | NUMBER OR LOGIC_EXPR
               | NUMBER LARGER LOGIC_EXPR
               | NUMBER EQUAL LOGIC_EXPR
               | NUMBER SMALLER LOGIC_EXPR
    '''
    if p[2] == 'and':
        p[0] = p[1] + '&&' + p[3]
    elif p[2] == 'or':
        p[0] = p[1] + '^' + p[3]
    elif p[2] == 'larger':
        p[0] = p[1] + '>' + p[3]
    elif p[2] == 'equal':
        p[0] = p[1] + '==' + p[3]
    elif p[2] == 'smaller':
        p[0] = p[1] + '<' + p[3]



import ply.yacc as yacc
yacc.yacc()

data = '''
{
    val R = 1000
    var lines = text_file("input.data")
    val rand = user_define "new Random(42)"

    for a in b{
        val R = 1000
        val rand = user_define "new Random(42)"
    }

    while a equal 10 and b {
        val R = 1 
    }
    if a larger b{
        var haha = 1
    }
    elseif a smaller b{
        var haha = 2
    }
    else{
        var haha = 3
    }
}
'''
#for R in rand { user_define "R=R+1" }


#yacc.parse(data,debug=True)
yacc.parse(data)
#"""


'''
def p_object_name(t):
    'OBJECT : OBJECT_NUMBER BLOCKSTMT'
    object_name = t[1]

def p_block_stmt(t):
    """
    BLOCK_STMT : '{' VAR_DECL_INIT STMT_INIT '}'
              | '{' VAL_DECL_INIT STMT_INIT '}'
              ;
    """

rdd.map( => )
rdd.groupByKey
var = var function_call parameter end
var varName = expression
expression : arithmetic_stmt
           | function_call
function_call : varName function_name Lparameter Rparmeter
              | varName user_define String

'''



"""

BLOCK_STMT          :   '{' VAR_DECL_INIT STMT_INIT '}'
                    |   '{' VAL_DECL_INIT STMT_INIT '}'
                    ;
STMT_INIT           :   STMT_INIT STMT
                    |
                    ;

#todo
STMT                : 
                    ;

FOR_STMT : FOR ID IN CONTAINER '{' USER_DEFINE_VALUE '}'
         ;

VAR_DECL_INIT       :   VAR_DECL_INIT VAR_DECL
                    |
                    ;

VARDECL             :   VAR ID
                    ;

VAL_DECL_INIT       :   VAL_DECL_INIT VAL_DECL
                    |
                    ;

VAL_DECL            :   VAL ID '=' NUMBER
                    |   VAL ID '=' USER_DEFINE_VALUE
                    ;

USER_DEFINE_VALUE   :   USER_DEFINE STRING
                    ;


RDD_INIT            :   TEXT_FILE '(' PATH ')'
                    :   SEQUENCE_FILE( PATH, CLASS , CLASS)
                    ;

PATH                :   STRING
CLASS               :   STRING
OBJECT_ID           :   STRING


"""

'''
EXPRESSION
if else
case data
function call
a.function_call

WHILE(a){
    

}
'''