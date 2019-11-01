import DummyDB
import sys

DB = DummyDB.DummyDB()

terminale = ("Expr", "Inp")
nterminale = {terminale[0]:("SELECT", "FROM", "CREATE", "WITH", "SET", "TO", "IN", "SAVE", "HALLO", "LOAD"), terminale[1]:("*", "KEYS")}

tokens = []
content = []

programm_counter = 0

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
            c[j] = c[j].upper()
            for key in nterminale:
                b = c[j]
                if b in nterminale.get(key):
                    tokens.append(key)
            if list(c[j])[-1] == ";" and key != terminale[0]:
                if c[0] == "SELECT" and not ("\'" in list(c[j]) or "\"" in list(c[j])):
                    tokens.append(terminale[1])
                elif c[0] != "SELECT":
                    tokens.append(terminale[1])
            if list(c[j])[0] == "\"" and list(c[j])[-1] == "\"" or list(c[j])[0] == "\'"  and list(c[j])[-1] == "\'" \
                    and len(list(c[j])) > 2:
                tokens.append(terminale[1])
            if c[j] in [str(n) for n in range(10)]:
                tokens.append(terminale[1])
            if list(c[j])[-1] == ",":
                tokens.append(terminale[1])
                tokens.append(terminale[0])

        if(grammar_check()):
            parser()
        else:
            print("Die Anweisung ist nicht richtig")

def grammar_check():
    global tokens
    global terminale
    #print(tokens)
    buffer = None
    order = 0
    for i in range(len(tokens)):
        if buffer is None and tokens[i] == terminale[0]:
            order = 1
        elif buffer is None and tokens[i] != terminale[0]:
            return 0
        if buffer is not None:
            if tokens[i] == terminale[0] and tokens[i - 1] != terminale[0]:
                order += 1
            elif tokens[i] == terminale[0] and tokens[i - 1] == terminale[0]:
                return 0
            if tokens[i] == terminale[1] and tokens[i - 1] == terminale[0]:
                order -= 1
            elif tokens[i] == terminale[1] and tokens[i - 1] != terminale[0]:
                return 0
        buffer = tokens[i]
    if order == 0:
        return 1
    return 0


def parser():
    global content
    global tokens
    global programm_counter

    columns = []
    print(programm_counter)
    content_buffer = content[programm_counter].split()
    #print (content[programm_counter].split())
    token_buffer = tokens
    for i in range(len(content_buffer)):
        try:
            if i == token_buffer.index("Expr"):
                content_buffer[i] = content_buffer[i].upper()
                token_buffer[i] = None
        except ValueError:
            pass

    if content_buffer[0].upper() == "SELECT":
        print(DB.get(content_buffer[1].upper(), content_buffer[content_buffer.index("FROM") + 1].split(";")[0]))
        tokens = []
    elif content_buffer[0].upper() == "CREATE":
        for i in range(content_buffer.index("WITH") + 1, len(content_buffer)):
            columns.append(content_buffer[i])
        DB.create(columns, content_buffer[1])
        tokens = []
    elif content_buffer[0].upper() == "SET":
        DB.set(content_buffer[1], content_buffer[content_buffer.index("TO") + 1].replace(";",""), content_buffer[content_buffer.index("IN") + 1])
        tokens = []
    elif content_buffer[0].upper() == "SAVE":
        Save = DB.get_all()
        columns = ""
        with open(content_buffer[-1].replace(";", "").replace("\"", "").replace("\'", ""), "a+") as file:
            for i in range(len(Save)):
                for key in list(Save[i][1].keys()):
                    if list(Save[i][1]).index(key) != len(list(Save[i][1].keys())) - 1:
                        if type(key)  == int:
                            columns += str(key) + ", "
                        if type(key) == str:
                            columns += "\"{}\"".format(key) + ", "
                    else:
                        if type(key)  == int:
                            columns += str(key)
                        if type(key) == str:
                            columns += "\"{}\"".format(key)
                file.writelines("CREATE {} WITH {};".format(Save[i][0], columns) + "\n")
                columns = ""
                for j in list(Save[i][1].items()):
                    for k in j:
                        if type(j[0]) == str:
                            key = "\"{}\"".format(j[0])
                        else:
                            key = j[0]
                        if j.index(k) != 0:
                            file.writelines("SET {} IN {} TO {}; \n".format(key, Save[i][0], k))
        tokens = []

    elif content_buffer[0] == "HALLO":
        tokens = []
        content = []
        programm_counter = 0
        temp_content_buffer = content_buffer[1]
        content_buffer = []
        tokenizer(temp_content_buffer.replace(";","").replace("\"","").replace("\'",""))
    else:
        print("Anweisung ist semantisch sinnlos")
    programm_counter += 1

def run():
    args = sys.argv
    #print(args)
    cmd = ""
    if args[-1] != "-f" and "-f" in args and "-c" not in args:
        try:
            file = args[args.index("-f") + 1]
            tokenizer(file)
        except ValueError as e:
            print(e)
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