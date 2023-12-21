# openapi_client.GeorecourcesPublicControllerApi

All URIs are relative to *http://localhost:8085*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_all_public_georesource_features_by_id**](GeorecourcesPublicControllerApi.md#get_all_public_georesource_features_by_id) | **GET** /management/public/georesources/{georesourceId}/allFeatures | retrieve all feature entries for all applicable periods of validity for the selected public geo-resource dataset (hence might contain each feature multiple times if they exist for different periods of validity)
[**get_public_georesource_by_id**](GeorecourcesPublicControllerApi.md#get_public_georesource_by_id) | **GET** /management/public/georesources/{georesourceId} | retrieve information about available features of the selected public geo-resource dataset
[**get_public_georesource_by_id_and_year_and_month**](GeorecourcesPublicControllerApi.md#get_public_georesource_by_id_and_year_and_month) | **GET** /management/public/georesources/{georesourceId}/{year}/{month}/{day} | retrieve the features according to the selected public geo-resource dataset and selected year and month as GeoJSON
[**get_public_georesource_schema_by_level**](GeorecourcesPublicControllerApi.md#get_public_georesource_schema_by_level) | **GET** /management/public/georesources/{georesourceId}/schema | retrieve the JSON schema for the selected public geo-resource dataset
[**get_public_georesources**](GeorecourcesPublicControllerApi.md#get_public_georesources) | **GET** /management/public/georesources | retrieve information about available features of different public geo-resource datasets


# **get_all_public_georesource_features_by_id**
> str get_all_public_georesource_features_by_id(georesource_id, simplify_geometries=simplify_geometries)

retrieve all feature entries for all applicable periods of validity for the selected public geo-resource dataset (hence might contain each feature multiple times if they exist for different periods of validity)

retrieve all feature entries for all applicable periods of validity for the selected public geo-resource dataset (hence might contain each feature multiple times if they exist for different periods of validity)

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
    api_instance = openapi_client.GeorecourcesPublicControllerApi(api_client)
    georesource_id = 'georesource_id_example' # str | georesourceId
    simplify_geometries = 'original' # str | simplifyGeometries (optional) (default to 'original')

    try:
        # retrieve all feature entries for all applicable periods of validity for the selected public geo-resource dataset (hence might contain each feature multiple times if they exist for different periods of validity)
        api_response = api_instance.get_all_public_georesource_features_by_id(georesource_id, simplify_geometries=simplify_geometries)
        print("The response of GeorecourcesPublicControllerApi->get_all_public_georesource_features_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GeorecourcesPublicControllerApi->get_all_public_georesource_features_by_id: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **georesource_id** | **str**| georesourceId | 
 **simplify_geometries** | **str**| simplifyGeometries | [optional] [default to &#39;original&#39;]

### Return type

**str**

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

# **get_public_georesource_by_id**
> GeoresourceOverviewType get_public_georesource_by_id(georesource_id)

retrieve information about available features of the selected public geo-resource dataset

retrieve information about available features of the selected public geo-resource dataset

### Example

* OAuth Authentication (kommonitor-data-access_oauth):
```python
import time
import os
import openapi_client
from openapi_client.models.georesource_overview_type import GeoresourceOverviewType
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
    api_instance = openapi_client.GeorecourcesPublicControllerApi(api_client)
    georesource_id = 'georesource_id_example' # str | georesourceId

    try:
        # retrieve information about available features of the selected public geo-resource dataset
        api_response = api_instance.get_public_georesource_by_id(georesource_id)
        print("The response of GeorecourcesPublicControllerApi->get_public_georesource_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GeorecourcesPublicControllerApi->get_public_georesource_by_id: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **georesource_id** | **str**| georesourceId | 

### Return type

[**GeoresourceOverviewType**](GeoresourceOverviewType.md)

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

# **get_public_georesource_by_id_and_year_and_month**
> bytearray get_public_georesource_by_id_and_year_and_month(day, georesource_id, month, year, simplify_geometries=simplify_geometries)

retrieve the features according to the selected public geo-resource dataset and selected year and month as GeoJSON

retrieve the features according to the selected public geo-resource dataset and selected year and month as GeoJSON

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
    api_instance = openapi_client.GeorecourcesPublicControllerApi(api_client)
    day = 1.0 # float | day (default to 1.0)
    georesource_id = 'georesource_id_example' # str | georesourceId
    month = 1.0 # float | month (default to 1.0)
    year = 2023.0 # float | year (default to 2023.0)
    simplify_geometries = 'original' # str | simplifyGeometries (optional) (default to 'original')

    try:
        # retrieve the features according to the selected public geo-resource dataset and selected year and month as GeoJSON
        api_response = api_instance.get_public_georesource_by_id_and_year_and_month(day, georesource_id, month, year, simplify_geometries=simplify_geometries)
        print("The response of GeorecourcesPublicControllerApi->get_public_georesource_by_id_and_year_and_month:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GeorecourcesPublicControllerApi->get_public_georesource_by_id_and_year_and_month: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **day** | **float**| day | [default to 1.0]
 **georesource_id** | **str**| georesourceId | 
 **month** | **float**| month | [default to 1.0]
 **year** | **float**| year | [default to 2023.0]
 **simplify_geometries** | **str**| simplifyGeometries | [optional] [default to &#39;original&#39;]

### Return type

**bytearray**

### Authorization

[kommonitor-data-access_oauth](../README.md#kommonitor-data-access_oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/octed-stream

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | Invalid status value |  -  |
**401** | API key is missing or invalid |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_public_georesource_schema_by_level**
> str get_public_georesource_schema_by_level(georesource_id)

retrieve the JSON schema for the selected public geo-resource dataset

retrieve the JSON schema for the selected public geo-resource dataset. The JSON schema indicates the property structure of the dataset.

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
    api_instance = openapi_client.GeorecourcesPublicControllerApi(api_client)
    georesource_id = 'georesource_id_example' # str | georesourceId

    try:
        # retrieve the JSON schema for the selected public geo-resource dataset
        api_response = api_instance.get_public_georesource_schema_by_level(georesource_id)
        print("The response of GeorecourcesPublicControllerApi->get_public_georesource_schema_by_level:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GeorecourcesPublicControllerApi->get_public_georesource_schema_by_level: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **georesource_id** | **str**| georesourceId | 

### Return type

**str**

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

# **get_public_georesources**
> GeoresourceOverviewType get_public_georesources()

retrieve information about available features of different public geo-resource datasets

retrieve information about available features of different public geo-resource datasets

### Example

* OAuth Authentication (kommonitor-data-access_oauth):
```python
import time
import os
import openapi_client
from openapi_client.models.georesource_overview_type import GeoresourceOverviewType
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
    api_instance = openapi_client.GeorecourcesPublicControllerApi(api_client)

    try:
        # retrieve information about available features of different public geo-resource datasets
        api_response = api_instance.get_public_georesources()
        print("The response of GeorecourcesPublicControllerApi->get_public_georesources:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GeorecourcesPublicControllerApi->get_public_georesources: %s\n" % e)
```



### Parameters
This endpoint does not need any parameter.

### Return type

[**GeoresourceOverviewType**](GeoresourceOverviewType.md)

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

