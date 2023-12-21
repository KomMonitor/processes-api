# SpatialUnitOverviewType


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**allowed_roles** | **List[str]** | list of role identifiers that have read access rights for this dataset | 
**available_periods_of_validity** | [**List[PeriodOfValidityType]**](PeriodOfValidityType.md) |  | [optional] 
**metadata** | [**CommonMetadataType**](CommonMetadataType.md) |  | 
**next_lower_hierarchy_level** | **str** | the identifier/name of the spatial unit level that contains the features of the nearest lower hierarchy level | 
**next_upper_hierarchy_level** | **str** | the identifier/name of the spatial unit level that contains the features of the nearest upper hierarchy level | 
**spatial_unit_id** | **str** | the unique identifier of the spatial unit level the features apply to | 
**spatial_unit_level** | **str** | the name of the spatial unit level the features apply to | 
**wfs_url** | **str** | the URL of a running WFS instance serving the spatial features of the associated dataset | 
**wms_url** | **str** | the URL of a running WMS instance serving the spatial features of the associated dataset | 
**user_permissions** | **List[str]** | List of permissions that are effective on this dataset for the current user | [optional] 

## Example

```python
from openapi_client.models.spatial_unit_overview_type import SpatialUnitOverviewType

# TODO update the JSON string below
json = "{}"
# create an instance of SpatialUnitOverviewType from a JSON string
spatial_unit_overview_type_instance = SpatialUnitOverviewType.from_json(json)
# print the JSON string representation of the object
print SpatialUnitOverviewType.to_json()

# convert the object into a dict
spatial_unit_overview_type_dict = spatial_unit_overview_type_instance.to_dict()
# create an instance of SpatialUnitOverviewType from a dict
spatial_unit_overview_type_form_dict = spatial_unit_overview_type.from_dict(spatial_unit_overview_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


