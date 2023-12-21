# openapi_client.TopicsControllerApi

All URIs are relative to *http://localhost:8085*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_topic**](TopicsControllerApi.md#add_topic) | **POST** /management/topics | Register a new topic
[**delete_topic**](TopicsControllerApi.md#delete_topic) | **DELETE** /management/topics/{topicId} | Delete the topic
[**update_topic**](TopicsControllerApi.md#update_topic) | **PUT** /management/topics/{topicId} | Modify topic information


# **add_topic**
> ResponseEntity add_topic(topic_data)

Register a new topic

Add/Register a topic

### Example

* OAuth Authentication (kommonitor-data-access_oauth):
```python
import time
import os
import openapi_client
from openapi_client.models.response_entity import ResponseEntity
from openapi_client.models.topic_input_type import TopicInputType
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8085
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8085"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.TopicsControllerApi(api_client)
    topic_data = openapi_client.TopicInputType() # TopicInputType | topicData

    try:
        # Register a new topic
        api_response = api_instance.add_topic(topic_data)
        print("The response of TopicsControllerApi->add_topic:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TopicsControllerApi->add_topic: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **topic_data** | [**TopicInputType**](TopicInputType.md)| topicData | 

### Return type

[**ResponseEntity**](ResponseEntity.md)

### Authorization

[kommonitor-data-access_oauth](../README.md#kommonitor-data-access_oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**201** | Created |  -  |
**401** | API key is missing or invalid |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**405** | Invalid input |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_topic**
> ResponseEntity delete_topic(topic_id)

Delete the topic

Delete the topic

### Example

* OAuth Authentication (kommonitor-data-access_oauth):
```python
import time
import os
import openapi_client
from openapi_client.models.response_entity import ResponseEntity
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8085
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8085"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.TopicsControllerApi(api_client)
    topic_id = 'topic_id_example' # str | topicId

    try:
        # Delete the topic
        api_response = api_instance.delete_topic(topic_id)
        print("The response of TopicsControllerApi->delete_topic:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TopicsControllerApi->delete_topic: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **topic_id** | **str**| topicId | 

### Return type

[**ResponseEntity**](ResponseEntity.md)

### Authorization

[kommonitor-data-access_oauth](../README.md#kommonitor-data-access_oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**204** | No Content |  -  |
**401** | API key is missing or invalid |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_topic**
> ResponseEntity update_topic(topic_id, topic_data)

Modify topic information

Modify topic information

### Example

* OAuth Authentication (kommonitor-data-access_oauth):
```python
import time
import os
import openapi_client
from openapi_client.models.response_entity import ResponseEntity
from openapi_client.models.topic_input_type import TopicInputType
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8085
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8085"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.TopicsControllerApi(api_client)
    topic_id = 'topic_id_example' # str | topicId
    topic_data = openapi_client.TopicInputType() # TopicInputType | topicData

    try:
        # Modify topic information
        api_response = api_instance.update_topic(topic_id, topic_data)
        print("The response of TopicsControllerApi->update_topic:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TopicsControllerApi->update_topic: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **topic_id** | **str**| topicId | 
 **topic_data** | [**TopicInputType**](TopicInputType.md)| topicData | 

### Return type

[**ResponseEntity**](ResponseEntity.md)

### Authorization

[kommonitor-data-access_oauth](../README.md#kommonitor-data-access_oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**201** | Created |  -  |
**401** | API key is missing or invalid |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**405** | Invalid input |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

