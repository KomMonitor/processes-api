# IndicatorPUTInputType


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**allowed_roles** | **List[str]** | list of role identifiers that have read access rights for this dataset | 
**applicable_spatial_unit** | **str** |  | 
**default_classification_mapping** | [**DefaultClassificationMappingType**](DefaultClassificationMappingType.md) |  | [optional] 
**indicator_values** | [**List[IndicatorPUTInputTypeIndicatorValues]**](IndicatorPUTInputTypeIndicatorValues.md) | an array of entries containing indicator values and mapping to spatial features via identifiers | 

## Example

```python
from openapi_client.models.indicator_put_input_type import IndicatorPUTInputType

# TODO update the JSON string below
json = "{}"
# create an instance of IndicatorPUTInputType from a JSON string
indicator_put_input_type_instance = IndicatorPUTInputType.from_json(json)
# print the JSON string representation of the object
print IndicatorPUTInputType.to_json()

# convert the object into a dict
indicator_put_input_type_dict = indicator_put_input_type_instance.to_dict()
# create an instance of IndicatorPUTInputType from a dict
indicator_put_input_type_form_dict = indicator_put_input_type.from_dict(indicator_put_input_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


