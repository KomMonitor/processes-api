# openapi_client.GeorecourcesControllerApi

All URIs are relative to *http://localhost:8085*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_georesource_as_body**](GeorecourcesControllerApi.md#add_georesource_as_body) | **POST** /management/georesources | Add a new geo-resource
[**delete_all_georesource_features_by_id**](GeorecourcesControllerApi.md#delete_all_georesource_features_by_id) | **DELETE** /management/georesources/{georesourceId}/allFeatures | Delete all features/contents of the selected geo-resource dataset
[**delete_georesource_by_id**](GeorecourcesControllerApi.md#delete_georesource_by_id) | **DELETE** /management/georesources/{georesourceId} | Delete the features/contents of the selected geo-resource dataset
[**delete_georesource_by_id_and_year_and_month**](GeorecourcesControllerApi.md#delete_georesource_by_id_and_year_and_month) | **DELETE** /management/georesources/{georesourceId}/{year}/{month}/{day} | Delete the features/contents of the selected geo-resource dataset, selected by year and month
[**get_all_georesource_features_by_id**](GeorecourcesControllerApi.md#get_all_georesource_features_by_id) | **GET** /management/georesources/{georesourceId}/allFeatures | retrieve all feature entries for all applicable periods of validity for the selected geo-resource dataset (hence might contain each feature multiple times if they exist for different periods of validity)
[**get_georesource_by_id**](GeorecourcesControllerApi.md#get_georesource_by_id) | **GET** /management/georesources/{georesourceId} | retrieve information about available features of the selected geo-resource dataset
[**get_georesource_by_id_and_year_and_month**](GeorecourcesControllerApi.md#get_georesource_by_id_and_year_and_month) | **GET** /management/georesources/{georesourceId}/{year}/{month}/{day} | retrieve the features according to the selected geo-resource dataset and selected year and month as GeoJSON
[**get_georesource_schema_by_level**](GeorecourcesControllerApi.md#get_georesource_schema_by_level) | **GET** /management/georesources/{georesourceId}/schema | retrieve the JSON schema for the selected geo-resource dataset
[**get_georesources**](GeorecourcesControllerApi.md#get_georesources) | **GET** /management/georesources | retrieve information about available features of different geo-resource datasets
[**update_georesource_as_body**](GeorecourcesControllerApi.md#update_georesource_as_body) | **PUT** /management/georesources/{georesourceId} | Modify/Update the features of the selected geo-resource dataset
[**update_georesource_metadata_as_body**](GeorecourcesControllerApi.md#update_georesource_metadata_as_body) | **PATCH** /management/georesources/{georesourceId} | Modify/Update the metadata of the selected geo-resource dataset


# **add_georesource_as_body**
> ResponseEntity add_georesource_as_body(feature_data)

Add a new geo-resource

Add/Register a geo-resource dataset for a certain period of time

### Example

* OAuth Authentication (kommonitor-data-access_oauth):
```python
import time
import os
import openapi_client
from openapi_client.models.georesource_post_input_type import GeoresourcePOSTInputType
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
    api_instance = openapi_client.GeorecourcesControllerApi(api_client)
    feature_data = openapi_client.GeoresourcePOSTInputType() # GeoresourcePOSTInputType | featureData

    try:
        # Add a new geo-resource
        api_response = api_instance.add_georesource_as_body(feature_data)
        print("The response of GeorecourcesControllerApi->add_georesource_as_body:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GeorecourcesControllerApi->add_georesource_as_body: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **feature_data** | [**GeoresourcePOSTInputType**](GeoresourcePOSTInputType.md)| featureData | 

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

# **delete_all_georesource_features_by_id**
> ResponseEntity delete_all_georesource_features_by_id(georesource_id)

Delete all features/contents of the selected geo-resource dataset

Delete all features/contents of the selected geo-resource dataset

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
    api_instance = openapi_client.GeorecourcesControllerApi(api_client)
    georesource_id = 'georesource_id_example' # str | georesourceId

    try:
        # Delete all features/contents of the selected geo-resource dataset
        api_response = api_instance.delete_all_georesource_features_by_id(georesource_id)
        print("The response of GeorecourcesControllerApi->delete_all_georesource_features_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GeorecourcesControllerApi->delete_all_georesource_features_by_id: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **georesource_id** | **str**| georesourceId | 

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

# **delete_georesource_by_id**
> ResponseEntity delete_georesource_by_id(georesource_id)

Delete the features/contents of the selected geo-resource dataset

Delete the features/contents of the selected geo-resource dataset

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
    api_instance = openapi_client.GeorecourcesControllerApi(api_client)
    georesource_id = 'georesource_id_example' # str | georesourceId

    try:
        # Delete the features/contents of the selected geo-resource dataset
        api_response = api_instance.delete_georesource_by_id(georesource_id)
        print("The response of GeorecourcesControllerApi->delete_georesource_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GeorecourcesControllerApi->delete_georesource_by_id: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **georesource_id** | **str**| georesourceId | 

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

# **delete_georesource_by_id_and_year_and_month**
> ResponseEntity delete_georesource_by_id_and_year_and_month(day, georesource_id, month, year)

Delete the features/contents of the selected geo-resource dataset, selected by year and month

Delete the features/contents of the selected geo-resource dataset, selected by year and month

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
    api_instance = openapi_client.GeorecourcesControllerApi(api_client)
    day = 1.0 # float | day (default to 1.0)
    georesource_id = 'georesource_id_example' # str | georesourceId
    month = 1.0 # float | month (default to 1.0)
    year = 2023.0 # float | year (default to 2023.0)

    try:
        # Delete the features/contents of the selected geo-resource dataset, selected by year and month
        api_response = api_instance.delete_georesource_by_id_and_year_and_month(day, georesource_id, month, year)
        print("The response of GeorecourcesControllerApi->delete_georesource_by_id_and_year_and_month:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GeorecourcesControllerApi->delete_georesource_by_id_and_year_and_month: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **day** | **float**| day | [default to 1.0]
 **georesource_id** | **str**| georesourceId | 
 **month** | **float**| month | [default to 1.0]
 **year** | **float**| year | [default to 2023.0]

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

# **get_all_georesource_features_by_id**
> str get_all_georesource_features_by_id(georesource_id, name=name, simplify_geometries=simplify_geometries)

retrieve all feature entries for all applicable periods of validity for the selected geo-resource dataset (hence might contain each feature multiple times if they exist for different periods of validity)

retrieve all feature entries for all applicable periods of validity for the selected geo-resource dataset (hence might contain each feature multiple times if they exist for different periods of validity)

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
    api_instance = openapi_client.GeorecourcesControllerApi(api_client)
    georesource_id = 'georesource_id_example' # str | georesourceId
    name = 'name_example' # str |  (optional)
    simplify_geometries = 'original' # str | simplifyGeometries (optional) (default to 'original')

    try:
        # retrieve all feature entries for all applicable periods of validity for the selected geo-resource dataset (hence might contain each feature multiple times if they exist for different periods of validity)
        api_response = api_instance.get_all_georesource_features_by_id(georesource_id, name=name, simplify_geometries=simplify_geometries)
        print("The response of GeorecourcesControllerApi->get_all_georesource_features_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GeorecourcesControllerApi->get_all_georesource_features_by_id: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **georesource_id** | **str**| georesourceId | 
 **name** | **str**|  | [optional] 
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

# **get_georesource_by_id**
> GeoresourceOverviewType get_georesource_by_id(georesource_id, name=name)

retrieve information about available features of the selected geo-resource dataset

retrieve information about available features of the selected geo-resource dataset

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
    api_instance = openapi_client.GeorecourcesControllerApi(api_client)
    georesource_id = 'georesource_id_example' # str | georesourceId
    name = 'name_example' # str |  (optional)

    try:
        # retrieve information about available features of the selected geo-resource dataset
        api_response = api_instance.get_georesource_by_id(georesource_id, name=name)
        print("The response of GeorecourcesControllerApi->get_georesource_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GeorecourcesControllerApi->get_georesource_by_id: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **georesource_id** | **str**| georesourceId | 
 **name** | **str**|  | [optional] 

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

# **get_georesource_by_id_and_year_and_month**
> bytearray get_georesource_by_id_and_year_and_month(day, georesource_id, month, year, name=name, simplify_geometries=simplify_geometries)

retrieve the features according to the selected geo-resource dataset and selected year and month as GeoJSON

retrieve the features according to the selected geo-resource dataset and selected year and month as GeoJSON

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
    api_instance = openapi_client.GeorecourcesControllerApi(api_client)
    day = 1.0 # float | day (default to 1.0)
    georesource_id = 'georesource_id_example' # str | georesourceId
    month = 1.0 # float | month (default to 1.0)
    year = 2023.0 # float | year (default to 2023.0)
    name = 'name_example' # str |  (optional)
    simplify_geometries = 'original' # str | simplifyGeometries (optional) (default to 'original')

    try:
        # retrieve the features according to the selected geo-resource dataset and selected year and month as GeoJSON
        api_response = api_instance.get_georesource_by_id_and_year_and_month(day, georesource_id, month, year, name=name, simplify_geometries=simplify_geometries)
        print("The response of GeorecourcesControllerApi->get_georesource_by_id_and_year_and_month:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GeorecourcesControllerApi->get_georesource_by_id_and_year_and_month: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **day** | **float**| day | [default to 1.0]
 **georesource_id** | **str**| georesourceId | 
 **month** | **float**| month | [default to 1.0]
 **year** | **float**| year | [default to 2023.0]
 **name** | **str**|  | [optional] 
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

# **get_georesource_schema_by_level**
> str get_georesource_schema_by_level(georesource_id, name=name)

retrieve the JSON schema for the selected geo-resource dataset

retrieve the JSON schema for the selected geo-resource dataset. The JSON schema indicates the property structure of the dataset.

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
    api_instance = openapi_client.GeorecourcesControllerApi(api_client)
    georesource_id = 'georesource_id_example' # str | georesourceId
    name = 'name_example' # str |  (optional)

    try:
        # retrieve the JSON schema for the selected geo-resource dataset
        api_response = api_instance.get_georesource_schema_by_level(georesource_id, name=name)
        print("The response of GeorecourcesControllerApi->get_georesource_schema_by_level:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GeorecourcesControllerApi->get_georesource_schema_by_level: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **georesource_id** | **str**| georesourceId | 
 **name** | **str**|  | [optional] 

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

# **get_georesources**
> List[GeoresourceOverviewType] get_georesources(name=name)

retrieve information about available features of different geo-resource datasets

retrieve information about available features of different geo-resource datasets

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
    api_instance = openapi_client.GeorecourcesControllerApi(api_client)
    name = 'name_example' # str |  (optional)

    try:
        # retrieve information about available features of different geo-resource datasets
        api_response = api_instance.get_georesources(name=name)
        print("The response of GeorecourcesControllerApi->get_georesources:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GeorecourcesControllerApi->get_georesources: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | [optional] 

### Return type

[**List[GeoresourceOverviewType]**](GeoresourceOverviewType.md)

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

# **update_georesource_as_body**
> ResponseEntity update_georesource_as_body(georesource_id, feature_data)

Modify/Update the features of the selected geo-resource dataset

Modify/Update the features of the selected geo-resource dataset.  The interface expects a full upload of all geometries for the spatial unit. Internally, those geometries are compared to the existing ones to mark 'old' geometries that are no longer in use as outdated. Hence, each geometric object is only persisted once and its use is controlled by time validity marks.

### Example

* OAuth Authentication (kommonitor-data-access_oauth):
```python
import time
import os
import openapi_client
from openapi_client.models.georesource_put_input_type import GeoresourcePUTInputType
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
    api_instance = openapi_client.GeorecourcesControllerApi(api_client)
    georesource_id = 'georesource_id_example' # str | georesourceId
    feature_data = openapi_client.GeoresourcePUTInputType() # GeoresourcePUTInputType | featureData

    try:
        # Modify/Update the features of the selected geo-resource dataset
        api_response = api_instance.update_georesource_as_body(georesource_id, feature_data)
        print("The response of GeorecourcesControllerApi->update_georesource_as_body:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GeorecourcesControllerApi->update_georesource_as_body: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **georesource_id** | **str**| georesourceId | 
 **feature_data** | [**GeoresourcePUTInputType**](GeoresourcePUTInputType.md)| featureData | 

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

# **update_georesource_metadata_as_body**
> ResponseEntity update_georesource_metadata_as_body(georesource_id, metadata)

Modify/Update the metadata of the selected geo-resource dataset

Modify/Update the metadata of the selected geo-resource dataset. This replaces the formerly stored metadata.

### Example

* OAuth Authentication (kommonitor-data-access_oauth):
```python
import time
import os
import openapi_client
from openapi_client.models.georesource_patch_input_type import GeoresourcePATCHInputType
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
    api_instance = openapi_client.GeorecourcesControllerApi(api_client)
    georesource_id = 'georesource_id_example' # str | georesourceId
    metadata = openapi_client.GeoresourcePATCHInputType() # GeoresourcePATCHInputType | metadata

    try:
        # Modify/Update the metadata of the selected geo-resource dataset
        api_response = api_instance.update_georesource_metadata_as_body(georesource_id, metadata)
        print("The response of GeorecourcesControllerApi->update_georesource_metadata_as_body:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GeorecourcesControllerApi->update_georesource_metadata_as_body: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **georesource_id** | **str**| georesourceId | 
 **metadata** | [**GeoresourcePATCHInputType**](GeoresourcePATCHInputType.md)| metadata | 

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
**204** | No Content |  -  |
**401** | API key is missing or invalid |  -  |
**403** | Forbidden |  -  |
**405** | Invalid input |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

