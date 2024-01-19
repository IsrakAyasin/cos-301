while True:
    token=input()
    token = token.replace(" ", "")

    size=len(token)
    loc = token.rfind("+")
    if loc != -1:
        try:
            print(int(token[:loc]) + (int(token[loc+1:])))
        except:
            print("huh something's not working")