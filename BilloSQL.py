import DummyDB
import sys

DB = DummyDB.DummyDB()

terminale = ("Expr", "Inp")
nterminale = {terminale[0]:("SELECT", "FROM"), terminale[1]:"*"}

tokens = []
content = []

programm_counter = 0

#def cmd_parser(arg):


def file_parser(file):
    content = []
    with open(file) as f:
        for line in f.read().split("\n"):
            if len(line) > 0:
                content.append(line)
    return content

def tokenizer(file):
    global tokens
    global content
    if file is not None and len(content) == 0:
        content = file_parser(file)
    for i in range(len(content)):
        content[i].upper()
        c = content[i].split()
        for j in range(len(c)):
            if c[j].islower():
                c[j] = c[j].upper()
            for key in nterminale:
                b = c[j]
                if b in nterminale.get(key):
                    tokens.append(key)
            if list(c[j])[-1] == ";" and key != terminale[0] and not ("\'" in list(c[j]) or "\"" in list(c[j])):#(list(c[j])[0] == "\"" or list(c[j])[0] == "\'" or list(c[j])):
                tokens.append(terminale[1])
            if list(c[j])[0] == "\"" and list(c[j])[-1] == "\"" or list(c[j])[0] == "\'"  and list(c[j])[-1] == "\'" \
                    and len(list(c[j])) > 2:
                tokens.append(terminale[1])
            if c[j] in [str(n) for n in range(10)]:
                tokens.append(terminale[1])

        if(grammar_check()):
            parser()
        else:
            print("Die Anweisung ist nicht richtig")

def grammar_check():
    global tokens
    global terminale
    print(tokens)
    buffer = None
    order = 0
    for i in range(len(tokens)):
        if buffer is None and tokens[i] == terminale[0]:
            order = 1
        elif buffer is None and tokens[i] != terminale[0]:
            return 0
        if buffer is not None:
            if tokens[i] == terminale[0]:
                order += 1
            if tokens[i] == terminale[1]:
                order -= 1
        buffer = tokens[i]
    if order == 0:
        return 1
    return 0


def parser():
    global content
    global tokens
    global programm_counter

    content_buffer = content[programm_counter].split()
    print (content[programm_counter].split())
    token_buffer = tokens
    for i in range(len(content_buffer)):
        try:
            if i == token_buffer.index("Expr"):
                content_buffer[i] = content_buffer[i].upper()
                token_buffer[i] = None
        except ValueError:
            pass

    if content_buffer[0].upper() == "SELECT":
        print(DB.get(content_buffer[1], content_buffer[content_buffer.index("FROM") + 1].split(";")[0]))
        tokens = []
    else:
        print("Anweisung ist semantisch sinnlos")
    programm_counter += 1

def run():
    args = sys.argv
    print(args)
    cmd = ""
    if args[-1] != "-f" and "-f" in args and "-c" not in args:
        try:
            file = args[args.index("-f") + 1]
            tokenizer(file)
        except ValueError:
            print("Parameter sind falsch angegeben oder der Pfad existiert nicht")
            exit(1)

    if args[-1] != "-c" and "-c" in args:
        try:
            if "-f" not in args and "-c" in args:
                for i in range(args.index("-c") + 1, len(args)):
                    if i != len(args) - 1:
                        cmd += args[i] + " "
                    else:
                        cmd += args[i]
            content.append(cmd)
            tokenizer(None)
        except ValueError:
            print("Parameter sind falsch angegeben oder der Pfad existiert nicht")
            exit(2)

run()