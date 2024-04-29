# -----------------------------------------------------------------------------
# pmpv compile
#
# A simple calculator compiler.
# Created by Israk Ayasin. Source code is from O'Reilly's "Lex and Yacc", p. 63.
# -----------------------------------------------------------------------------

# Import the lexical analyzer generator (Lex)
import ply.lex as lex
import ply.yacc as yacc

# Define the tokens recognized by the lexer
tokens = (
    'NAME', 'NUMBER',
)

# Define literals (characters with a specific meaning)
literals = ['=', '+', '-', '*', '/', '%', '$', '(', ')']

# Initialize variables
function = "Function: main/0"
consList = [None]  # List to store constants
localls = []  # List to store locals
globals = "Globals: print"
start_label = 0
all_results = []  # List to store all the results

# Regular expression for a valid variable name
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# Regular expression for any real number
def t_NUMBER(t):
    r'(\.)?+\d+(\.\d+)?'
    try:
        t.value = int(t.value)
    except:
        t.value = float(t.value)
    return t

# Ignore whitespace and tabs
t_ignore = " \t"

# Track line numbers for better error reporting
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# Handle errors by skipping invalid characters
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lex.lex()

# Define the precedence of operators
precedence = (
    ('left', '+', '-'),
    ('left', '*', '/', '%', '$'),
    ('right', 'UMINUS'),
)

# Define a statement: variable assignment
def p_statement_assign(p):
    'statement : NAME "=" expression'
    global localls, code
    localls.append(p[1]) 
    code.append(f"  STORE_FAST {localls.index(p[1])}")  # Generate the STORE_FAST instruction

# Define an expression as a variable name
def p_expression_name(p):
    "expression : NAME"
    global code
    try:
        code.append(f"  LOAD_FAST {localls.index(p[1])}\n")  # Generate the LOAD_FAST instruction
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0

# Define a statement: standalone expression
def p_statement_expr(p):
    'statement : expression'
    global code
    code.append("  LOAD_GLOBAL 0\n  ROT_TWO\n  CALL_FUNCTION 1")  # Generate the instructions to call the print function

# Define an expression with binary operators
def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression '%' expression
                  | expression '$' expression'''
    
    global code
    if p[2] == '+':
        code.append("  BINARY_ADD")
    elif p[2] == '-':
        code.append("  BINARY_SUBTRACT")
    elif p[2] == '*':
        code.append("  BINARY_MULTIPLY")
    elif p[2] == '/':
        if p[3] != 0:
            code.append("  BINARY_TRUE_DIVIDE")
        else:
            print('Error: Can\'t divide by 0')
    elif p[2] == '$':
        if p[3] != 0:
            code.append("  BINARY_FLOOR_DIVIDE")
        else:
            print('Error: Can\'t divide by 0')
    elif p[2] == '%':
        code.append("  BINARY_MODULO")

# Define an expression with unary minus
def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    global code, consList
    consList.pop(-1)  # Remove the previous value from the constants list
    code.pop(-1)  # Remove the previous instruction from the code
    consList.append(-p[2])  # Add the negated value to the constants list
    code.append(f"  LOAD_CONST {len(consList)-1}")  # Generate the instruction to load the negated value
    p[0] = -p[2]

# Define an expression within parentheses
def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]

# Define an expression as a number
def p_expression_number(p):
    "expression : NUMBER"
    global consList, code
    consList.append(p[1])  # Add the number to the constants list
    code.append(f"  LOAD_CONST {len(consList)-1}")  # Generate the instruction to load the number
    p[0] = p[1]

# Handle syntax errors
def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

# Main loop to read input and parse expressions
yacc.yacc()
s = []
while 1:
    try:
        s.append(input())  # Read input from the user
    except EOFError:
        break

code = []
for i in s:
    if len(i) > 0:
        i = i.replace("//", "$")  # Replace "//" with "$" to handle integer division
        code.append(f"START{start_label}:")  # Add a label to the beginning of the code block
        yacc.parse(i)  # Parse the line
        code.append(f"END{start_label}:")  # Add a label to the end of the code block
        all_results.append(code)  # Add the code block to the list of all results
        start_label += 1
        code = []

# Print the output
print(function)
print("Constants: ", end="")
count1 = 0
for i in consList:
    if count1 != len(consList) - 1:
        print(i, end=", ")
        count1 += 1
    else:
        print(i, end="")
print()
if len(localls) > 0:
    print("Locals: ", end="")
    count = 0
    for i in localls:
        if count != len(localls) - 1:
            print(i, end=", ")
            count += 1
        else:
            print(i, end="")
    print()
print(globals)
print("BEGIN")
for result in all_results:
    for i in result:
        print(i)
print("LOAD_CONST 0\nRETURN_VALUE\nEND")