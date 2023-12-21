# IndicatorPATCHDisplayOrderInputType


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**indicator_id** | **str** | unique ID of the associated indicator | 
**display_order** | **float** | the new displayOrder value | 

## Example

```python
from openapi_client.models.indicator_patch_display_order_input_type import IndicatorPATCHDisplayOrderInputType

# TODO update the JSON string below
json = "{}"
# create an instance of IndicatorPATCHDisplayOrderInputType from a JSON string
indicator_patch_display_order_input_type_instance = IndicatorPATCHDisplayOrderInputType.from_json(json)
# print the JSON string representation of the object
print IndicatorPATCHDisplayOrderInputType.to_json()

# convert the object into a dict
indicator_patch_display_order_input_type_dict = indicator_patch_display_order_input_type_instance.to_dict()
# create an instance of IndicatorPATCHDisplayOrderInputType from a dict
indicator_patch_display_order_input_type_form_dict = indicator_patch_display_order_input_type.from_dict(indicator_patch_display_order_input_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


