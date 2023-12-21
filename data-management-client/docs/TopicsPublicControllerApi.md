# openapi_client.TopicsPublicControllerApi

All URIs are relative to *http://localhost:8085*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_topic_by_id**](TopicsPublicControllerApi.md#get_topic_by_id) | **GET** /management/public/topics/{topicId} | retrieve information about the selected topic
[**get_topics**](TopicsPublicControllerApi.md#get_topics) | **GET** /management/public/topics | retrieve information about available topics


# **get_topic_by_id**
> TopicOverviewType get_topic_by_id(topic_id)

retrieve information about the selected topic

retrieve information about the selected topic

### Example

* OAuth Authentication (kommonitor-data-access_oauth):
```python
import time
import os
import openapi_client
from openapi_client.models.topic_overview_type import TopicOverviewType
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
    api_instance = openapi_client.TopicsPublicControllerApi(api_client)
    topic_id = 'topic_id_example' # str | topicId

    try:
        # retrieve information about the selected topic
        api_response = api_instance.get_topic_by_id(topic_id)
        print("The response of TopicsPublicControllerApi->get_topic_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TopicsPublicControllerApi->get_topic_by_id: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **topic_id** | **str**| topicId | 

### Return type

[**TopicOverviewType**](TopicOverviewType.md)

### Authorization

[kommonitor-data-access_oauth](../README.md#kommonitor-data-access_oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | Invalid status value |  -  |
**401** | API key is missing or invalid |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_topics**
> TopicOverviewType get_topics()

retrieve information about available topics

retrieve information about available topics

### Example

* OAuth Authentication (kommonitor-data-access_oauth):
```python
import time
import os
import openapi_client
from openapi_client.models.topic_overview_type import TopicOverviewType
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
    api_instance = openapi_client.TopicsPublicControllerApi(api_client)

    try:
        # retrieve information about available topics
        api_response = api_instance.get_topics()
        print("The response of TopicsPublicControllerApi->get_topics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TopicsPublicControllerApi->get_topics: %s\n" % e)
```



### Parameters
This endpoint does not need any parameter.

### Return type

[**TopicOverviewType**](TopicOverviewType.md)

### Authorization

[kommonitor-data-access_oauth](../README.md#kommonitor-data-access_oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | Invalid status value |  -  |
**401** | API key is missing or invalid |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

