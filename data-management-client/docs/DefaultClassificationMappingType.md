# DefaultClassificationMappingType


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**color_brewer_scheme_name** | **str** | the name of the colorBrewer color scheme jused to define the colors for classification (see project http://colorbrewer2.org/#type&#x3D;sequential&amp;scheme&#x3D;BuGn&amp;n&#x3D;3 for colorSchemes). Set to &#39;INDIVIDUAL&#39; if colors are set arbitrarily. | 
**items** | [**List[DefaultClassificationMappingItemType]**](DefaultClassificationMappingItemType.md) | array of classification mapping items. The order of the items corresponds to indicator value intervals from low to high. The number of items represents the number of classes. In combination they represent the default classification and mapping to custom rating of the indicator values | 

## Example

```python
from openapi_client.models.default_classification_mapping_type import DefaultClassificationMappingType

# TODO update the JSON string below
json = "{}"
# create an instance of DefaultClassificationMappingType from a JSON string
default_classification_mapping_type_instance = DefaultClassificationMappingType.from_json(json)
# print the JSON string representation of the object
print DefaultClassificationMappingType.to_json()

# convert the object into a dict
default_classification_mapping_type_dict = default_classification_mapping_type_instance.to_dict()
# create an instance of DefaultClassificationMappingType from a dict
default_classification_mapping_type_form_dict = default_classification_mapping_type.from_dict(default_classification_mapping_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


