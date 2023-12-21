# GeoresourcePATCHInputType


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**allowed_roles** | **List[str]** | list of role identifiers that have read access rights for this dataset | [optional] 
**aoi_color** | **str** | color name or color code (i.e. hex number) for areas of interest | [optional] 
**dataset_name** | **str** | the meaningful name of the dataset | [optional] 
**is_aoi** | **bool** | boolean value indicating if the dataset contains areas of interest | [optional] 
**is_loi** | **bool** | boolean value indicating if the dataset contains lines of interest | [optional] 
**is_poi** | **bool** | boolean value indicating if the dataset contains points of interest | [optional] 
**loi_color** | **str** | color name or color code (i.e. hex number) for lines of interest | [optional] 
**loi_dash_array_string** | **str** | sring of line stroke dash array for lines of interest (e.g. 20,20; see https://developer.mozilla.org/de/docs/Web/SVG/Attribute/stroke-dasharray) | [optional] 
**loi_width** | **float** | display width for lines of interest (number of pixels in leaflet) | [optional] 
**metadata** | [**CommonMetadataType**](CommonMetadataType.md) |  | 
**poi_marker_color** | **str** | If georesource is a POI then custom POI marker color can be set by specifying one of the following color names | [optional] 
**poi_symbol_bootstrap3_name** | **str** | If georesource is a POI then custom POI marker symbol can be set by specifying the name of a Bootstrap 3 glyphicon symbol (i.e. \&quot;home\&quot; for a home symbol or \&quot;education\&quot; for a students hat symbol) | [optional] 
**poi_symbol_color** | **str** | If georesource is a POI then custom POI symbol color can be set by specifying one of the following color names | [optional] 
**topic_reference** | **str** | id of the last topic hierarchy entity  | [optional] 

## Example

```python
from openapi_client.models.georesource_patch_input_type import GeoresourcePATCHInputType

# TODO update the JSON string below
json = "{}"
# create an instance of GeoresourcePATCHInputType from a JSON string
georesource_patch_input_type_instance = GeoresourcePATCHInputType.from_json(json)
# print the JSON string representation of the object
print GeoresourcePATCHInputType.to_json()

# convert the object into a dict
georesource_patch_input_type_dict = georesource_patch_input_type_instance.to_dict()
# create an instance of GeoresourcePATCHInputType from a dict
georesource_patch_input_type_form_dict = georesource_patch_input_type.from_dict(georesource_patch_input_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


