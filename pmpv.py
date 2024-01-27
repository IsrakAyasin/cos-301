def pmpv():
    variables = {}
    
    def calculate(expression):
        result = 0
        stack = []
        sign = 1
        
        for i in expression:
            if i == '(':
                stack.append((result, sign))
                result = 0
                sign = 1
            elif i == ')':
                last_result, last_sign = stack.pop()
                result = last_result + last_sign * result
            elif i.isnumeric():
                result += sign * int(i)
            elif i.isidentifier():
                result += sign * variables[i]
            elif i == '+':
                sign = 1
            elif i == '-':
                sign = -1
        return(result)

    def parse(token):
        token = token.replace(" ", "")
        token = token.replace("--", "+")
        token = token.replace("+-", "-")
        token = token.replace("++", "+")
        token = token.replace("-+", "-")
        token = token.replace(")", " ) ")
        token = token.replace("(", "( ")
        token = token.replace("+", " + ")
        token = token.replace("-", " - ")
        token = token.replace("=", " = ")
        return token.split()

    try:
        while True:
            user_input = input()
            token_list = parse(user_input)
            if(len(user_input)==0):
                print("")
            elif '=' in token_list:
                variables[token_list[0]] = calculate(token_list[2:])
            else:
                print(calculate(token_list))
    except EOFError:
        print("")
pmpv()