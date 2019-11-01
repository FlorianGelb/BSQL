class DummyDB:

    names = []
    def __init__(self, key = None, value = None, name = None):
        if(key != None and value != None and name != None):
            self.DB[key] = value

    def get_all(self):
        ret = []
        for name in self.names:
            content = eval("self.{}".format(name).replace("\"", "").replace("\'", ""))
            ret.append((name, content))
        return (ret)

    def get(self, key, name):
        exist = False
        key = self.key_type_converter(key)
        try:
            content = eval("self.{}".format(name))
            exist = True
            if key == "*":
                return list(content.values())
            if key == "KEYS":
                return list(content.keys())
        except NameError:
            exist = False
            print("{} existiert nicht in {}".format(key, name))
        except AttributeError as e:
            print(e)
        if exist:
            return content.get(key)

    def create(self, keys, name):
        #print(keys)
        append = ""
        try:
            for key in keys:
                key = self.key_type_converter(key)
                if ";" not in key:
                    append += key.replace(",", "") + ":None, "
                else:
                    append += key.replace(",", "").replace(";", "") + ":None"
            exec("self.{} = {}".format(name.replace("\"", "").replace("\'", ""), "{" + append + "}"))
            self.names.append(name)
            #print(self.Table)
        except NameError:
            print("{} existiert nicht in {}".format(key, name))
        except AttributeError as e:
            print(e)

    def set(self, key, value, name):
        exist = False
        key = self.key_type_converter(key)
        name = name.replace("\"","").replace("\'", "")
        try:
            content = eval("self.{}".format(name).replace(";", ""))
            if key in list(content.keys()):
                exist = True
            else:
                print("Die Spalte {} existiert nicht".format(key))
            if key == "*":
                for key in content.keys:
                    content[key] = value
        except NameError:
            exist = False
            print("{} existiert nicht in {}".format(key, name))
        except AttributeError as e:
            print(e)
        if exist:
            content[key] = value

    def key_type_converter(self, key):
        if list(key)[0] == "\"" and list(key)[-1] == "\"" or list(key)[0] == "\'" and list(key)[-1] == "\'":
            key = key.replace("\'", "").replace("\"", "")
        elif "\"" not in  key or "\'" not in key:
            try:
                key = int(key)
            except ValueError:
                pass
        return key
