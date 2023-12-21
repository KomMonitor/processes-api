# TopicInputType


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sub_topics** | [**List[TopicInputType]**](TopicInputType.md) | optional list of subTopics | [optional] 
**topic_description** | **str** | short description of the topic | 
**topic_id** | **str** | the topic identifier | [optional] 
**topic_name** | **str** | the topic name | 
**topic_resource** | **str** | topic resource indicating if the topic object corresponds to an indicator or to a georesource | [optional] 
**topic_type** | **str** | topic type indicating if the topic object is a subtopic or a main topic - only topics of type &#39;sub&#39; shall be subTopics of topics with type &#39;main&#39; | 

## Example

```python
from openapi_client.models.topic_input_type import TopicInputType

# TODO update the JSON string below
json = "{}"
# create an instance of TopicInputType from a JSON string
topic_input_type_instance = TopicInputType.from_json(json)
# print the JSON string representation of the object
print TopicInputType.to_json()

# convert the object into a dict
topic_input_type_dict = topic_input_type_instance.to_dict()
# create an instance of TopicInputType from a dict
topic_input_type_form_dict = topic_input_type.from_dict(topic_input_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


