# GeoresourceReferenceType

a reference to georesource, e.g. a resource that is used to compute the main indicator

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**referenced_georesource_description** | **str** | a meaningful description of how the referenced georesource is related to the main indicator | 
**referenced_georesource_id** | **str** | unique identifier of the referenced georesource | 
**referenced_georesource_name** | **str** | the meaningful name of the referenced georesource | 

## Example

```python
from openapi_client.models.georesource_reference_type import GeoresourceReferenceType

# TODO update the JSON string below
json = "{}"
# create an instance of GeoresourceReferenceType from a JSON string
georesource_reference_type_instance = GeoresourceReferenceType.from_json(json)
# print the JSON string representation of the object
print GeoresourceReferenceType.to_json()

# convert the object into a dict
georesource_reference_type_dict = georesource_reference_type_instance.to_dict()
# create an instance of GeoresourceReferenceType from a dict
georesource_reference_type_form_dict = georesource_reference_type.from_dict(georesource_reference_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


