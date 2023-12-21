# OgcServicesType


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**default_style_name** | **str** | the name of the default style (SLD) that is published and applied to the associated dataset | 
**spatial_unit** | **str** | the name of the spatial unit | 
**wfs_url** | **str** | the URL of a running WFS instance serving the spatial features of the associated dataset | 
**wms_url** | **str** | the URL of a running WMS instance serving the spatial features of the associated dataset | 

## Example

```python
from openapi_client.models.ogc_services_type import OgcServicesType

# TODO update the JSON string below
json = "{}"
# create an instance of OgcServicesType from a JSON string
ogc_services_type_instance = OgcServicesType.from_json(json)
# print the JSON string representation of the object
print OgcServicesType.to_json()

# convert the object into a dict
ogc_services_type_dict = ogc_services_type_instance.to_dict()
# create an instance of OgcServicesType from a dict
ogc_services_type_form_dict = ogc_services_type.from_dict(ogc_services_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


