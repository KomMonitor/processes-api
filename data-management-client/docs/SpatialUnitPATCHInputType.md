# SpatialUnitPATCHInputType


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**allowed_roles** | **List[str]** | list of role identifiers that have read access rights for this dataset | 
**metadata** | [**CommonMetadataType**](CommonMetadataType.md) |  | 
**next_lower_hierarchy_level** | **str** | the identifier/name of the spatial unit level that contains the features of the nearest lower hierarchy level | 
**next_upper_hierarchy_level** | **str** | the identifier/name of the spatial unit level that contains the features of the nearest upper hierarchy level | 

## Example

```python
from openapi_client.models.spatial_unit_patch_input_type import SpatialUnitPATCHInputType

# TODO update the JSON string below
json = "{}"
# create an instance of SpatialUnitPATCHInputType from a JSON string
spatial_unit_patch_input_type_instance = SpatialUnitPATCHInputType.from_json(json)
# print the JSON string representation of the object
print SpatialUnitPATCHInputType.to_json()

# convert the object into a dict
spatial_unit_patch_input_type_dict = spatial_unit_patch_input_type_instance.to_dict()
# create an instance of SpatialUnitPATCHInputType from a dict
spatial_unit_patch_input_type_form_dict = spatial_unit_patch_input_type.from_dict(spatial_unit_patch_input_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


