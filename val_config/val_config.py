#####################################
# CONFIG FILE FOR AUTOMATED SCRIPTS #
#####################################

#####################################
#           EDIT THIS PART          #
#####################################

object_types = [
    "Patient",
    "Plan",
    "BeamSet",
    "Case",
    "Examination",
    "MachineDB",
    "PatientDB",
    "ui",
    "Machine"
]

file_prefix = "json_data_R6_" #TODO: "R6" should be replaced by an automatic recognition method
file_suffix = ".json"

def get_object_for_type(object_type):
    try:
        import connect as rsl
    except:
        pass

    if object_type == "Machine":
        return rsl.get_current("MachineDB").GetTreatmentMachine(machineName=rsl.get_current("BeamSet").MachineReference.MachineName, lockMode=None)
    else:
        return rsl.get_current(object_type)

def replace_specific_attributes(object_type, obj):
    import rmh.test.rslOffline
        
    if object_type == "MachineDB":
        def fake_GetTreatmentMachine(machineName=None, lockMode=None):
            return rmh.test.rslOffline.get_current("Machine")
        obj.GetTreatmentMachine = fake_GetTreatmentMachine

        
#####################################
#       DON'T EDIT THIS PART        #
#####################################

def get_object_types():
    return object_types

def get_file_prefix():
    return file_prefix

def get_file_suffix():
    return file_suffix