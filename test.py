
reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'elseif' : 'ELSEIF',
    'while' : 'WHILE',
    'for' : 'FOR',
    'break' : 'BREAK',
    'continue' : 'CONTINUE',



    'in' : 'IN',
    'val' : 'VAL',
    'var' : 'VAR',

    'function':'FUNCTION',
    'to' : 'TO',
    'user_define' : 'USER_DEFINE',
    'text_file' : 'TEXT_FILE',
}
tokens = [
    'ID','NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'NOT','AND','OR','LARGER','SMALLER','LOGIC_EQUAL',

    'LPAREN','RPAREN',

    'LBRACE',
    'RBRACE',


    'STRING'
    ]+ list(reserved.values())



# Tokens
t_PLUS        = r'\+'
t_MINUS       = r'-'
t_TIMES       = r'\*'
t_DIVIDE      = r'/'
t_EQUALS      = r'='
t_NOT         = r'!'
t_AND         = r'&&'
t_OR          = r'\|\|'
t_LARGER      = r'>'
t_SMALLER     = r'<'
t_LOGIC_EQUAL = r'=='
t_LPAREN      = r'\('
t_RPAREN      = r'\)'
t_LBRACE      = r'\{'
t_RBRACE      = r'\}'
t_NUMBER      = r'[-+]?\d*\.\d+|\d+'


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
{
    val R = 1000
    val rand = user_define "new Random(42)"
    
    var lines = text_file "input.data"
    val data = lines function map line to function parseVector "line,' '"
    
    var kPoints = data function takeSample "false,K,42"
    var tempDist = 1.0


    while tempDist > convergeDist {
        var closest = data function map p to ( function closestPoint "p, kPoints" ( 1 p ) )
        var pointStats = closest function reduceByKey ((x1 y1)  (x2 y2)) to ( x1+x2  y1+y2 )
        var newPoint = pointStats function map pair to (pair_1 par_2/pair_2_2)
        var newPointArray =  newPoint function collectAsMap
        tempDist = 0.0

    }
}
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
        #self.id_table = {}
        self.decl = []
        self.stmt_init = []
        #self.rdd_id = ""
        self.code = ""  
    def append_code(self,code):
        self.code = self.code + code;

scope_now = Scope(None)

class Tuple:
    def __init__(self,parent_tuple):
        self.parent_tuple = parent_tuple
        self.element_list = []
    def append(self,element):
        self.element_list.append(element)

tuple_now = Tuple(None)

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
         | BREAK
         | CONTINUE 
    '''
    p[0] = p[1]
def p_statment_2(p):
    '''
    STMT : ID EQUALS EXPR
    '''
    p[0] = p[1] + p[2] + p[3]
def p_if_stmt(p):
    '''
    IF_STMT : IF EXPR BLOCK_STMT 
    ''' 
    p[0] = 'if' + '(' + p[2] + ')' + p[3]

def p_else_stmt(p): 
    ''' 
    ELSE_STMT : ELSE BLOCK_STMT 
    ''' 
    p[0] = 'else' + p[2]

def p_else_if_stmt(p): 
    ''' 
    ELSE_IF_STMT : ELSEIF EXPR BLOCK_STMT
    ''' 
    p[0] = 'else if' + '(' + p[2] + ')' + p[3]

def p_for_stmt(p):
    '''
    FOR_STMT : FOR ITERABLE BLOCK_STMT
    '''
    p[0] = 'for' + '( ' + p[2] + ' )' + p[3]


def p_while_stmt(p):
    '''
    WHILE_STMT : WHILE EXPR BLOCK_STMT
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
    VAL_DECL : VAL ID EQUALS EXPR
             | VAL ID EQUALS USER_DEFINE_VALUE
    '''
    p[0] = "val "+p[2]+" = "+p[4]

def p_var_declare(p):
    '''
    VAR_DECL : VAR ID EQUALS EXPR
             | VAR ID EQUALS USER_DEFINE_VALUE
    '''
    p[0] = "var " + p[2] + " = " + p[4]

def p_user_define_value(p):
    '''
    USER_DEFINE_VALUE : USER_DEFINE STRING
    '''
    p[0] = p[2][1:-1]

def p_rdd_init(p):
    '''
    RDD_INIT : TEXT_FILE  STRING 
    '''
    p[0] = 'sc.textFile("%s")' % p[2][1:-1]


def p_error(p):
    print("Syntax error at '%s'" % p.value)

def p_expr(p):
    '''
    EXPR : ID 
         | NUMBER
         | RDD_INIT
         | FUNCTION_CALL

    '''
    #to-do 
    p[0] = p[1]
def p_expr_tuple(p):
    '''
    EXPR : LPAREN enter_tuple TUPLE_INIT RPAREN
    '''
    global tuple_now

    p[0] = p[1] + ",".join(tuple_now.element_list)+p[4]
    tuple_now = tuple_now.parent_tuple

def p_enter_tuple(p):
    '''
    enter_tuple :
    '''
    global tuple_now
    tuple_now = Tuple(tuple_now)

def p_tuple_init(p):
    '''
    TUPLE_INIT : TUPLE_INIT EXPR
               |
    '''
    global tuple_now
    if len(p) > 1:
        tuple_now.append(p[2])

def p_function_call(p):
    '''
    FUNCTION_CALL : FUNCTION ID PARAMETER
    '''
    p[0] = p[2]+"("+p[3]+")"

def p_object_function_call(p):
    '''
    FUNCTION_CALL : ID FUNCTION ID PARAMETER
    '''
    p[0] = p[1]+"."+p[3]+"("+p[4]+")"

def p_parameter(p):
    '''
    PARAMETER : STRING
    '''
    p[0] = p[1][1:-1]
    #no parameter => pass ""

def p_parameter_2(p):
    '''
    PARAMETER : EXPR TO EXPR
    '''
    p[0] = p[1] + " => " + p[3]
def p_prefix_expr(p):
    '''
    EXPR : NOT EXPR
         | MINUS EXPR
    '''

    p[0] = p[1] + p[2]

def p_logic_op_expr(p):
    '''
    EXPR : EXPR AND EXPR
         | EXPR OR EXPR
         | EXPR LARGER EXPR
         | EXPR LOGIC_EQUAL EXPR
         | EXPR SMALLER EXPR
         | EXPR PLUS EXPR
         | EXPR MINUS EXPR
         | EXPR TIMES EXPR
         | EXPR DIVIDE EXPR
         
    '''

    p[0] = p[1] + " " + p[2] + " " + p[3]


import ply.yacc as yacc
yacc.yacc()

data = '''
{
    val R = 1000
    val rand = user_define "new Random(42)"
    
    var lines = text_file "input.data"
    val data = lines function map line to function parseVector "line,' '"
    
    var kPoints = data function takeSample "false,K,42"
    var tempDist = 1.0


    while tempDist > convergeDist {
        var closest = data function map p to ( function closestPoint "p, kPoints" ( 1 p ) )
        var pointStats = closest function reduceByKey ((x1 y1)  (x2 y2)) to ( x1+x2  y1+y2 )
        var newPoint = pointStats function map pair to (pair_1 par_2/pair_2_2)
        var newPointArray =  newPoint function collectAsMap ""

        tempDist = 0.0
        for point in kPoints {
            tempDist = tempDist + point function squaredDist "newPoint"

        }
        for newP in newPoint {
            kPoints  = newP_2
        }

    }
}
'''
'''



'''
#for R in rand { user_define "R=R+1" }


#yacc.parse(data,debug=True)
yacc.parse(data)
#"""


'''
#def p_object_name(t):
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




'''

'''