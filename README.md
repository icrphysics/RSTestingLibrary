# RayStation Testing environment

## About

The testing environment can be used to build tests and execute them without the real RayStation environment.

### TO-DO List for RayStation Update
1.	Adapt `val_config` > `val_config.py`
2.	Generate JSON files with the `create_initial module`

## HOW-TO
### Using the testing library for dummy objects in unit tests
#### Using default objects
Default objects are standard ray station objects. At minimum these are all objects that can be accessed via the `connect.get_current` function (e.g. `Patient`, `BeamSet`, `Case`, …). To receive a default dummy object `import rslOffline` and type `rslOffline.get_current("Patient")` or any other object type you want to use.
#### Create and use smaller object units
If you want your test to be independent of the outer structure of an object you can serialize your own smaller objects and reuse them later on. But you will have to regenerate them every time the version updates. So please be careful with when to use it. Only use it if the testing quality improves significantly.

Import the `create_initial` module in your RayStation scripting environment. Then type e.g. `create_initial.create_custom(patient.Cases[0].PatientModel)`. You can also enter an additional parameter that defines a name. Be careful, the name could already be in use. Please check in advance. If no name is provided, a unique name will be generated and returned. Use the returned name or your specified name later on to receive that object in your tests. To do so `import rslOffline` and enter `rslOffline.get(file_id="your_file_id")` .
#### Query for objects that were already generated
If you want to test smaller object units but don't have a lot of custom requirements for it please try out if an objects that fulfils your needs has already been generated. To do so you can receive a matching object by using the `rslOffline.get()` function with a `lamda` expression for the `spec` parameter. As soon as your lambda function returns true, the object will be returned. Example:

```python
rslOffline.get(spec = lambda x: (hasattr(x, "planType") and x.planType == "yourRequiredValue"))
```

You can restrict your query to default files only or one specific default file by using the `default` parameter and either setting it to `True` (for all default objects) or to the default object name (e.g. `"Patient"`).