# PeriodOfValidityType

definition of the period of validity of a certain dataset

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**end_date** | **date** | an optional timestamp representing the ending date according to ISO 8601 (e.g. 2018-01-30). The parameter can be omitted, if the end date is unknown. | [optional] 
**start_date** | **date** | a timestamp representing the starting date according to ISO 8601 (e.g. 2018-01-30) | 

## Example

```python
from openapi_client.models.period_of_validity_type import PeriodOfValidityType

# TODO update the JSON string below
json = "{}"
# create an instance of PeriodOfValidityType from a JSON string
period_of_validity_type_instance = PeriodOfValidityType.from_json(json)
# print the JSON string representation of the object
print PeriodOfValidityType.to_json()

# convert the object into a dict
period_of_validity_type_dict = period_of_validity_type_instance.to_dict()
# create an instance of PeriodOfValidityType from a dict
period_of_validity_type_form_dict = period_of_validity_type.from_dict(period_of_validity_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


