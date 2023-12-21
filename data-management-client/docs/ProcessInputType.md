# ProcessInputType


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_type** | **str** | the data type of the process input | 
**default_value** | **str** | the default value of the process parameter | 
**description** | **str** | a short description of the process input | 
**max_parameter_value_for_numeric_inputs** | **float** | the maximum value that is allowed for the process parameter | [optional] 
**min_parameter_value_for_numeric_inputs** | **float** | the minimum value that is allowed for the process parameter | [optional] 
**name** | **str** | the name of the process input parameter | 

## Example

```python
from openapi_client.models.process_input_type import ProcessInputType

# TODO update the JSON string below
json = "{}"
# create an instance of ProcessInputType from a JSON string
process_input_type_instance = ProcessInputType.from_json(json)
# print the JSON string representation of the object
print ProcessInputType.to_json()

# convert the object into a dict
process_input_type_dict = process_input_type_instance.to_dict()
# create an instance of ProcessInputType from a dict
process_input_type_form_dict = process_input_type.from_dict(process_input_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


