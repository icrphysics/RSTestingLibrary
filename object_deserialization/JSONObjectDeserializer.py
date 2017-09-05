from rmh.test.rslMocks import AttrDict as Map
from rmh.test.rslMocks import RslSequence
from rmh.test.val_config import val_config

class JSONObjectDeserializer:
    """
    A class that serializes a given object to JSON
    """
    def use(self, s):
        """
        Should be used to set the string that should be deserialized
        """
        self.str = s
        self.id_list = {}
    
    def deserialize(self):
        """
        Does the deserialization
        """
        import json
        d = json.loads(self.str)
        self.obj = self.dictToMap(d)
        self.removeReferences(self.obj)
        

    def removeReferences(self, d, path = ""):
        if type(d) == Map:
            for key in d:
                pp = "{}.{}".format(path, key)
                if isinstance(d[key], Map) and "id_reference" in d[key] and d[key]["id_reference"] == True and d[key]["__RayStation_ID"] != None:
                    d[key] = self.id_list["id_{}".format(d[key]["__RayStation_ID"])]
                else:
                    self.removeReferences(d[key], pp)
        elif type(d) == RslSequence:
            for key in range(d.Count):
                pp = "{}.{}".format(path, key)
                if isinstance(d[key], Map) and "id_reference" in d[key] and d[key]["id_reference"] == True and d[key]["__RayStation_ID"] != None:
                    d[key] = self.id_list["id_{}".format(d[key]["__RayStation_ID"])]
                else:
                    self.removeReferences(d[key], pp)
                
    def dictToMap(self, d):
        """
        Converts a dict into a class-like object (attributes can be accessed with ".")
        """
        
        
        o = None
        if isinstance(d, dict) and "type" in d and d.get("type") == "function":
            return self.get_fake_function(d)
        if isinstance(d, dict):
            for key in d:
                d[key] = self.dictToMap(d[key])
            o = Map(d)
        elif isinstance(d, list):
            for key, v in enumerate(d):
                d[key] = self.dictToMap(d[key])
            o = RslSequence(d)
        else:
            o = d
            
        if isinstance(d, dict) and "id_reference" in d and d.get("id_reference") == True:
            pass
        elif isinstance(d, dict) and "__RayStation_ID" in d and d.get("__RayStation_ID") != None:
            self.id_list["id_{}".format(d.get("__RayStation_ID"))] = o
            
        return o
        

    def get_fake_function(self, d):
        """
        Returns a fake function that checks on the existance of a the necessary params.
        @param d: a dict that needs to contain the "params" field
        @returns a function that throws a ValueError when too many arguments are given. If not the enough arguments are given it will print a message.
        """
        params = d.get("params")
        def f(**kwargs):
            for p in params:
                if not p in kwargs:
                    print "[Info] Parameter \"{}\" missing!".format(p) #TODO: How to handle this?
            for k in kwargs:
                if not k in params:
                    raise ValueError("Wrong keyword argument given: {}".format(k))
        return f

    def get(self):
        """
        Returns the deserialized object
        """
        return self.obj