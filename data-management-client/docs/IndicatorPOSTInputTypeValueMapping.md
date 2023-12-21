# IndicatorPOSTInputTypeValueMapping


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**indicator_value** | **float** | the numeric extent of the indicator for the timestamp | [optional] 
**timestamp** | **date** | timestamp consisting of year, month and day according to ISO 8601 (e.g. 2018-01-30) | [optional] 

## Example

```python
from openapi_client.models.indicator_post_input_type_value_mapping import IndicatorPOSTInputTypeValueMapping

# TODO update the JSON string below
json = "{}"
# create an instance of IndicatorPOSTInputTypeValueMapping from a JSON string
indicator_post_input_type_value_mapping_instance = IndicatorPOSTInputTypeValueMapping.from_json(json)
# print the JSON string representation of the object
print IndicatorPOSTInputTypeValueMapping.to_json()

# convert the object into a dict
indicator_post_input_type_value_mapping_dict = indicator_post_input_type_value_mapping_instance.to_dict()
# create an instance of IndicatorPOSTInputTypeValueMapping from a dict
indicator_post_input_type_value_mapping_form_dict = indicator_post_input_type_value_mapping.from_dict(indicator_post_input_type_value_mapping_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


