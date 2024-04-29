# -----------------------------------------------------------------------------
# calccompile.py
# Description: An extension of the simple calculator from O'Reilly's "Lex and 
# Yacc", p. 63. This version adds support for modulus, integer division, and 
# exponentiation, and compiles the expression to JCoco assembly.
# Author: Nayan Sawyer
# Date: 2024-04-02
# Dependencies: PLY (Python Lex-Yacc)
# Comments: I claim no credit for the original code. This is a simple 
# extension of the original code to add support for modulus, integer division, 
# and exponentiation, and compile to JCoco assembly. This program was written 
# for a homework assignment for COS 301: Programming Languages at the 
# University of Maine. 
#
# Original Author: David Beazley
# Date: 2022-11-27\
# File URL: https://github.com/dabeaz/ply/blob/master/example/calc/calc.py
# -----------------------------------------------------------------------------

# LabelCounterSingleton 
class LabelCounterSingleton:
    counter = 0
    def increment():
        temp = LabelCounterSingleton.counter
        LabelCounterSingleton.counter += 1
        return temp

# Maps operators to their corresponding assembly instructions
# Lambdas are required because LabelCounterSingleton is incremented each time a label is used
# and function calls don't fire if its just a dictionary of strings
op_map2 = {
    '+': lambda : "\tBINARY_ADD",
    '-': lambda : "\tBINARY_SUBTRACT",
    '*': lambda : "\tBINARY_MULTIPLY",
    '/': lambda : "\tSTORE_FAST 0\n\
\tDUP_TOP\n\
\tLOAD_FAST 0\n\
\tROT_TWO\n\
\tLOAD_FAST 0\n\
\tBINARY_MODULO\n\
\tLOAD_CONST 1\n\
\tCOMPARE_OP 2\n\t" +
f"POP_JUMP_IF_FALSE fc{LabelCounterSingleton.counter}" + "\n" +
"\tBINARY_FLOOR_DIVIDE\n" +
"\t" + f"JUMP_ABSOLUTE fc{LabelCounterSingleton.counter}e" + "\n" +
f"fc{LabelCounterSingleton.counter}:" + "\n" +
"\tBINARY_TRUE_DIVIDE\n" +
f"fc{LabelCounterSingleton.increment()}e:",
    '%': lambda : "\tBINARY_MODULO",
    '^': lambda : "\tBINARY_POWER",
    'IDIV': lambda : "\tBINARY_FLOOR_DIVIDE",
    'UMINUS': lambda : "\tLOAD_CONST 1\n\tROT_TWO\n\tBINARY_SUBTRACT" # You could multiply by -1, but subtraction would be faster if this were real machine instructions
}
# These are for storing a list of starting data for the compiler to put in the header of the casm
constants = [None, 0, ""]
variables = ["worker",]

# AST classes
class Statement:
    def __init__(self, expression):
        self.expression = expression

    def eval(self):
        string = self.expression.eval()
        string += "\n" + "\tLOAD_GLOBAL 0\n\tROT_TWO\n\tCALL_FUNCTION 1"
        return string

class Assignment:
    def __init__(self, name, expression, index):
        self.name = name
        self.expression = expression
        self.index = index

    def eval(self):
        string = self.expression.eval() + "\n" + "\tSTORE_FAST " + str(self.index)
        string += "\n" + "\tLOAD_GLOBAL 0\n\tLOAD_CONST 2\n\tCALL_FUNCTION 1"
        return string

class BinaryOp:
    def __init__(self, left, right, op):
        self.op = op
        self.left = left
        self.right = right

    def eval(self):
        string = self.left.eval() + "\n" + self.right.eval() + "\n" + op_map2[self.op]()
        return string
        
class UnaryOp:
    def __init__(self, operand, op):
        self.op = op
        self.operand = operand

    def eval(self):
        string = self.operand.eval() + "\n" + op_map2[self.op]()
        return string

class Number:
    def __init__(self, value, index):
        self.value = value
        self.index = index

    def eval(self):
        string = "\tLOAD_CONST " + str(self.index)
        return string

class Variable:
    def __init__(self, name, index):
        self.name = name
        self.index = index

    def eval(self):
        string = "\tLOAD_FAST " + str(self.index)
        return string

# Lexing and parsing begins here
tokens = (
    'NAME', 'INT', 'FLOAT', 'IDIV', # integer division
)

literals = ['=', '+', '-', '*', '/', '(', ')', '%', '^'] # modulus and exponentiation

# Tokens

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = 'NAME'
    if t.value not in variables:
        variables.append(t.value)
    return t

def t_FLOAT(t): # floating point numbers
    r'([0-9]*\.[0-9]+)'
    t.value = float(t.value)
    if t.value not in constants: # only add the constant if it's not already in the list
        constants.append(t.value)
    return t

def t_INT(t):
    r'[0-9]+'
    t.value = int(t.value) 
    if t.value not in constants: # only add the constant if it's not already in the list
        constants.append(t.value)
    return t

def t_IDIV(t): # integer division
    r'//'
    t.value = 'IDIV'
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/', '%', 'IDIV'), # modulus and integer division
    ('right', 'UMINUS'),
    ('right', '^'), # exponentiation
)

# dictionary of names
names = {}

def p_statement_assign(p):
    'statement : NAME "=" expression'
    p[0] = Assignment(p[1], p[3], variables.index(p[1]))


def p_statement_expr(p):
    'statement : expression'
    p[0] = Statement(p[1])


def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression '%' expression
                  | expression IDIV expression
                  | expression '^' expression''' # modulus, integer division, and exponentiation
    p[0] = BinaryOp(p[1], p[3], p[2])


def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = UnaryOp(p[2], "UMINUS")


def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]


def p_expression_number(p):
    '''expression : INT
                  | FLOAT'''
    p[0] = Number(p[1], constants.index(p[1]))


def p_expression_name(p):
    "expression : NAME"
    try:
        p[0] = Variable(p[1], variables.index(p[1]))
    except LookupError:
        print(f"Undefined name '{p[1]}'")
        p[0] = 0


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
parser = yacc.yacc()

if __name__ == '__main__':
    lines = []
    while True:
        try:
            s = input()
            lines.append(s)
        except EOFError:
            break

    statements = []
    for line in lines:
        if line == "":
            statements.append("\tLOAD_GLOBAL 0\n\tLOAD_CONST 2\n\tCALL_FUNCTION 1")
            continue
        # use the parser defined above to get a statement object
        statement = parser.parse(line)
        # use the eval method of the statement object to get the compiled string
        statements.append(statement.eval())

    out = f'''Function: main/0
Constants: None, 0, "", {', '.join([str(x) for x in constants[3:]])}
Locals: worker {"," if len(variables) > 1 else ""} {",".join([str(x) for x in variables[1:]])}
Globals: print
BEGIN
'''
    statement_counter = 0
    for statement in statements:
        out += f"START{statement_counter}:" + "\n"
        out += statement + "\n"
        out += f"END{statement_counter}:" + "\n"
        statement_counter += 1
    out += "\tLOAD_CONST 0\n\tRETURN_VALUE\nEND\n"
    print(out)