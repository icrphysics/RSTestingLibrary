from contextlib import contextmanager
import os
# --------------- #
import logging
logger = logging.getLogger("create_initial_logger")
logger.setLevel(logging.DEBUG)

#ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)

#logger.addHandler(ch)

from val_config import val_config


def get_current(object_type=None, custom = False, file_path=None):
    """
    Mimic operation of the RayStation connect.get_current() module
    returning dummy test objects
    """
    logger.info('Building fake object for object type \'{}\'...'.format(object_type))
    
    from storage.JSONStorageReceiver import JSONStorageReceiver as storage_receiver_class
    storage_receiver = storage_receiver_class(custom)

    from object_deserialization.JSONObjectDeserializer import JSONObjectDeserializer as deserialization_class
    deserializer = deserialization_class()

    logger.info('  \'->Receiving data from storage...')
    old_raw = ""
    if file_path is None:
        old_raw = storage_receiver.get(val_config.get_file_prefix(), object_type, val_config.get_file_suffix())
    else:
        old_raw = storage_receiver.get_with_filepath(file_path)
    logger.info('  \'->Successfully received data from storage!')

    logger.info('  \'->Deserializing data...')
    deserializer.use(old_raw)
    deserializer.deserialize()
    obj = deserializer.get()
    logger.info('  \'->Successfully deserialized data from storage!')
    
    logger.info('  \'->Replacing important functions')
    val_config.replace_specific_attributes(object_type, obj)
    logger.info('  \'->Successfully replaced important functions')

    logger.info('Successfully built fake object for object type \'{}\'!'.format(object_type))
    return obj



def get(**kwargs):
    """
    Parameters
    ----------
    file_id : string
        File ID of the json file to load
    default : string
        If given and no "spec" parameter is given then the get_current will be called with the value specified.
        Example: get(default="Patient") is equivalent to get_current("Patient")
    spec : lamda function
        Will look through all files (custom and default) to look if the given lamda expression returns true for the transferred object.
        If it does the object will be returned. If no match is found None will be returned.
        If "default" parameter is given it will only check
            a) the given default object if "default" is string (e.g. "Patient")
            b) all default files (e.g. Patient, BeamSet, ...) if "default" is "True"
    """
    if kwargs.get("file_id"):
        return get_current(kwargs.get("file_id"), True)
    
    if kwargs.get("default") and not kwargs.get("spec"):
        return get_current(kwargs.get("default"))

    if kwargs.get("spec"):
        object_types = None
        if isinstance(kwargs.get("default"), basestring):
            #Only look through the specified default object
            object_types = [kwargs.get("default")]
        elif kwargs.get("default") == True:
            #Only look through all the default objects
            object_types = val_config.get_object_types()
        
        files = []
        cdir = os.path.split(os.path.realpath(__file__))[0]
        json_storage_dir = os.path.join(cdir, "storage", "json_storage")
        custom_dir = os.path.join(json_storage_dir, "custom")
        if object_types is None:
            #It was not specified which files to search. Add the custom files to the files to look through
            files = [os.path.join(custom_dir, x) for x in os.listdir(custom_dir) if x.endswith(".json")]
            object_types = val_config.get_object_types()
        files.extend([os.path.join(json_storage_dir, "{}{}{}".format(val_config.get_file_prefix(), x, val_config.get_file_suffix())) for x in object_types])
        for f in files:
            obj = get_current(file_path=f)
            if kwargs.get("spec")(obj):
                return obj
            else:
                print "{} doesn't fit the lamda specs.".format(f)
        return None
# --------------- #

@contextmanager
def CompositeAction(name):
    print "<Starting undo block : %s>" % name
    yield
    print "<Ending undo block : %s>" % name

# --------------- #

class RslOfflineException(Exception):
    """
    Custom exception
    """
    pass