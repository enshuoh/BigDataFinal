
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
        self.id_table = {}
        self.val_decl = []
        self.stmt_init = []
        self.rdd_id = ""
        self.code = ""
    
    def append_code(self,code):
        self.code = self.code + code;


now_scope = Scope(parent_scope = None)

#to-do have to finish the scope structure
#to-do change the VAL_DECL_INIT STMT_INIT mechanism


def p_program(p):
    '''
    PROGRAM : BLOCK_STMT
    '''
    print p[1]

def p_block_stmt(p):
    '''
    BLOCK_STMT : LBRACE enter_scope VAL_DECL_INIT STMT_INIT exit_scope RBRACE 
    '''
    p[0] = now_scope.code

def p_statment_init(p):
    '''
    STMT_INIT : STMT_INIT STMT 
    '''
    now_scope.stmt_init.append(p[2])

def p_statment_end(p):
    '''
    STMT_INIT : 
    '''  

def p_statment(p):
    '''
    STMT : BLOCK_STMT
     | FOR_STMT
     | RDD_STMT
    '''
    p[0] = p[1]
"""
def p_statment_for(p):
    '''
    STMT : FOR_STMT 
    ''' 
    p[0] = p[1]
"""
def p_for_stmt(p):
    '''
    FOR_STMT : FOR ITERABLE BLOCK_STMT
    '''
    p[0] = 'for' + '( ' + p[2] + ' )' + p[3]

def p_enter_scope(p):
    '''
    enter_scope :
    '''
    global now_scope
    now_scope = Scope(now_scope)

def p_exit_scope(p):
    '''
    exit_scope :
    '''
    global now_scope
    now_scope.code = '{\n' + ''.join(now_scope.val_decl) +'\n' + ''.join(now_scope.stmt_init) + '\n}\n'
    code = now_scope.code
    now_scope = now_scope.parent_scope
    now_scope.append_code(code)

def p_iterable(p):
    '''
    ITERABLE : ID IN CONTAINER
    '''
    p[0] = p[1] + ' <- ' + p[3]

def p_container(p):
    '''
    CONTAINER : ID
    '''
    p[0] = p[1]



def p_val_declare_init(p):
    '''VAL_DECL_INIT : VAL_DECL_INIT VAL_DECL  
                     |
    '''
    if len(p) > 1 :
        now_scope.val_decl.append(p[2]+'\n')

def p_val_declare(p):
    '''
    VAL_DECL : VAL ID EQUALS NUMBER
             | VAL ID EQUALS USER_DEFINE_VALUE
             | VAL ID EQUALS RDD_INIT
    '''
    p[0] = "var "+p[2]+" = "+p[4]

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
    
def p_rdd_stmt(p):
    '''
    RDD_STMT : RDD RDD_FUNC_BLOCK END
    '''
    p[0] = p[2]

def p_rdd_func_block(p):
    '''
    RDD_FUNC_BLOCK : RDD_FUNC_BLOCK RDD_FUNC
                |
    '''
    if len(p)>1:
        p[0] = p[1] + p[2]
    else:
        p[0] = ''

def p_rdd_func(p):
    '''
    RDD_FUNC : STRING STRING ID ID
    '''
    p[0] = p[4] + " = " + p[3] +'.%s(%s)\n' %(p[1][1:-1],p[2][1:-1])

def p_error(p):
    print("Syntax error at '%s'" % p.value)



import ply.yacc as yacc
yacc.yacc()

data = '''
{
val R = 1000
val rand = user_define "new Random(42)"
val lines = text_file("input.data")
for a in b 
{
val R = 1000
val rand = user_define "new Random(42)"
}
rdd
"map" "abc" tmp1 tmp2
"map" "abc" tmp1 tmp3
end

rdd
"map" "abc" tmp1 tmp2
"map" "abc" tmp1 tmp3
end
}
'''
#for R in rand { user_define "R=R+1" }



#yacc.parse(data,debug=True)
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
