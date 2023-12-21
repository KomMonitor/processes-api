# openapi_client.ScriptPublicControllerApi

All URIs are relative to *http://localhost:8085*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_process_script_code1**](ScriptPublicControllerApi.md#get_process_script_code1) | **GET** /management/public/process-scripts/{scriptId}/scriptCode | retrieve the process script code associated to a certain public indicator as JavaScript file
[**get_process_script_code_for_indicator1**](ScriptPublicControllerApi.md#get_process_script_code_for_indicator1) | **GET** /management/public/process-scripts/usingIndicatorId/{indicatorId}/scriptCode | retrieve the process script code associated to a certain public indicator as JavaScript file
[**get_process_script_for_indicator1**](ScriptPublicControllerApi.md#get_process_script_for_indicator1) | **GET** /management/public/process-scripts/usingIndicatorId/{indicatorId} | retrieve information about the associated process script for a certain public indicator
[**get_process_script_for_script_id1**](ScriptPublicControllerApi.md#get_process_script_for_script_id1) | **GET** /management/public/process-scripts/{scriptId} | retrieve information about the associated process script for a certain scriptId associated to a public indicator
[**get_process_scripts1**](ScriptPublicControllerApi.md#get_process_scripts1) | **GET** /management/public/process-scripts | retrieve information about available process scripts associated to public indicators


# **get_process_script_code1**
> bytearray get_process_script_code1(script_id)

retrieve the process script code associated to a certain public indicator as JavaScript file

retrieve the process script code associated to a certain public indicator as JavaScript file

### Example

* OAuth Authentication (kommonitor-data-access_oauth):
```python
import time
import os
import openapi_client
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
    api_instance = openapi_client.ScriptPublicControllerApi(api_client)
    script_id = 'script_id_example' # str | scriptId

    try:
        # retrieve the process script code associated to a certain public indicator as JavaScript file
        api_response = api_instance.get_process_script_code1(script_id)
        print("The response of ScriptPublicControllerApi->get_process_script_code1:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScriptPublicControllerApi->get_process_script_code1: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **script_id** | **str**| scriptId | 

### Return type

**bytearray**

### Authorization

[kommonitor-data-access_oauth](../README.md#kommonitor-data-access_oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/javascript

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | Invalid status value |  -  |
**401** | API key is missing or invalid |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_process_script_code_for_indicator1**
> bytearray get_process_script_code_for_indicator1(indicator_id)

retrieve the process script code associated to a certain public indicator as JavaScript file

retrieve the process script code associated to a certain public indicator as JavaScript file

### Example

* OAuth Authentication (kommonitor-data-access_oauth):
```python
import time
import os
import openapi_client
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
    api_instance = openapi_client.ScriptPublicControllerApi(api_client)
    indicator_id = 'indicator_id_example' # str | indicatorId

    try:
        # retrieve the process script code associated to a certain public indicator as JavaScript file
        api_response = api_instance.get_process_script_code_for_indicator1(indicator_id)
        print("The response of ScriptPublicControllerApi->get_process_script_code_for_indicator1:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScriptPublicControllerApi->get_process_script_code_for_indicator1: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **indicator_id** | **str**| indicatorId | 

### Return type

**bytearray**

### Authorization

[kommonitor-data-access_oauth](../README.md#kommonitor-data-access_oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/javascript

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | Invalid status value |  -  |
**401** | API key is missing or invalid |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_process_script_for_indicator1**
> ProcessScriptOverviewType get_process_script_for_indicator1(indicator_id)

retrieve information about the associated process script for a certain public indicator

retrieve information about the associated process script for a certain indicator

### Example

* OAuth Authentication (kommonitor-data-access_oauth):
```python
import time
import os
import openapi_client
from openapi_client.models.process_script_overview_type import ProcessScriptOverviewType
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
    api_instance = openapi_client.ScriptPublicControllerApi(api_client)
    indicator_id = 'indicator_id_example' # str | indicatorId

    try:
        # retrieve information about the associated process script for a certain public indicator
        api_response = api_instance.get_process_script_for_indicator1(indicator_id)
        print("The response of ScriptPublicControllerApi->get_process_script_for_indicator1:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScriptPublicControllerApi->get_process_script_for_indicator1: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **indicator_id** | **str**| indicatorId | 

### Return type

[**ProcessScriptOverviewType**](ProcessScriptOverviewType.md)

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

# **get_process_script_for_script_id1**
> ProcessScriptOverviewType get_process_script_for_script_id1(script_id)

retrieve information about the associated process script for a certain scriptId associated to a public indicator

retrieve information about the associated process script for a certain scriptId associated to a public indicator

### Example

* OAuth Authentication (kommonitor-data-access_oauth):
```python
import time
import os
import openapi_client
from openapi_client.models.process_script_overview_type import ProcessScriptOverviewType
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
    api_instance = openapi_client.ScriptPublicControllerApi(api_client)
    script_id = 'script_id_example' # str | scriptId

    try:
        # retrieve information about the associated process script for a certain scriptId associated to a public indicator
        api_response = api_instance.get_process_script_for_script_id1(script_id)
        print("The response of ScriptPublicControllerApi->get_process_script_for_script_id1:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScriptPublicControllerApi->get_process_script_for_script_id1: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **script_id** | **str**| scriptId | 

### Return type

[**ProcessScriptOverviewType**](ProcessScriptOverviewType.md)

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

# **get_process_scripts1**
> ProcessScriptOverviewType get_process_scripts1()

retrieve information about available process scripts associated to public indicators

retrieve information about available process scripts associated to public indicators

### Example

* OAuth Authentication (kommonitor-data-access_oauth):
```python
import time
import os
import openapi_client
from openapi_client.models.process_script_overview_type import ProcessScriptOverviewType
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
    api_instance = openapi_client.ScriptPublicControllerApi(api_client)

    try:
        # retrieve information about available process scripts associated to public indicators
        api_response = api_instance.get_process_scripts1()
        print("The response of ScriptPublicControllerApi->get_process_scripts1:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScriptPublicControllerApi->get_process_scripts1: %s\n" % e)
```



### Parameters
This endpoint does not need any parameter.

### Return type

[**ProcessScriptOverviewType**](ProcessScriptOverviewType.md)

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

