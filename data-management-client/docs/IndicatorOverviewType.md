# IndicatorOverviewType


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**abbreviation** | **str** | abbreviated mark of the indicator | 
**allowed_roles** | **List[str]** | list of role identifiers that have read access rights for this dataset | [optional] 
**applicable_dates** | **List[str]** | array of applicable dates (year and month and day as YEAR-MONTH-DAY) according to ISO 8601 (e.g. 2018-01-30) | 
**applicable_spatial_units** | [**List[IndicatorSpatialUnitJoinItem]**](IndicatorSpatialUnitJoinItem.md) | array of spatial unit levels for which the dataset is applicable | 
**characteristic_value** | **str** | the distuingishing characteristic value of the indicator | 
**creation_type** | **str** | indicates if the data is simply inserted (INSERTION), computed by an automated script (COMPUTATION) or automatically aggregated by a script (AGGREGATION) | 
**default_classification_mapping** | [**DefaultClassificationMappingType**](DefaultClassificationMappingType.md) |  | [optional] 
**indicator_id** | **str** | unique identifier of this resource | 
**indicator_name** | **str** | name of the indicator | 
**indicator_type** | **str** | indicates whether the indicator is a status indicator (values represent the extent of the watched phenomenon for a certain point in time) or a dynamic indicator (values represent the change of extent of the watched phenomenon within a certain period of time) | [optional] 
**interpretation** | **str** | interpretation of the indicator values | 
**is_headline_indicator** | **bool** | boolean value indicating if the indicator is a headline indicator | 
**lowest_spatial_unit_for_computation** | **str** | identifier/name of the lowest spatial unit for which the indicator can be computed and thus is available (only necessary for computable indicators) | [optional] 
**metadata** | [**CommonMetadataType**](CommonMetadataType.md) |  | 
**ogc_services** | [**List[OgcServicesType]**](OgcServicesType.md) | list of available OGC services for that indicator for different spatial units | 
**process_description** | **str** | description about how the indicator was computed | 
**reference_date_note** | **str** | an optional note on the reference date of the indicator | [optional] 
**display_order** | **float** | an order number to control display order in clients | [optional] 
**referenced_georesources** | [**List[GeoresourceReferenceType]**](GeoresourceReferenceType.md) | list of references to georesources | [optional] 
**referenced_indicators** | [**List[IndicatorReferenceType]**](IndicatorReferenceType.md) | list of references to other indicators | [optional] 
**tags** | **List[str]** | list of tag labels for the indicator | 
**topic_reference** | **str** | id of the last topic hierarchy entity  | 
**unit** | **str** | unit of the indicator values | 
**user_permissions** | **List[str]** | List of permissions that are effective on this dataset for the current user | [optional] 

## Example

```python
from openapi_client.models.indicator_overview_type import IndicatorOverviewType

# TODO update the JSON string below
json = "{}"
# create an instance of IndicatorOverviewType from a JSON string
indicator_overview_type_instance = IndicatorOverviewType.from_json(json)
# print the JSON string representation of the object
print IndicatorOverviewType.to_json()

# convert the object into a dict
indicator_overview_type_dict = indicator_overview_type_instance.to_dict()
# create an instance of IndicatorOverviewType from a dict
indicator_overview_type_form_dict = indicator_overview_type.from_dict(indicator_overview_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


