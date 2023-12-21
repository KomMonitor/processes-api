# SpatialUnitPOSTInputType


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**allowed_roles** | **List[str]** | list of role identifiers that have read access rights for this dataset | 
**geo_json_string** | **str** | a valid GeoJSON string containing the features consisting of a geometry and a unique identifier as property &#39;uuid&#39; | 
**json_schema** | **str** | a JSON schema as string that defines the data model for this dataset. It can be used to validate the geoJsonString property. | 
**metadata** | [**CommonMetadataType**](CommonMetadataType.md) |  | 
**next_lower_hierarchy_level** | **str** | the identifier/name of the spatial unit level that contains the features of the nearest lower hierarchy level | 
**next_upper_hierarchy_level** | **str** | the identifier/name of the spatial unit level that contains the features of the nearest upper hierarchy level | 
**period_of_validity** | [**PeriodOfValidityType**](PeriodOfValidityType.md) |  | 
**spatial_unit_level** | **str** | the name and identifier of the spatial unit level the features apply to | 

## Example

```python
from openapi_client.models.spatial_unit_post_input_type import SpatialUnitPOSTInputType

# TODO update the JSON string below
json = "{}"
# create an instance of SpatialUnitPOSTInputType from a JSON string
spatial_unit_post_input_type_instance = SpatialUnitPOSTInputType.from_json(json)
# print the JSON string representation of the object
print SpatialUnitPOSTInputType.to_json()

# convert the object into a dict
spatial_unit_post_input_type_dict = spatial_unit_post_input_type_instance.to_dict()
# create an instance of SpatialUnitPOSTInputType from a dict
spatial_unit_post_input_type_form_dict = spatial_unit_post_input_type.from_dict(spatial_unit_post_input_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


