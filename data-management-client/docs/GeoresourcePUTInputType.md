# GeoresourcePUTInputType


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**geo_json_string** | **str** | a valid GeoJSON string containing the features consisting of a geometry and properties specific to the dataset | 
**period_of_validity** | [**PeriodOfValidityType**](PeriodOfValidityType.md) |  | 
**is_partial_update** | **bool** | if set to TRUE, then a partial upload of geometries is possible. Missing features that are already in the database will then not be deleted | 

## Example

```python
from openapi_client.models.georesource_put_input_type import GeoresourcePUTInputType

# TODO update the JSON string below
json = "{}"
# create an instance of GeoresourcePUTInputType from a JSON string
georesource_put_input_type_instance = GeoresourcePUTInputType.from_json(json)
# print the JSON string representation of the object
print GeoresourcePUTInputType.to_json()

# convert the object into a dict
georesource_put_input_type_dict = georesource_put_input_type_instance.to_dict()
# create an instance of GeoresourcePUTInputType from a dict
georesource_put_input_type_form_dict = georesource_put_input_type.from_dict(georesource_put_input_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


