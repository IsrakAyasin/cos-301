operator="+"
token=input()
token = token.replace(" ", "")

size=len(token)
loc = token.rfind("+")
if loc != -1:
    print(int(token[:loc]) + (int(token[loc+1:])))
