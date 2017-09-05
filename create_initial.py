# IMPORTS

import logging, os

logger = logging.getLogger("create_initial_logger")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

logger.addHandler(ch)

from val_config import val_config as config
# "MAIN" METHOD CALLING

if __name__ == "__main__":
    create_initial()

# CREATING THE INITIAL SERIALIZATION

def create_initial(overwrite = False):
    """
    Adds serialization of all specified objects that are available via the get_current() method
    Specification of "all" is in the config.config file
    """
    import time
    start_time = time.time()
    for object_type in config.get_object_types():
        print "object type: {}".format(object_type)
        add_serialization(object_type, overwrite)
    logger.info("==> Execution time: %s seconds" % (time.time() - start_time))

def create_custom(_obj, id=None):
    custom_id = save_obj(obj=_obj, custom=True, object_type=id)
    return custom_id

def add_serialization(object_type, overwrite = False):
    """
    Adds serialization for a specific object_type.
    """
    logger.info('Adding serialization for object type \'{}\'...'.format(object_type))
    
    from storage.JSONStorageReceiver import JSONStorageReceiver as storage_receiver_class
    storage_receiver = storage_receiver_class()

    logger.info('\'->Receiving data from storage...')
    old_raw = storage_receiver.get(config.get_file_prefix(), object_type, config.get_file_suffix())
    logger.info('\'->Successfully received data from storage!')

    logger.info('\'->Receiving object from RayStation...')
    obj = config.get_object_for_type(object_type)
    logger.info('\'->Successfully received object from RayStation!')

    save_obj(obj, overwrite, old_raw, object_type)

def save_obj(obj, overwrite=True, old_raw=None, object_type=None, custom=False):

    from object_serialization.JSONObjectSerializer import JSONObjectSerializer as serializer_class
    serializer = serializer_class()

    from data_combination.JSONDataCombinator import JSONDataCombinator as data_combination_class
    data_combination = data_combination_class()

    from storage.JSONStorageSaver import JSONStorageSaver as saver_class
    saver = saver_class(custom)

    logger.info('\'->Serializing object...')
    serializer.use(obj)
    serializer.serialize()
    new_raw = serializer.get()
    logger.info('\'->Successfully serialized object!')

    logger.info('\'->Building union of old and new serialized object...')
    if not overwrite:
        data_combination.set_str1(old_raw)
    data_combination.set_str2(new_raw)
    data_combination.combine()
    result = data_combination.get_result()
    logger.info('\'->Successfully built union of old and new serialized object!')

    logger.info('\'->Saving new serialized data...')
    if custom and object_type == None:
        folder = os.path.join(os.path.split(os.path.realpath(__file__))[0],"storage", 'json_storage', "custom")
        object_type = get_new_filename(folder)
    custom_id = saver.save(config.get_file_prefix(), object_type, config.get_file_suffix(), result)
    logger.info('\'->Successfully saved new serialized data!')

    logger.info('Successfully added serialization for object type \'{}\''.format(object_type))

    if custom:
        return object_type

def get_new_filename(folder):
    import os
    i = 0
    while os.path.exists(os.path.join(folder, "{}{}{}".format(config.get_file_prefix(), i, config.get_file_suffix()))):
        i += 1
    return i