# ProcessScriptPUTInputType


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** | short description of the scripts content (what does it do) | 
**name** | **str** | name of the process script | 
**required_georesource_ids** | **List[str]** | identifiers of georesources that are used within the script. | 
**required_indicator_ids** | **List[str]** | identifiers of indicators that are used within the script. | 
**script_type** | **str** | a script type reference name used to distuingish process scripts from a client perspective, i.e. setup admin pages due to knowledge about type-specific script parameters and required indicators/georesources | [optional] 
**script_code_base64** | **str** | the actual script code (JavaScript) as BASE64 encoded string | 
**variable_process_parameters** | [**List[ProcessInputType]**](ProcessInputType.md) | list of process parameters that can be set by an expert user. They are used within the script to parameterize the indicator computation | 

## Example

```python
from openapi_client.models.process_script_put_input_type import ProcessScriptPUTInputType

# TODO update the JSON string below
json = "{}"
# create an instance of ProcessScriptPUTInputType from a JSON string
process_script_put_input_type_instance = ProcessScriptPUTInputType.from_json(json)
# print the JSON string representation of the object
print ProcessScriptPUTInputType.to_json()

# convert the object into a dict
process_script_put_input_type_dict = process_script_put_input_type_instance.to_dict()
# create an instance of ProcessScriptPUTInputType from a dict
process_script_put_input_type_form_dict = process_script_put_input_type.from_dict(process_script_put_input_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


