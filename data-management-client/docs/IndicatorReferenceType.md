# IndicatorReferenceType

a reference to another indicator, e.g. a sub-indicator that is used to compute the main indicator

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**referenced_indicator_description** | **str** | a meaningful description of how the referenced indicator is related to the main indicator | 
**referenced_indicator_id** | **str** | unique identifier of the referenced indicator | 
**referenced_indicator_name** | **str** | the meaningful name of the referenced indicator | 

## Example

```python
from openapi_client.models.indicator_reference_type import IndicatorReferenceType

# TODO update the JSON string below
json = "{}"
# create an instance of IndicatorReferenceType from a JSON string
indicator_reference_type_instance = IndicatorReferenceType.from_json(json)
# print the JSON string representation of the object
print IndicatorReferenceType.to_json()

# convert the object into a dict
indicator_reference_type_dict = indicator_reference_type_instance.to_dict()
# create an instance of IndicatorReferenceType from a dict
indicator_reference_type_form_dict = indicator_reference_type.from_dict(indicator_reference_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


