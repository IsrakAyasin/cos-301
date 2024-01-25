while True:
    token=input()
    token = token.replace(" ", "")
    token = token.replace("--", "+")
    token = token.replace("+-", "-")
    token = token.replace("++", "+")
    token = token.replace("-+", "-")
    token = token.replace(" ", "")
    token = token.replace("- -", "+")
    token = token.replace("+ -", "-")
    token = token.replace("+ +", "+")
    token = token.replace("- +", "-")
    #print(token) 

    size=len(token)
    
    token2 = token.replace("+"," + ")
    token2 = token2.replace("-"," + -")
    token2 = token2.replace("="," = ")
    list = token2.split()
    print(list)
    size2 = len(list)

    action = 0
    action += token.count("+")
    action += token.count("-")
    action += token.count("=")   


    result = 0
    i=0
    while i<size2:     
        if list[i].isdigit():
            try:
                if(list[i+1] == "+"):
                    print(int(list[i])+int(list[i+2]))
                    i+=3           
            except:
                print(list[i])
                i+=1           
        else:
            i+=1
