class JSONObjectSerializer:
    """
    A class that serializes a given object to JSON
    """
    def use(self, o):
        """
        Method for defining which object shall be used

        @param o: the object to serialize
        """
        self.obj = o
    
    def serialize(self):
        """
        Method that actually serializes the in use() method specified object

        This method will call the JSONObjectPreprocessor
        """
        # Invoke preprocessor first
        from preprocessor.JSONObjectPreprocessor import JSONObjectPreprocessor as pp
        p = pp()
        p.enable_percentage_printing()
        p.use(self.obj)
        p.process()
        self.obj = p.get()

        # Use json to serialize the (now) perfectly structured obj
        import json
        self.obj_json = json.dumps(self.obj, sort_keys=True, indent=4)
        self.obj_json = self.obj_json.replace(": True", ": true")     # that's really ugly... TODO
        self.obj_json = self.obj_json.replace(": False", ": false")   # that's really ugly... TODO

    def get(self):
        """
        Function that will return the serialized object.
        Note: This function will only work when serialize was called previously
        """
        return self.obj_json