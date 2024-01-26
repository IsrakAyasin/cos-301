def pmpv():    
    variables = {}
    def calculate(list):
        size = len(list) 
        result = 0   

        if(size==0):
            print("")
        else:
            i=0
            while i<size:
                try:
                    result+=int(list[i])
                except:
                    result-=2*int(list[i+1]) 
                i+=1
        return(result)

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

    def parenthesis(list):
        prenNum = list.count("-(")
        for i in range(prenNum):
            start = list.index("-(")
            end = list.index(")",start)
            list.pop(start)
            while start<end:
                list.insert(start,"-")
                start+=2
            list.pop(end+1)

        string = ' '.join(list)
        string = string.replace(")", "")
        string = string.replace("(", "")
        list = string.split()
        return(list)

    try:
        while True:
            token=input()
            list = parse(token)
            list = parenthesis(list)
            # print(list)
            if(list.count("=")):
                variables[list[0]] = calculate(list[2:])
                #print(calculate(list[2:]))
            elif(list[0].isidentifier()):
                print(variables[list[0]])
            else:
                print(calculate(list))
    except EOFError:
            print("")
pmpv()