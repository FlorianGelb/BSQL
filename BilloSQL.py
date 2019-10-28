terminale = ("Expr", "Inp")
nterminale = {terminale[0]:("SELECT", "FROM"), terminale[1]:"*"}

tokens = []

def file_parser(file):
    content = []
    with open(file) as f:
        for line in f.read().split("\n"):
            content.append(line)
    return content

def tokenizer(file):
    global tokens
    content = file_parser(file)
    for i in range(len(content)):
        content[i].upper()
        c = content[i].split()
        for j in range(len(c)):
            if c[j].islower():
                c[j] = c[j].upper()
            for key in nterminale:
                b = c[j]
                if b.split(";")[0] in nterminale.get(key):
                    tokens.append(key)
            if list(c[j])[-1] == ";" and key != terminale[0] and not ("\'" in list(c[j]) or "\"" in list(c[j])):#(list(c[j])[0] == "\"" or list(c[j])[0] == "\'" or list(c[j])):
                tokens.append(terminale[1])
            if list(c[j])[0] == "\"" and list(c[j])[-1] == "\"" or list(c[j])[0] == "\'"  and list(c[j])[-1] == "\'" \
                    and len(list(c[j])) > 2:
                tokens.append(terminale[1])

    if(grammar_check()):
        print("Die Anweisung ist richtig")
    else:
        print("Die Anweisung ist nicht richtig")

def grammar_check():
    global tokens
    global terminale
    buffer = None
    order = 0
    for i in range(len(tokens)):
        if buffer == None and tokens[i] == terminale[0]:
            order = 1
        elif buffer == None and tokens[i] != terminale[0]:
            return 0
        if buffer != None:
            if tokens[i] == terminale[0]:
                order += 1
            if tokens[i] == terminale[1]:
                order -= 1
        buffer = tokens[i]
    if order == 0:
        return 1
    return 0

def run():
    tokenizer("Goal.txt")

run()