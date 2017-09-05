"""
Provide a list accessible like a ScriptCollection object and 
a dictionary object with keys accessible as attributes
i.e. with the . operator

Useful for mocking up objects that look like Raystation objects for testing purposes.
"""

# ------------------------------- #

from collections import MutableSequence
from copy import deepcopy

# ------------------------------- #

class RslSequenceException(Exception):
    pass
    
# ------------------------------- #

class RslSequence(MutableSequence):
    """
    Custom list that implements .Count property
    """
    def __init__(self, *args, **kwargs):
        self._list = list()
        if len(args) > 0:
            if isinstance(args[0], MutableSequence):
                self._list = args[0]
            else:
                self._list = [args[0]]
            
    def __len__(self): 
        #raise Exception('Should not use len() with .net Collection objects Use .Count instead')
        return len(self._list)
        
    def __getitem__(self, ind):
        if type(ind) == int:
            return self._list[ind]
        elif type(ind) == str:
            for element in self._list:
                if type(element) is AttrDict: 
                    if 'Name' in element.keys() and element.Name == ind:
                        return element
                    elif 'OfRoi' in element.keys() and element.OfRoi.Name == ind:
                        return element
                    elif 'OfPoi' in element.keys() and element.OfPoi.Name == ind:
                        return element
                    elif 'OnExamination' in element.keys() and element.OnExamination.Name == ind:
                        return element
                        
        elif isinstance(ind, slice):
            start, stop, stride = ind.indices(len(self._list))
            return RslSequence([ self[ii] for ii in range(start, stop, stride) ])
        
        return self._list[0]
        
    def __delitem__(self, ind):
        del self._list[ind]
    
    def __setitem__(self, ind, val):
        try:
            self._list[ind] = val
        except IndexError:
            self._list.insert(ind, val)
    
    def __str__(self):
        return str(self._list)
    
    def __iter__(self):
        return iter(self._list)
    
    def __eq__(self, other):
        return self._list == other
    
    def insert(self, ind, val):
        self._list.insert(ind, val)
    
    def append(self, val):
        self._list.append(val)
        
    @property
    def Count(self):
        return len(self._list)

# ------------------------------- #

class AttrDict(dict):
    """
    A dictionary object with keys accessible as attributes
    i.e. with the . operator
    """
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self
            
    # ----- #
    
    def copy(self):
        result = AttrDict()
        
        for key1, val1 in self.__dict__.items():
        
            try:
                self._copyItem(result, key1, val1)
            except ValueError as ve:
                # In event of value error try again
                print('Problem copying key %s. Retrying ..' % key1)
                self._copyItem(result, key1, val1)
        
        return result
    
    # ----- #
    
    def __repr__(self):
        return super(AttrDict, self).__repr__()
    
    # ----- #
    
    def _copyItem(self, result, key1, val1):
        """
        Copy the dict item specified by key1 and val1 into result
        
        Sometimes this randomly throws a ValueError in isinstance test
        due to an intermittent bug in ironpython 2.7.1
        """
        if isinstance(val1,dict):
            setattr(result, key1, self._copySubDict(key1, val1))
        elif isinstance(val1, MutableSequence):
            
            if type(val1) is RslSequence:
                setattr(result, key1, RslSequence())
            else:
                setattr(result, key1, [])
                
            for vi in val1:
                if isinstance(vi,dict):
                    result[key1].append(self._copySubDict(key1, vi))
                else:
                    result[key1].append(vi)
                    
        else:
            setattr(result, key1, val1)
        
    # ----- #
    
    def _copySubDict(self, ky, val):
        """
        Continue recursively copying sub dictionary objects
        Except for certain keys where by value copying is stopped
        to prevent memory overflow and infinte recursion.
        """
        if ky == 'ForBeamSet':
            return val
        if ky == 'ForBeam':
            return val
        if ky == 'ForRegionOfInterest':
            return val
        if ky == 'ForSegment':
            return val
        if ky == 'ForTargetRoi':
            return val
        if ky == 'ForDoseGridStructures':
            return val
        if ky == 'ForTreatmentSetup':
            return val
        if ky == 'ForRtpFunctions':
            return val
            
        if ky == 'OfRoi':
            return val 
        if ky == 'OfPoi':
            return val
        if ky == 'OfTreatmentSetup':
            return val
        if ky == 'OfTargetDoseGridRoi':
            return val
            
        if ky == 'OnDensity':
            return val
        if ky == 'OnStructure':
            return val
        
        if ky == 'Boli':
            return val
        if ky == 'Blocks':
            return val
        if ky == 'SetupBeams':
            return val
        if ky == 'LocalizationPoiGeometrySource':
            return val
        if ky == 'BeamListSource':
            return val
        
        # There is a rare intermittent bug in dict copy
        # If it is encountered then try operation again
        # This hack can be removed when ironpython is updated
        try:
            return val.copy()
        except (SystemError, ValueError) as err:
            print(err)
            print('Problem copying %s. Retrying ..' % ky)
            return val.copy()
            
# ------------------------------- #

# ------------------------------- #