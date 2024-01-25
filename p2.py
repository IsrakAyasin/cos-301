def calculate(string):
    string = string.replace(")", "")
    string = string.replace("(", "")
    list = string.split()
    size = len(list) 

    result = 0
    i=0
    if(size==0):
        print("")
    else:
        while i<size:
            try:
                result+=int(list[i])
                i+=1
            except:
                result-=2*int(list[i+1]) 
                i+=1
        print(result)

def parse(token):
    token = token.replace(" ", "")
    token = token.replace("--", "+")
    token = token.replace("+-", "-")
    token = token.replace("++", "+")
    token = token.replace("-+", "-")
    token = token.replace(")", " ) ")
    token = token.replace("(", "( ")
    
    token = token.replace("+"," ")
    token = token.replace("-"," -")
    token = token.replace("="," = ") 
    list = token.split()   
    return list

def prenthesis(list):
    prenNum = list.count("-(")

    for i in range(prenNum):
        start = list.index("-(")
        end = list.index(")",start)
        list.pop(start)
        while start<end:
            list.insert(start,"-")
            start+=2
        list.pop(end+1)

    result_string = ' '.join(list)
    return(result_string)

try:
    while True:
        token=input()
        list = parse(token)
        list = prenthesis(list)
        calculate(list)
except EOFError:
        print("")