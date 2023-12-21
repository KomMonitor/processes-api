# SpatialUnitPUTInputType


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**geo_json_string** | **str** | a valid GeoJSON string containing the features consisting of a geometry and a unique identifier as property &#39;uuid&#39; | 
**period_of_validity** | [**PeriodOfValidityType**](PeriodOfValidityType.md) |  | 
**is_partial_update** | **bool** | if set to TRUE, then a partial upload of geometries is possible. Missing features that are already in the database will then not be deleted | 

## Example

```python
from openapi_client.models.spatial_unit_put_input_type import SpatialUnitPUTInputType

# TODO update the JSON string below
json = "{}"
# create an instance of SpatialUnitPUTInputType from a JSON string
spatial_unit_put_input_type_instance = SpatialUnitPUTInputType.from_json(json)
# print the JSON string representation of the object
print SpatialUnitPUTInputType.to_json()

# convert the object into a dict
spatial_unit_put_input_type_dict = spatial_unit_put_input_type_instance.to_dict()
# create an instance of SpatialUnitPUTInputType from a dict
spatial_unit_put_input_type_form_dict = spatial_unit_put_input_type.from_dict(spatial_unit_put_input_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


