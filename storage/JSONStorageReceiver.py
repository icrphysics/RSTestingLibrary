import os
class JSONStorageReceiver:
    """
    A class that returns raw data from the storage. More specifically it
    returns JSON files from the sub folder "json_storage".
    """
    def __init__(self, _custom=False):
        self.custom = _custom
    
    def use_custom(self):
        self.custom = True
    
    def get(self, prefix, object_type, suffix):
        """
        The method that returns the file content.

        @param prefix: The prefix of the file
        @param object_type: The type of the file that should be loaded (e.g. 'Patient')
        @param suffix: File suffix (e.g. '.json')
        """
        file_name = "{pre}{obj_type}{post}".format(pre=prefix, obj_type=object_type, post=suffix)
        

        #TODO Duplicated Code... 
        folder = os.path.join(os.path.split(os.path.realpath(__file__))[0],'json_storage')
        if self.custom:
            folder = os.path.join(folder, 'custom')
        
        file_path = os.path.join(folder, file_name)
        return self.get_with_filepath(file_path)

    def get_with_filepath(self, file_path):
        full_str = ""
        if os.path.isfile(file_path):
            with open(file_path, "r") as f:
                for line in f:
                    full_str += line
                    
        return full_str