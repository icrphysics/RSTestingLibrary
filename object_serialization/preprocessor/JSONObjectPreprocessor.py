import json
import sys
class JSONObjectPreprocessor:
    """
    A class that preprocesses a given object to create a new object that will without any further adaptions be JSON serializable.

    Things that were thought of:
        '-> Circular references
        '-> Non serializable objects
        '-> C-sharp objects

    Note: This class is very specialized on RayStation Objects
    """ 
    def __init__(self):
        """
        Constructor

        Default values:
            '-> self.obj_ids = []
        """
        self.obj_ids = []
        self.percentage_printing = False

    def set_ids(self, ids):
        """
        Sets the already seen ids of objects by the parent.
        This will be used for detecting circular references
        """
        self.obj_ids = ids

    def get_ids(self):
        """
        After the processing of an object probably new object ids were found.
        The union of previous and new object ids will be returned in this function.

        Note: The value returned will be the set_ids() value if process() was not called.
        """
        return self.obj_ids

    def use(self, o):
        """
        With this method the object to use will be defined.

        @param o: The object to use
        """
        self.obj = o
    
    def enable_percentage_printing(self):
        self.percentage_printing = True
    
    def process(self, callPath=''):
        """
        Processes the in use() defined object and creates a new object representing the old one.
        The new object will be json serializable with json.dumps(...)
        """
        
        c_type = str(type(self.obj))
        c_id = self.__getID()
        c_id_test = c_id is None or c_id not in self.get_ids()
        if self.obj_ids is None:
            self.obj_ids = []
        self.obj_ids.append(c_id)
        #move to config
        if not c_id_test:
            self.obj_end = {
                "id_reference": True
            }
        elif 'ScriptObjectCollection' in c_type and self.obj.Count > 0 and c_id_test:
            self.obj_end = self.__do_children__(collection=True, callPath=callPath)
        elif ('ScriptObject' in c_type or 'ExpandoObject' in c_type) and c_id_test:
            self.obj_end = self.__do_children__(callPath=callPath)
        elif "'Color'" in c_type and c_id_test:
            self.obj_end = self.__do_children__(callPath=callPath, attributes=["A", "R", "G", "B"])
        elif "Byte" in c_type and c_id_test:
            try:
                self.obj_end = int(str(self.obj))
            except:
                self.obj_end = 0
        elif "Array[float]" in c_type and c_id_test:
            self.obj_end = self.__do_children__(collection=True, callPath=callPath, max_children=200)
        else:
            try:
                #Check if object is dumpable
                json.dumps(self.obj)
                self.obj_end = self.obj
                #from copy import deepcopy
                #check if object is deepcopyable
                #obj_end = deepcopy(self.obj)
            except:
                #This is probably a function.
                try:
                    description = self.obj.GetDescription()
                    self.obj_end = self.__function_to_dict(self.obj)
                except:
                    self.obj_end = ""

        if isinstance(self.obj_end, dict) and c_id:
            self.obj_end["__RayStation_ID"] = c_id
    
    def __function_to_dict(self, fct):
        end = {"type": "function", "description": fct.GetDescription()}
        end["params"] = self.__parse_description(end.get("description"))
        return end

    def __parse_description(self, descr):
        position_of_attributes = descr.find("Parameters:")
        substr1 = descr[position_of_attributes:]
        without_parameters_heading = substr1[substr1.find(":\r\n")+len(":\r\n"):]
        
        split_by_line = without_parameters_heading.split("\r\n")
        params = []
        for line in split_by_line:
            if " - " in line and line.startswith("    "):
                param = line.split(" - ")[0].replace(" ", "")
                if param:
                    params.append(param)
            elif line.startswith("  ") and not line.startswith("    "):
                break
        
        return params

    def __do_children__(self, attributes=None, collection = False, callPath='', max_children=1):
        if collection:
            all = []
            for i, c in enumerate(self.obj):
                if i > max_children-1:
                    #TODO: NOT HARDCODED
                    break
                preprocessor = JSONObjectPreprocessor()
                preprocessor.use(c)
                preprocessor.set_ids(self.get_ids())
                new_callPath = '{}.{}'.format(callPath, "[{}]".format(i))
                preprocessor.process(callPath=new_callPath)
                res = preprocessor.get()
                all.append(res)
                self.set_ids(preprocessor.get_ids())
                
            return all
        
        fake_obj = {}
                
        try:
            if attributes == None:
                attributes = [kk for kk in dir(self.obj) if kk[0] != '_']
        except Exception as e:
            print("    DEBUG: Error in {} : {}".format(str(self.obj),callPath))
            if 'InternalError' not in e.message:
                raise e
            return fake_obj
            
        for i, attr in enumerate(attributes):
            #TODO: config
            if attr in ['PixelData', 'DoseData', 'DicomDataSet', 'DeformationMatrix', 'Contours', 'VoxelValues']:
                continue
            preprocessor = JSONObjectPreprocessor()
            preprocessor.use(getattr(self.obj, attr))
            preprocessor.set_ids(self.get_ids())
            new_callPath = '{}.{}'.format(callPath, attr)
            preprocessor.process(callPath=new_callPath)
            res = preprocessor.get()
            fake_obj[attr] = res
            self.set_ids(preprocessor.get_ids())
            if self.percentage_printing:
                sys.stdout.write("\r")
                sys.stdout.write("{:.0%}".format(float(i)/float(len(attributes))))
                sys.stdout.flush()
        sys.stdout.write("\r")  
        
        return fake_obj
    
    def __getID(self):
        """
        Get object ID as string
        """
        str = self.obj.__repr__()
        strInd = str.find("id=")
        if strInd > 0:
            return str[strInd+3:-1]
        else:
            return None

    def get(self):
        return self.obj_end