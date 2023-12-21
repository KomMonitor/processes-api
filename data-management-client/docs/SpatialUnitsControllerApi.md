# openapi_client.SpatialUnitsControllerApi

All URIs are relative to *http://localhost:8085*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_spatial_unit_as_body**](SpatialUnitsControllerApi.md#add_spatial_unit_as_body) | **POST** /management/spatial-units | Add a new spatial-unit
[**delete_all_spatial_unit_features_by_id**](SpatialUnitsControllerApi.md#delete_all_spatial_unit_features_by_id) | **DELETE** /management/spatial-units/{spatialUnitId}/allFeatures | Delete all features/contents of the selected spatial-unit dataset
[**delete_spatial_unit_by_id**](SpatialUnitsControllerApi.md#delete_spatial_unit_by_id) | **DELETE** /management/spatial-units/{spatialUnitId} | Delete the features/contents of the selected spatial-unit
[**delete_spatial_unit_by_id_and_year_and_month**](SpatialUnitsControllerApi.md#delete_spatial_unit_by_id_and_year_and_month) | **DELETE** /management/spatial-units/{spatialUnitId}/{year}/{month}/{day} | Delete the features/contents of the selected spatial-unit, year and month
[**get_all_spatial_unit_features_by_id**](SpatialUnitsControllerApi.md#get_all_spatial_unit_features_by_id) | **GET** /management/spatial-units/{spatialUnitId}/allFeatures | retrieve all feature entries for all applicable periods of validity for the selected spatial unit/level (hence might contain each feature multiple times if they exist for different periods of validity)
[**get_spatial_units**](SpatialUnitsControllerApi.md#get_spatial_units) | **GET** /management/spatial-units | retrieve information about available features of different spatial units/levels
[**get_spatial_units_by_id**](SpatialUnitsControllerApi.md#get_spatial_units_by_id) | **GET** /management/spatial-units/{spatialUnitId} | retrieve information about available features of the selected spatial unit/level
[**get_spatial_units_by_id_and_year_and_month**](SpatialUnitsControllerApi.md#get_spatial_units_by_id_and_year_and_month) | **GET** /management/spatial-units/{spatialUnitId}/{year}/{month}/{day} | retrieve the features according to the selected spatial unit/level and selected year and month as GeoJSON
[**get_spatial_units_schema_by_id**](SpatialUnitsControllerApi.md#get_spatial_units_schema_by_id) | **GET** /management/spatial-units/{spatialUnitId}/schema | retrieve the JSON schema for the selected spatial unit/level
[**update_spatial_unit_as_body**](SpatialUnitsControllerApi.md#update_spatial_unit_as_body) | **PUT** /management/spatial-units/{spatialUnitId} | Modify/Update the features of the selected spatial-unit
[**update_spatial_unit_metadata_as_body**](SpatialUnitsControllerApi.md#update_spatial_unit_metadata_as_body) | **PATCH** /management/spatial-units/{spatialUnitId} | Modify/Update the metadata of the selected spatial-unit


# **add_spatial_unit_as_body**
> ResponseEntity add_spatial_unit_as_body(feature_data)

Add a new spatial-unit

Add/Register a spatial unit for a certain period of time

### Example

* OAuth Authentication (kommonitor-data-access_oauth):
```python
import time
import os
import openapi_client
from openapi_client.models.response_entity import ResponseEntity
from openapi_client.models.spatial_unit_post_input_type import SpatialUnitPOSTInputType
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
    api_instance = openapi_client.SpatialUnitsControllerApi(api_client)
    feature_data = openapi_client.SpatialUnitPOSTInputType() # SpatialUnitPOSTInputType | featureData

    try:
        # Add a new spatial-unit
        api_response = api_instance.add_spatial_unit_as_body(feature_data)
        print("The response of SpatialUnitsControllerApi->add_spatial_unit_as_body:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SpatialUnitsControllerApi->add_spatial_unit_as_body: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **feature_data** | [**SpatialUnitPOSTInputType**](SpatialUnitPOSTInputType.md)| featureData | 

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

# **delete_all_spatial_unit_features_by_id**
> ResponseEntity delete_all_spatial_unit_features_by_id(spatial_unit_id)

Delete all features/contents of the selected spatial-unit dataset

Delete all features/contents of the selected spatial-unit dataset

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
    api_instance = openapi_client.SpatialUnitsControllerApi(api_client)
    spatial_unit_id = 'spatial_unit_id_example' # str | spatialUnitId

    try:
        # Delete all features/contents of the selected spatial-unit dataset
        api_response = api_instance.delete_all_spatial_unit_features_by_id(spatial_unit_id)
        print("The response of SpatialUnitsControllerApi->delete_all_spatial_unit_features_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SpatialUnitsControllerApi->delete_all_spatial_unit_features_by_id: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **spatial_unit_id** | **str**| spatialUnitId | 

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

# **delete_spatial_unit_by_id**
> ResponseEntity delete_spatial_unit_by_id(spatial_unit_id)

Delete the features/contents of the selected spatial-unit

Delete the features/contents of the selected spatial-unit

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
    api_instance = openapi_client.SpatialUnitsControllerApi(api_client)
    spatial_unit_id = 'spatial_unit_id_example' # str | spatialUnitId

    try:
        # Delete the features/contents of the selected spatial-unit
        api_response = api_instance.delete_spatial_unit_by_id(spatial_unit_id)
        print("The response of SpatialUnitsControllerApi->delete_spatial_unit_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SpatialUnitsControllerApi->delete_spatial_unit_by_id: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **spatial_unit_id** | **str**| spatialUnitId | 

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

# **delete_spatial_unit_by_id_and_year_and_month**
> ResponseEntity delete_spatial_unit_by_id_and_year_and_month(day, month, spatial_unit_id, year)

Delete the features/contents of the selected spatial-unit, year and month

Delete the features/contents of the selected spatial-unit, year and month

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
    api_instance = openapi_client.SpatialUnitsControllerApi(api_client)
    day = 1.0 # float | day (default to 1.0)
    month = 1.0 # float | month (default to 1.0)
    spatial_unit_id = 'spatial_unit_id_example' # str | spatialUnitId
    year = 2023.0 # float | year (default to 2023.0)

    try:
        # Delete the features/contents of the selected spatial-unit, year and month
        api_response = api_instance.delete_spatial_unit_by_id_and_year_and_month(day, month, spatial_unit_id, year)
        print("The response of SpatialUnitsControllerApi->delete_spatial_unit_by_id_and_year_and_month:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SpatialUnitsControllerApi->delete_spatial_unit_by_id_and_year_and_month: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **day** | **float**| day | [default to 1.0]
 **month** | **float**| month | [default to 1.0]
 **spatial_unit_id** | **str**| spatialUnitId | 
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

# **get_all_spatial_unit_features_by_id**
> str get_all_spatial_unit_features_by_id(spatial_unit_id, name=name, simplify_geometries=simplify_geometries)

retrieve all feature entries for all applicable periods of validity for the selected spatial unit/level (hence might contain each feature multiple times if they exist for different periods of validity)

retrieve all feature entries for all applicable periods of validity for the selected spatial unit/level (hence might contain each feature multiple times if they exist for different periods of validity)

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
    api_instance = openapi_client.SpatialUnitsControllerApi(api_client)
    spatial_unit_id = 'spatial_unit_id_example' # str | spatialUnitId
    name = 'name_example' # str |  (optional)
    simplify_geometries = 'original' # str | simplifyGeometries (optional) (default to 'original')

    try:
        # retrieve all feature entries for all applicable periods of validity for the selected spatial unit/level (hence might contain each feature multiple times if they exist for different periods of validity)
        api_response = api_instance.get_all_spatial_unit_features_by_id(spatial_unit_id, name=name, simplify_geometries=simplify_geometries)
        print("The response of SpatialUnitsControllerApi->get_all_spatial_unit_features_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SpatialUnitsControllerApi->get_all_spatial_unit_features_by_id: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **spatial_unit_id** | **str**| spatialUnitId | 
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

# **get_spatial_units**
> SpatialUnitOverviewType get_spatial_units(name=name)

retrieve information about available features of different spatial units/levels

retrieve information about available features of different spatial units/levels

### Example

* OAuth Authentication (kommonitor-data-access_oauth):
```python
import time
import os
import openapi_client
from openapi_client.models.spatial_unit_overview_type import SpatialUnitOverviewType
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
    api_instance = openapi_client.SpatialUnitsControllerApi(api_client)
    name = 'name_example' # str |  (optional)

    try:
        # retrieve information about available features of different spatial units/levels
        api_response = api_instance.get_spatial_units(name=name)
        print("The response of SpatialUnitsControllerApi->get_spatial_units:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SpatialUnitsControllerApi->get_spatial_units: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | [optional] 

### Return type

[**SpatialUnitOverviewType**](SpatialUnitOverviewType.md)

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

# **get_spatial_units_by_id**
> SpatialUnitOverviewType get_spatial_units_by_id(spatial_unit_id, name=name)

retrieve information about available features of the selected spatial unit/level

retrieve information about available features of the selected spatial unit/level

### Example

* OAuth Authentication (kommonitor-data-access_oauth):
```python
import time
import os
import openapi_client
from openapi_client.models.spatial_unit_overview_type import SpatialUnitOverviewType
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
    api_instance = openapi_client.SpatialUnitsControllerApi(api_client)
    spatial_unit_id = 'spatial_unit_id_example' # str | spatialUnitId
    name = 'name_example' # str |  (optional)

    try:
        # retrieve information about available features of the selected spatial unit/level
        api_response = api_instance.get_spatial_units_by_id(spatial_unit_id, name=name)
        print("The response of SpatialUnitsControllerApi->get_spatial_units_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SpatialUnitsControllerApi->get_spatial_units_by_id: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **spatial_unit_id** | **str**| spatialUnitId | 
 **name** | **str**|  | [optional] 

### Return type

[**SpatialUnitOverviewType**](SpatialUnitOverviewType.md)

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

# **get_spatial_units_by_id_and_year_and_month**
> bytearray get_spatial_units_by_id_and_year_and_month(day, month, spatial_unit_id, year, name=name, simplify_geometries=simplify_geometries)

retrieve the features according to the selected spatial unit/level and selected year and month as GeoJSON

retrieve the features according to the selected spatial unit/level and selected year and month as GeoJSON

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
    api_instance = openapi_client.SpatialUnitsControllerApi(api_client)
    day = 1.0 # float | day (default to 1.0)
    month = 1.0 # float | month (default to 1.0)
    spatial_unit_id = 'spatial_unit_id_example' # str | spatialUnitId
    year = 2023.0 # float | year (default to 2023.0)
    name = 'name_example' # str |  (optional)
    simplify_geometries = 'original' # str | simplifyGeometries (optional) (default to 'original')

    try:
        # retrieve the features according to the selected spatial unit/level and selected year and month as GeoJSON
        api_response = api_instance.get_spatial_units_by_id_and_year_and_month(day, month, spatial_unit_id, year, name=name, simplify_geometries=simplify_geometries)
        print("The response of SpatialUnitsControllerApi->get_spatial_units_by_id_and_year_and_month:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SpatialUnitsControllerApi->get_spatial_units_by_id_and_year_and_month: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **day** | **float**| day | [default to 1.0]
 **month** | **float**| month | [default to 1.0]
 **spatial_unit_id** | **str**| spatialUnitId | 
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

# **get_spatial_units_schema_by_id**
> str get_spatial_units_schema_by_id(spatial_unit_id, name=name)

retrieve the JSON schema for the selected spatial unit/level

retrieve the JSON schema for the selected spatial unit/level. The JSON schema indicates the property structure of the dataset.

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
    api_instance = openapi_client.SpatialUnitsControllerApi(api_client)
    spatial_unit_id = 'spatial_unit_id_example' # str | spatialUnitId
    name = 'name_example' # str |  (optional)

    try:
        # retrieve the JSON schema for the selected spatial unit/level
        api_response = api_instance.get_spatial_units_schema_by_id(spatial_unit_id, name=name)
        print("The response of SpatialUnitsControllerApi->get_spatial_units_schema_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SpatialUnitsControllerApi->get_spatial_units_schema_by_id: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **spatial_unit_id** | **str**| spatialUnitId | 
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

# **update_spatial_unit_as_body**
> ResponseEntity update_spatial_unit_as_body(spatial_unit_id, feature_data)

Modify/Update the features of the selected spatial-unit

Modify/Update the features of the selected spatial-unit. The interface expects a full upload of all geometries for the spatial unit. Internally, those geometries are compared to the existing ones to mark 'old' geometries that are no longer in use as outdated. Hence, each geometric object is only persisted once and its use is controlled by time validity marks.

### Example

* OAuth Authentication (kommonitor-data-access_oauth):
```python
import time
import os
import openapi_client
from openapi_client.models.response_entity import ResponseEntity
from openapi_client.models.spatial_unit_put_input_type import SpatialUnitPUTInputType
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
    api_instance = openapi_client.SpatialUnitsControllerApi(api_client)
    spatial_unit_id = 'spatial_unit_id_example' # str | spatialUnitId
    feature_data = openapi_client.SpatialUnitPUTInputType() # SpatialUnitPUTInputType | featureData

    try:
        # Modify/Update the features of the selected spatial-unit
        api_response = api_instance.update_spatial_unit_as_body(spatial_unit_id, feature_data)
        print("The response of SpatialUnitsControllerApi->update_spatial_unit_as_body:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SpatialUnitsControllerApi->update_spatial_unit_as_body: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **spatial_unit_id** | **str**| spatialUnitId | 
 **feature_data** | [**SpatialUnitPUTInputType**](SpatialUnitPUTInputType.md)| featureData | 

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

# **update_spatial_unit_metadata_as_body**
> ResponseEntity update_spatial_unit_metadata_as_body(spatial_unit_id, metadata)

Modify/Update the metadata of the selected spatial-unit

Modify/Update the metadata of the selected spatial-unit. This replaces the formerly stored metadata.

### Example

* OAuth Authentication (kommonitor-data-access_oauth):
```python
import time
import os
import openapi_client
from openapi_client.models.response_entity import ResponseEntity
from openapi_client.models.spatial_unit_patch_input_type import SpatialUnitPATCHInputType
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
    api_instance = openapi_client.SpatialUnitsControllerApi(api_client)
    spatial_unit_id = 'spatial_unit_id_example' # str | spatialUnitId
    metadata = openapi_client.SpatialUnitPATCHInputType() # SpatialUnitPATCHInputType | metadata

    try:
        # Modify/Update the metadata of the selected spatial-unit
        api_response = api_instance.update_spatial_unit_metadata_as_body(spatial_unit_id, metadata)
        print("The response of SpatialUnitsControllerApi->update_spatial_unit_metadata_as_body:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SpatialUnitsControllerApi->update_spatial_unit_metadata_as_body: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **spatial_unit_id** | **str**| spatialUnitId | 
 **metadata** | [**SpatialUnitPATCHInputType**](SpatialUnitPATCHInputType.md)| metadata | 

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

