# RoleOverviewType


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**role_id** | **str** | the unique role identifier | 
**role_name** | **str** | the role name | 

## Example

```python
from openapi_client.models.role_overview_type import RoleOverviewType

# TODO update the JSON string below
json = "{}"
# create an instance of RoleOverviewType from a JSON string
role_overview_type_instance = RoleOverviewType.from_json(json)
# print the JSON string representation of the object
print RoleOverviewType.to_json()

# convert the object into a dict
role_overview_type_dict = role_overview_type_instance.to_dict()
# create an instance of RoleOverviewType from a dict
role_overview_type_form_dict = role_overview_type.from_dict(role_overview_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


