# openapi_client.SpatialUnitsPublicControllerApi

All URIs are relative to *http://localhost:8085*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_all_spatial_unit_features_by_id1**](SpatialUnitsPublicControllerApi.md#get_all_spatial_unit_features_by_id1) | **GET** /management/public/spatial-units/{spatialUnitId}/allFeatures | retrieve all feature entries for all applicable periods of validity for the selected spatial unit/level (hence might contain each feature multiple times if they exist for different periods of validity)
[**get_spatial_units1**](SpatialUnitsPublicControllerApi.md#get_spatial_units1) | **GET** /management/public/spatial-units | retrieve information about available features of different spatial units/levels
[**get_spatial_units_by_id1**](SpatialUnitsPublicControllerApi.md#get_spatial_units_by_id1) | **GET** /management/public/spatial-units/{spatialUnitId} | retrieve information about available features of the selected spatial unit/level
[**get_spatial_units_by_id_and_year_and_month1**](SpatialUnitsPublicControllerApi.md#get_spatial_units_by_id_and_year_and_month1) | **GET** /management/public/spatial-units/{spatialUnitId}/{year}/{month}/{day} | retrieve the features according to the selected spatial unit/level and selected year and month as GeoJSON
[**get_spatial_units_schema_by_id1**](SpatialUnitsPublicControllerApi.md#get_spatial_units_schema_by_id1) | **GET** /management/public/spatial-units/{spatialUnitId}/schema | retrieve the JSON schema for the selected spatial unit/level


# **get_all_spatial_unit_features_by_id1**
> str get_all_spatial_unit_features_by_id1(spatial_unit_id, simplify_geometries=simplify_geometries)

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
    api_instance = openapi_client.SpatialUnitsPublicControllerApi(api_client)
    spatial_unit_id = 'spatial_unit_id_example' # str | spatialUnitId
    simplify_geometries = 'original' # str | simplifyGeometries (optional) (default to 'original')

    try:
        # retrieve all feature entries for all applicable periods of validity for the selected spatial unit/level (hence might contain each feature multiple times if they exist for different periods of validity)
        api_response = api_instance.get_all_spatial_unit_features_by_id1(spatial_unit_id, simplify_geometries=simplify_geometries)
        print("The response of SpatialUnitsPublicControllerApi->get_all_spatial_unit_features_by_id1:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SpatialUnitsPublicControllerApi->get_all_spatial_unit_features_by_id1: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **spatial_unit_id** | **str**| spatialUnitId | 
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

# **get_spatial_units1**
> List[SpatialUnitOverviewType] get_spatial_units1()

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
    api_instance = openapi_client.SpatialUnitsPublicControllerApi(api_client)

    try:
        # retrieve information about available features of different spatial units/levels
        api_response = api_instance.get_spatial_units1()
        print("The response of SpatialUnitsPublicControllerApi->get_spatial_units1:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SpatialUnitsPublicControllerApi->get_spatial_units1: %s\n" % e)
```



### Parameters
This endpoint does not need any parameter.

### Return type

[**List[SpatialUnitOverviewType]**](SpatialUnitOverviewType.md)

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

# **get_spatial_units_by_id1**
> SpatialUnitOverviewType get_spatial_units_by_id1(spatial_unit_id)

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
    api_instance = openapi_client.SpatialUnitsPublicControllerApi(api_client)
    spatial_unit_id = 'spatial_unit_id_example' # str | spatialUnitId

    try:
        # retrieve information about available features of the selected spatial unit/level
        api_response = api_instance.get_spatial_units_by_id1(spatial_unit_id)
        print("The response of SpatialUnitsPublicControllerApi->get_spatial_units_by_id1:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SpatialUnitsPublicControllerApi->get_spatial_units_by_id1: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **spatial_unit_id** | **str**| spatialUnitId | 

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

# **get_spatial_units_by_id_and_year_and_month1**
> bytearray get_spatial_units_by_id_and_year_and_month1(day, month, spatial_unit_id, year, simplify_geometries=simplify_geometries)

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
    api_instance = openapi_client.SpatialUnitsPublicControllerApi(api_client)
    day = 1.0 # float | day (default to 1.0)
    month = 1.0 # float | month (default to 1.0)
    spatial_unit_id = 'spatial_unit_id_example' # str | spatialUnitId
    year = 2023.0 # float | year (default to 2023.0)
    simplify_geometries = 'original' # str | simplifyGeometries (optional) (default to 'original')

    try:
        # retrieve the features according to the selected spatial unit/level and selected year and month as GeoJSON
        api_response = api_instance.get_spatial_units_by_id_and_year_and_month1(day, month, spatial_unit_id, year, simplify_geometries=simplify_geometries)
        print("The response of SpatialUnitsPublicControllerApi->get_spatial_units_by_id_and_year_and_month1:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SpatialUnitsPublicControllerApi->get_spatial_units_by_id_and_year_and_month1: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **day** | **float**| day | [default to 1.0]
 **month** | **float**| month | [default to 1.0]
 **spatial_unit_id** | **str**| spatialUnitId | 
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

# **get_spatial_units_schema_by_id1**
> str get_spatial_units_schema_by_id1(spatial_unit_id)

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
    api_instance = openapi_client.SpatialUnitsPublicControllerApi(api_client)
    spatial_unit_id = 'spatial_unit_id_example' # str | spatialUnitId

    try:
        # retrieve the JSON schema for the selected spatial unit/level
        api_response = api_instance.get_spatial_units_schema_by_id1(spatial_unit_id)
        print("The response of SpatialUnitsPublicControllerApi->get_spatial_units_schema_by_id1:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SpatialUnitsPublicControllerApi->get_spatial_units_schema_by_id1: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **spatial_unit_id** | **str**| spatialUnitId | 

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

