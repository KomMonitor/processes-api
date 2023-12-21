# DefaultClassificationMappingItemType


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**default_color_as_hex** | **str** | the default color for the specified value interval as hex string inclusive leading #, i.e. &#39;#ffffff&#39; | 
**default_custom_rating** | **str** | the default custom rating string for the specified value interval, i.e. &#39;very high&#39;/&#39;very low&#39; or &#39;good&#39;/&#39;bad&#39; | 

## Example

```python
from openapi_client.models.default_classification_mapping_item_type import DefaultClassificationMappingItemType

# TODO update the JSON string below
json = "{}"
# create an instance of DefaultClassificationMappingItemType from a JSON string
default_classification_mapping_item_type_instance = DefaultClassificationMappingItemType.from_json(json)
# print the JSON string representation of the object
print DefaultClassificationMappingItemType.to_json()

# convert the object into a dict
default_classification_mapping_item_type_dict = default_classification_mapping_item_type_instance.to_dict()
# create an instance of DefaultClassificationMappingItemType from a dict
default_classification_mapping_item_type_form_dict = default_classification_mapping_item_type.from_dict(default_classification_mapping_item_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


