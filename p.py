while True:
    token=input()
    token = token.replace(" ", "")
    token = token.replace("+", " ")
    list = token.split()
    print(list)