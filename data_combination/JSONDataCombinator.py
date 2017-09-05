import json

class JSONDataCombinator:
    """
    Builds the biggest possible union of two JSON strings

    If there are two variables with the same name then the value of object 1 will remain
    """
    def __init__(self):
        self.str1 = None
        self.str2 = None
    
    def set_str1(self, s):
        """
        The first json string which should be used
        """
        self.str1 = s

    def set_str2(self, s):
        """
        The second json string which should be used
        """
        self.str2 = s

    def combine(self):
        """
        Creates a new dict and updates it with two objects
        """
        result = {}
		
        if self.str1:
            obj1 = json.loads(self.str1)
            self.get_union(result, obj1)

        if self.str2:
            obj2 = json.loads(self.str2)
            self.get_union(result, obj2)        

        self.result = json.dumps(result)

    def get_result(self):
        """
        @returns: the with combine() generated new JSON string
        """
        return self.result

    def get_union(self, a, b):
        if type(a) != type(b) and len(a) > 0 and len(b) > 0:
            return a
        elif type(a) != type(b) and len(a) == 0:
            # sometimes empty lists will be saved as empty dicts
            return b
        elif type(a) != type(b) and len(b) == 0:
            return a
        elif a == None:
            return b
        if isinstance(b, list):
            new_l = a
            for i, _b in enumerate(b):
                if i < len(new_l):
                    _a = a[i]
                    new_l[i] = self.get_union(_a, _b)
                else:
                    new_l.append(_b)
            return new_l
        if isinstance(b, dict):
            new_d = a
            for key in b:
                if key in new_d:
                    new_d[key] = self.get_union(a[key], b[key])
                else:
                    new_d[key] = b[key]
            return new_d
        return a