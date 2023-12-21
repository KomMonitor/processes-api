# IndicatorPATCHInputType


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**allowed_roles** | **List[str]** | list of role identifiers that have read access rights for this dataset | 

## Example

```python
from openapi_client.models.indicator_patch_input_type import IndicatorPATCHInputType

# TODO update the JSON string below
json = "{}"
# create an instance of IndicatorPATCHInputType from a JSON string
indicator_patch_input_type_instance = IndicatorPATCHInputType.from_json(json)
# print the JSON string representation of the object
print IndicatorPATCHInputType.to_json()

# convert the object into a dict
indicator_patch_input_type_dict = indicator_patch_input_type_instance.to_dict()
# create an instance of IndicatorPATCHInputType from a dict
indicator_patch_input_type_form_dict = indicator_patch_input_type.from_dict(indicator_patch_input_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


