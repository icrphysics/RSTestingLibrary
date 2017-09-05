class JSONStorageSaver:
    """
    This class stores raw strings into files. More specifically this 
    class is intended to store json strings in the sub folder "json_storage".
    """
    def __init__(self, _custom=False):
        self.custom = _custom
    
    def use_custom(self):
        self.custom = True
    
    def save(self, prefix, object_type, suffix, raw):
        """
        @param prefix: this is the filename prefix
        @param object_type: the object_type that should be saved (also for file naming purposes)
        @param suffix: this is the filename suffix (e.g. ".json")
        @param raw: The data that should be saved
        """
        file_name = "{pre}{obj_type}{su}".format(pre=prefix, obj_type=object_type, su=suffix)
        import os.path
        folder = os.path.join(os.path.split(os.path.realpath(__file__))[0],'json_storage')

        if self.custom:
            folder = os.path.join(folder, "custom")
        
        file_path = os.path.join(folder, file_name)

        full_str = ""
        with open(file_path, "w") as f:
            f.write(raw)
        
        return full_str