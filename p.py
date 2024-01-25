class PMPVInterpreter:
    def __init__(self):
        self.variables = {}

    def evaluate_expression(self, expression):
        # Tokenize the expression
        tokens = expression.split()

        # Initialize variables
        current_operator = '+'
        result = 0

        # Iterate through tokens
        for token in tokens:
            if token == '+':
                current_operator = '+'
            elif token == '-':
                current_operator = '-'
            elif token.isdigit():
                num = int(token)
                if current_operator == '+':
                    result += num
                elif current_operator == '-':
                    result -= num

        return result

    def interpret(self, program):
        lines = program.split('\n')

        for line in lines:
            if not line.strip():
                continue  # Skip empty lines

            # Split the line into parts
            parts = line.split('=')
            if len(parts) == 2:
                # Variable assignment
                variable_name = parts[0].strip()
                expression = parts[1].strip()
                result = self.evaluate_expression(expression)
                self.variables[variable_name] = result
            else:
                # Variable lookup
                variable_name = line.strip()
                result = self.variables.get(variable_name, None)
                if result is not None:
                    print(result)
sample_input = """
3 + 5 - -2 - 2
x = 3 + 5 - -2 - 2
y = x - (x - 2)
y
ans = (17 - (5 - 20)) - (1 - 11)
ans
"""

# Create and run the interpreter
interpreter = PMPVInterpreter()
interpreter.interpret(sample_input)



def pmpvi(program):
    variables = {}

    def evaluate_expression(expr):
        if isinstance(expr, int):
            return expr
        elif expr[0] == '-':  # Handle unary negation
            return -evaluate_expression(expr[1:])
        elif expr[0] == '(':
            return evaluate_expression(expr[1:-1])
        else:
            lhs = evaluate_expression(expr[:expr.find('+')])
            rhs = evaluate_expression(expr[expr.find('+')+1:])
            return lhs + rhs  # Only addition supported for simplicity

    for line in program.splitlines():
        line = line.strip()
        if not line:
            continue

        if '=' in line:
            var_name, expr = line.split('=')
            result = evaluate_expression(expr.strip())
            variables[var_name] = result
        else:
            result = evaluate_expression(line)
            print(result)
pmpvi("1+2")


elif(list[i+1] == "-"):
                    print(int(list[i])-int(list[i+2]))
                    i+=3