# CommonMetadataType


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**contact** | **str** | contact details where additional information can be achieved | 
**databasis** | **str** | information about data used as a basis to generate the dataset | [optional] 
**datasource** | **str** | information about the origin/source of the dataset | 
**description** | **str** | description of the dataset | 
**last_update** | **date** | a timestamp representing the lastUpdate according to ISO 8601 (e.g. 2018-01-30) | [optional] 
**literature** | **str** | an optional hint to literature about the dataset (e.g. URL or book/article name) | [optional] 
**note** | **str** | an optional note with background information about the dataset | [optional] 
**srid_epsg** | **float** | the coordinate reference system of the dataset as EPSG code | 
**update_interval** | **str** |  | 

## Example

```python
from openapi_client.models.common_metadata_type import CommonMetadataType

# TODO update the JSON string below
json = "{}"
# create an instance of CommonMetadataType from a JSON string
common_metadata_type_instance = CommonMetadataType.from_json(json)
# print the JSON string representation of the object
print CommonMetadataType.to_json()

# convert the object into a dict
common_metadata_type_dict = common_metadata_type_instance.to_dict()
# create an instance of CommonMetadataType from a dict
common_metadata_type_form_dict = common_metadata_type.from_dict(common_metadata_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


