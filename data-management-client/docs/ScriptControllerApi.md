# openapi_client.ScriptControllerApi

All URIs are relative to *http://localhost:8085*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_process_script_as_body**](ScriptControllerApi.md#add_process_script_as_body) | **POST** /management/process-scripts | Register a new process script
[**delete_process_script**](ScriptControllerApi.md#delete_process_script) | **DELETE** /management/process-scripts/usingIndicatorId/{indicatorId} | Delete the process script
[**delete_process_script_by_script_id**](ScriptControllerApi.md#delete_process_script_by_script_id) | **DELETE** /management/process-scripts/{scriptId} | Delete the process script
[**get_process_script_code**](ScriptControllerApi.md#get_process_script_code) | **GET** /management/process-scripts/{scriptId}/scriptCode | retrieve the process script code associated to a certain indicator as JavaScript file
[**get_process_script_code_for_indicator**](ScriptControllerApi.md#get_process_script_code_for_indicator) | **GET** /management/process-scripts/usingIndicatorId/{indicatorId}/scriptCode | retrieve the process script code associated to a certain indicator as JavaScript file
[**get_process_script_for_indicator**](ScriptControllerApi.md#get_process_script_for_indicator) | **GET** /management/process-scripts/usingIndicatorId/{indicatorId} | retrieve information about the associated process script for a certain indicator
[**get_process_script_for_script_id**](ScriptControllerApi.md#get_process_script_for_script_id) | **GET** /management/process-scripts/{scriptId} | retrieve information about the associated process script for a certain scriptId
[**get_process_script_template**](ScriptControllerApi.md#get_process_script_template) | **GET** /management/process-scripts/template | retrieve an empty script template, that defines how to implement process scripts for KomMonitor as JavaScript file.
[**get_process_scripts**](ScriptControllerApi.md#get_process_scripts) | **GET** /management/process-scripts | retrieve information about available process scripts
[**update_process_script_as_body**](ScriptControllerApi.md#update_process_script_as_body) | **PUT** /management/process-scripts/usingIndicatorId/{indicatorId} | Modify/Update an existing process script
[**update_process_script_as_body_by_script_id**](ScriptControllerApi.md#update_process_script_as_body_by_script_id) | **PUT** /management/process-scripts/{scriptId} | Modify/Update an existing process script


# **add_process_script_as_body**
> ResponseEntity add_process_script_as_body(process_script_data)

Register a new process script

Register a process script associated to a certain indicator

### Example

* OAuth Authentication (kommonitor-data-access_oauth):
```python
import time
import os
import openapi_client
from openapi_client.models.process_script_post_input_type import ProcessScriptPOSTInputType
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
    api_instance = openapi_client.ScriptControllerApi(api_client)
    process_script_data = openapi_client.ProcessScriptPOSTInputType() # ProcessScriptPOSTInputType | processScriptData

    try:
        # Register a new process script
        api_response = api_instance.add_process_script_as_body(process_script_data)
        print("The response of ScriptControllerApi->add_process_script_as_body:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScriptControllerApi->add_process_script_as_body: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **process_script_data** | [**ProcessScriptPOSTInputType**](ProcessScriptPOSTInputType.md)| processScriptData | 

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

# **delete_process_script**
> ResponseEntity delete_process_script(indicator_id)

Delete the process script

Delete the process script associated to the specified indicator

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
    api_instance = openapi_client.ScriptControllerApi(api_client)
    indicator_id = 'indicator_id_example' # str | indicatorId

    try:
        # Delete the process script
        api_response = api_instance.delete_process_script(indicator_id)
        print("The response of ScriptControllerApi->delete_process_script:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScriptControllerApi->delete_process_script: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **indicator_id** | **str**| indicatorId | 

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

# **delete_process_script_by_script_id**
> ResponseEntity delete_process_script_by_script_id(script_id)

Delete the process script

Delete the process script associated to the specified scriptId

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
    api_instance = openapi_client.ScriptControllerApi(api_client)
    script_id = 'script_id_example' # str | scriptId

    try:
        # Delete the process script
        api_response = api_instance.delete_process_script_by_script_id(script_id)
        print("The response of ScriptControllerApi->delete_process_script_by_script_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScriptControllerApi->delete_process_script_by_script_id: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **script_id** | **str**| scriptId | 

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

# **get_process_script_code**
> bytearray get_process_script_code(script_id, name=name)

retrieve the process script code associated to a certain indicator as JavaScript file

retrieve the process script code associated to a certain indicator as JavaScript file

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
    api_instance = openapi_client.ScriptControllerApi(api_client)
    script_id = 'script_id_example' # str | scriptId
    name = 'name_example' # str |  (optional)

    try:
        # retrieve the process script code associated to a certain indicator as JavaScript file
        api_response = api_instance.get_process_script_code(script_id, name=name)
        print("The response of ScriptControllerApi->get_process_script_code:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScriptControllerApi->get_process_script_code: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **script_id** | **str**| scriptId | 
 **name** | **str**|  | [optional] 

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

# **get_process_script_code_for_indicator**
> bytearray get_process_script_code_for_indicator(indicator_id, name=name)

retrieve the process script code associated to a certain indicator as JavaScript file

retrieve the process script code associated to a certain indicator as JavaScript file

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
    api_instance = openapi_client.ScriptControllerApi(api_client)
    indicator_id = 'indicator_id_example' # str | indicatorId
    name = 'name_example' # str |  (optional)

    try:
        # retrieve the process script code associated to a certain indicator as JavaScript file
        api_response = api_instance.get_process_script_code_for_indicator(indicator_id, name=name)
        print("The response of ScriptControllerApi->get_process_script_code_for_indicator:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScriptControllerApi->get_process_script_code_for_indicator: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **indicator_id** | **str**| indicatorId | 
 **name** | **str**|  | [optional] 

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

# **get_process_script_for_indicator**
> ProcessScriptOverviewType get_process_script_for_indicator(indicator_id, name=name)

retrieve information about the associated process script for a certain indicator

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
    api_instance = openapi_client.ScriptControllerApi(api_client)
    indicator_id = 'indicator_id_example' # str | indicatorId
    name = 'name_example' # str |  (optional)

    try:
        # retrieve information about the associated process script for a certain indicator
        api_response = api_instance.get_process_script_for_indicator(indicator_id, name=name)
        print("The response of ScriptControllerApi->get_process_script_for_indicator:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScriptControllerApi->get_process_script_for_indicator: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **indicator_id** | **str**| indicatorId | 
 **name** | **str**|  | [optional] 

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

# **get_process_script_for_script_id**
> ProcessScriptOverviewType get_process_script_for_script_id(script_id, name=name)

retrieve information about the associated process script for a certain scriptId

retrieve information about the associated process script for a certain scriptId

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
    api_instance = openapi_client.ScriptControllerApi(api_client)
    script_id = 'script_id_example' # str | scriptId
    name = 'name_example' # str |  (optional)

    try:
        # retrieve information about the associated process script for a certain scriptId
        api_response = api_instance.get_process_script_for_script_id(script_id, name=name)
        print("The response of ScriptControllerApi->get_process_script_for_script_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScriptControllerApi->get_process_script_for_script_id: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **script_id** | **str**| scriptId | 
 **name** | **str**|  | [optional] 

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

# **get_process_script_template**
> bytearray get_process_script_template()

retrieve an empty script template, that defines how to implement process scripts for KomMonitor as JavaScript file.

retrieve an empty script template, that defines how to implement process scripts for KomMonitor. The script works as a template for a NodeJS module. Hence, it predefines required methods that are called by the executing processing engine (a NodeJS runtimne environment). As a script developer, those predefined methods have to be implemented. The template contains detailed documentation on how to implement those methods.

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
    api_instance = openapi_client.ScriptControllerApi(api_client)

    try:
        # retrieve an empty script template, that defines how to implement process scripts for KomMonitor as JavaScript file.
        api_response = api_instance.get_process_script_template()
        print("The response of ScriptControllerApi->get_process_script_template:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScriptControllerApi->get_process_script_template: %s\n" % e)
```



### Parameters
This endpoint does not need any parameter.

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

# **get_process_scripts**
> ProcessScriptOverviewType get_process_scripts(name=name)

retrieve information about available process scripts

retrieve information about available process scripts

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
    api_instance = openapi_client.ScriptControllerApi(api_client)
    name = 'name_example' # str |  (optional)

    try:
        # retrieve information about available process scripts
        api_response = api_instance.get_process_scripts(name=name)
        print("The response of ScriptControllerApi->get_process_scripts:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScriptControllerApi->get_process_scripts: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | [optional] 

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

# **update_process_script_as_body**
> ResponseEntity update_process_script_as_body(indicator_id, process_script_data)

Modify/Update an existing process script

Modify/Update an existing process script associated to a certain indicator

### Example

* OAuth Authentication (kommonitor-data-access_oauth):
```python
import time
import os
import openapi_client
from openapi_client.models.process_script_put_input_type import ProcessScriptPUTInputType
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
    api_instance = openapi_client.ScriptControllerApi(api_client)
    indicator_id = 'indicator_id_example' # str | indicatorId
    process_script_data = openapi_client.ProcessScriptPUTInputType() # ProcessScriptPUTInputType | processScriptData

    try:
        # Modify/Update an existing process script
        api_response = api_instance.update_process_script_as_body(indicator_id, process_script_data)
        print("The response of ScriptControllerApi->update_process_script_as_body:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScriptControllerApi->update_process_script_as_body: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **indicator_id** | **str**| indicatorId | 
 **process_script_data** | [**ProcessScriptPUTInputType**](ProcessScriptPUTInputType.md)| processScriptData | 

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

# **update_process_script_as_body_by_script_id**
> ResponseEntity update_process_script_as_body_by_script_id(script_id, process_script_data)

Modify/Update an existing process script

Modify/Update an existing process script associated to a certain scriptId

### Example

* OAuth Authentication (kommonitor-data-access_oauth):
```python
import time
import os
import openapi_client
from openapi_client.models.process_script_put_input_type import ProcessScriptPUTInputType
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
    api_instance = openapi_client.ScriptControllerApi(api_client)
    script_id = 'script_id_example' # str | scriptId
    process_script_data = openapi_client.ProcessScriptPUTInputType() # ProcessScriptPUTInputType | processScriptData

    try:
        # Modify/Update an existing process script
        api_response = api_instance.update_process_script_as_body_by_script_id(script_id, process_script_data)
        print("The response of ScriptControllerApi->update_process_script_as_body_by_script_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScriptControllerApi->update_process_script_as_body_by_script_id: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **script_id** | **str**| scriptId | 
 **process_script_data** | [**ProcessScriptPUTInputType**](ProcessScriptPUTInputType.md)| processScriptData | 

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

