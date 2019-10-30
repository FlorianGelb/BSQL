class DummyDB:

    DB = {}

    def __init__(self, key = None, value = None, name = None):
        if(key != None and value != None and name != None):
            self.DB[key] = value
        else:
            self.DB["KEY"] = "VALUE"
            self.DB["1"] = "2"
            self.DB[1] = "f"


    def get(self, key, name):
        exist = False
        key = self.key_type_converter(key)
        try:
            content = eval("self.{}".format(name))
            exist = True
            if key == "*":
                return list(content.values())

        except NameError:
            exist = False
            print("{} existiert nicht in {}".format(key, name))
        except AttributeError as e:
            print(e)
        if exist:
            return content.get(key)

    def set(self, key, value):
        self.DB[key] = value

    def key_type_converter(self, key):
        if list(key)[0] == "\"" and list(key)[-1] == "\"" or list(key)[0] == "\'" and list(key)[-1] == "\'":
            key = key.replace("\'", "").replace("\"", "")
        elif "\"" not in  key or "\'" not in key:
            try:
                key = int(key)
            except ValueError:
                pass
        return key
