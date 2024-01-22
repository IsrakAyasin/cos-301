while True:
    token=input()
    token = token.replace(" ", "")

    size=len(token)
    for i in token:
        token = token.replace("--", "+")
        token = token.replace("+-", "-")
        token = token.replace("++", "+")
        token = token.replace("-+", "-")
    print(token) 

    loc = token.rfind("+")
    if loc != -1:
        try:
            print(int(token[:loc]) + (int(token[loc+1:])))
        except:
            print("")