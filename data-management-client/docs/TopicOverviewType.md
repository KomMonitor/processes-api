# TopicOverviewType


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sub_topics** | [**List[TopicOverviewType]**](TopicOverviewType.md) | optional list of subTopics | [optional] 
**topic_description** | **str** | short description of the topic | 
**topic_id** | **str** | the identifier of the topic | 
**topic_name** | **str** | the topic name | 
**topic_resource** | **str** | topic resource indicating if the topic object corresponds to an indicator or to a georesource | [optional] 
**topic_type** | **str** | topic type indicating if the topic object is a subtopic or a main topic - only topics of type &#39;sub&#39; shall be subTopics of topics with type &#39;main&#39; | 

## Example

```python
from openapi_client.models.topic_overview_type import TopicOverviewType

# TODO update the JSON string below
json = "{}"
# create an instance of TopicOverviewType from a JSON string
topic_overview_type_instance = TopicOverviewType.from_json(json)
# print the JSON string representation of the object
print TopicOverviewType.to_json()

# convert the object into a dict
topic_overview_type_dict = topic_overview_type_instance.to_dict()
# create an instance of TopicOverviewType from a dict
topic_overview_type_form_dict = topic_overview_type.from_dict(topic_overview_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


