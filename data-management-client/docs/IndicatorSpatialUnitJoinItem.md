# IndicatorSpatialUnitJoinItem


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**allowed_roles** | **List[str]** | list of role identifiers that have read access rights for this dataset | [optional] 
**spatial_unit_id** | **str** | ID of the applicable spatial unit | 
**spatial_unit_name** | **str** | name of the applicable spatial unit | 
**user_permissions** | **List[str]** | List of permissions that are effective on this dataset for the current user | [optional] 

## Example

```python
from openapi_client.models.indicator_spatial_unit_join_item import IndicatorSpatialUnitJoinItem

# TODO update the JSON string below
json = "{}"
# create an instance of IndicatorSpatialUnitJoinItem from a JSON string
indicator_spatial_unit_join_item_instance = IndicatorSpatialUnitJoinItem.from_json(json)
# print the JSON string representation of the object
print IndicatorSpatialUnitJoinItem.to_json()

# convert the object into a dict
indicator_spatial_unit_join_item_dict = indicator_spatial_unit_join_item_instance.to_dict()
# create an instance of IndicatorSpatialUnitJoinItem from a dict
indicator_spatial_unit_join_item_form_dict = indicator_spatial_unit_join_item.from_dict(indicator_spatial_unit_join_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


