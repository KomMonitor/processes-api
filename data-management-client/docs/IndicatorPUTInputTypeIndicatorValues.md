# IndicatorPUTInputTypeIndicatorValues


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**spatial_reference_key** | **str** | identifier (uuid) of the spatial feature to which the values shall be applied | [optional] 
**value_mapping** | [**List[IndicatorPUTInputTypeValueMapping]**](IndicatorPUTInputTypeValueMapping.md) | an array of entries mapping an indicator value to a timestamp as mapping key | [optional] 

## Example

```python
from openapi_client.models.indicator_put_input_type_indicator_values import IndicatorPUTInputTypeIndicatorValues

# TODO update the JSON string below
json = "{}"
# create an instance of IndicatorPUTInputTypeIndicatorValues from a JSON string
indicator_put_input_type_indicator_values_instance = IndicatorPUTInputTypeIndicatorValues.from_json(json)
# print the JSON string representation of the object
print IndicatorPUTInputTypeIndicatorValues.to_json()

# convert the object into a dict
indicator_put_input_type_indicator_values_dict = indicator_put_input_type_indicator_values_instance.to_dict()
# create an instance of IndicatorPUTInputTypeIndicatorValues from a dict
indicator_put_input_type_indicator_values_form_dict = indicator_put_input_type_indicator_values.from_dict(indicator_put_input_type_indicator_values_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


