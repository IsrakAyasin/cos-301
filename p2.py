def calculate(token):
    list = token.split()
    size = len(list) 

    result = 0
    i=0
    while i<size:     
        result+=int(list[i])
        i+=1          
    print(result)

def parse(token):
    token = token.replace(" ", "")
    token = token.replace("--", "+")
    token = token.replace("+-", "-")
    token = token.replace("++", "+")
    token = token.replace("-+", "-")
    token = token.replace(" ", "")
    
    token = token.replace("+"," ")
    token = token.replace("-"," -")
    token = token.replace("="," = ")    
    return token

try:
    while True:
        token=input()
        #pren
        

        token = parse(token)
        calculate(token)
except EOFError:
        print("")