# openapi_client.IndicatorsPublicControllerApi

All URIs are relative to *http://localhost:8085*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_indicators1**](IndicatorsPublicControllerApi.md#get_indicators1) | **GET** /management/public/indicators | retrieve information about available public indicators
[**get_public_indicator_by_id**](IndicatorsPublicControllerApi.md#get_public_indicator_by_id) | **GET** /management/public/indicators/{indicatorId} | retrieve information about the selected public indicator
[**get_public_indicator_by_spatial_unit_id_and_id**](IndicatorsPublicControllerApi.md#get_public_indicator_by_spatial_unit_id_and_id) | **GET** /management/public/indicators/{indicatorId}/{spatialUnitId} | retrieve the public indicator for the selected spatial unit as GeoJSON
[**get_public_indicator_by_spatial_unit_id_and_id_and_year_and_month**](IndicatorsPublicControllerApi.md#get_public_indicator_by_spatial_unit_id_and_id_and_year_and_month) | **GET** /management/public/indicators/{indicatorId}/{spatialUnitId}/{year}/{month}/{day} | retrieve the public indicator for the selected public spatial unit, year and month as GeoJSON
[**get_public_indicator_by_spatial_unit_id_and_id_and_year_and_month_without_geometry**](IndicatorsPublicControllerApi.md#get_public_indicator_by_spatial_unit_id_and_id_and_year_and_month_without_geometry) | **GET** /management/public/indicators/{indicatorId}/{spatialUnitId}/{year}/{month}/{day}/without-geometry | retrieve the public indicator values and other properties for the selected public spatial unit, year and month. It does not include the spatial geometries!
[**get_public_indicator_by_spatial_unit_id_and_id_without_geometry**](IndicatorsPublicControllerApi.md#get_public_indicator_by_spatial_unit_id_and_id_without_geometry) | **GET** /management/public/indicators/{indicatorId}/{spatialUnitId}/without-geometry | retrieve the public indicator values and other properties for the selected public spatial unit. It does not include the spatial geometries!


# **get_indicators1**
> IndicatorOverviewType get_indicators1()

retrieve information about available public indicators

retrieve information about available public indicators

### Example

* OAuth Authentication (kommonitor-data-access_oauth):
```python
import time
import os
import openapi_client
from openapi_client.models.indicator_overview_type import IndicatorOverviewType
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
    api_instance = openapi_client.IndicatorsPublicControllerApi(api_client)

    try:
        # retrieve information about available public indicators
        api_response = api_instance.get_indicators1()
        print("The response of IndicatorsPublicControllerApi->get_indicators1:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IndicatorsPublicControllerApi->get_indicators1: %s\n" % e)
```



### Parameters
This endpoint does not need any parameter.

### Return type

[**IndicatorOverviewType**](IndicatorOverviewType.md)

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

# **get_public_indicator_by_id**
> IndicatorOverviewType get_public_indicator_by_id(indicator_id)

retrieve information about the selected public indicator

retrieve information about the selected public indicator

### Example

* OAuth Authentication (kommonitor-data-access_oauth):
```python
import time
import os
import openapi_client
from openapi_client.models.indicator_overview_type import IndicatorOverviewType
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
    api_instance = openapi_client.IndicatorsPublicControllerApi(api_client)
    indicator_id = 'indicator_id_example' # str | indicatorId

    try:
        # retrieve information about the selected public indicator
        api_response = api_instance.get_public_indicator_by_id(indicator_id)
        print("The response of IndicatorsPublicControllerApi->get_public_indicator_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IndicatorsPublicControllerApi->get_public_indicator_by_id: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **indicator_id** | **str**| indicatorId | 

### Return type

[**IndicatorOverviewType**](IndicatorOverviewType.md)

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

# **get_public_indicator_by_spatial_unit_id_and_id**
> bytearray get_public_indicator_by_spatial_unit_id_and_id(indicator_id, spatial_unit_id, simplify_geometries=simplify_geometries)

retrieve the public indicator for the selected spatial unit as GeoJSON

retrieve the public indicator for the selected spatial unit as GeoJSON

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
    api_instance = openapi_client.IndicatorsPublicControllerApi(api_client)
    indicator_id = 'indicator_id_example' # str | indicatorId
    spatial_unit_id = 'spatial_unit_id_example' # str | spatialUnitId
    simplify_geometries = 'original' # str | simplifyGeometries (optional) (default to 'original')

    try:
        # retrieve the public indicator for the selected spatial unit as GeoJSON
        api_response = api_instance.get_public_indicator_by_spatial_unit_id_and_id(indicator_id, spatial_unit_id, simplify_geometries=simplify_geometries)
        print("The response of IndicatorsPublicControllerApi->get_public_indicator_by_spatial_unit_id_and_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IndicatorsPublicControllerApi->get_public_indicator_by_spatial_unit_id_and_id: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **indicator_id** | **str**| indicatorId | 
 **spatial_unit_id** | **str**| spatialUnitId | 
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

# **get_public_indicator_by_spatial_unit_id_and_id_and_year_and_month**
> bytearray get_public_indicator_by_spatial_unit_id_and_id_and_year_and_month(day, indicator_id, month, spatial_unit_id, year, simplify_geometries=simplify_geometries)

retrieve the public indicator for the selected public spatial unit, year and month as GeoJSON

retrieve the public indicator for the selected spatial unit, year and month as GeoJSON

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
    api_instance = openapi_client.IndicatorsPublicControllerApi(api_client)
    day = 1.0 # float | day (default to 1.0)
    indicator_id = 'indicator_id_example' # str | indicatorId
    month = 1.0 # float | month (default to 1.0)
    spatial_unit_id = 'spatial_unit_id_example' # str | spatialUnitId
    year = 2023.0 # float | year (default to 2023.0)
    simplify_geometries = 'original' # str | simplifyGeometries (optional) (default to 'original')

    try:
        # retrieve the public indicator for the selected public spatial unit, year and month as GeoJSON
        api_response = api_instance.get_public_indicator_by_spatial_unit_id_and_id_and_year_and_month(day, indicator_id, month, spatial_unit_id, year, simplify_geometries=simplify_geometries)
        print("The response of IndicatorsPublicControllerApi->get_public_indicator_by_spatial_unit_id_and_id_and_year_and_month:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IndicatorsPublicControllerApi->get_public_indicator_by_spatial_unit_id_and_id_and_year_and_month: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **day** | **float**| day | [default to 1.0]
 **indicator_id** | **str**| indicatorId | 
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

# **get_public_indicator_by_spatial_unit_id_and_id_and_year_and_month_without_geometry**
> Dict[str, str] get_public_indicator_by_spatial_unit_id_and_id_and_year_and_month_without_geometry(day, indicator_id, month, spatial_unit_id, year)

retrieve the public indicator values and other properties for the selected public spatial unit, year and month. It does not include the spatial geometries!

retrieve the public indicator values and other properties for the selected public spatial unit, year and month. It does not include the spatial geometries!

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
    api_instance = openapi_client.IndicatorsPublicControllerApi(api_client)
    day = 1.0 # float | day (default to 1.0)
    indicator_id = 'indicator_id_example' # str | indicatorId
    month = 1.0 # float | month (default to 1.0)
    spatial_unit_id = 'spatial_unit_id_example' # str | spatialUnitId
    year = 2023.0 # float | year (default to 2023.0)

    try:
        # retrieve the public indicator values and other properties for the selected public spatial unit, year and month. It does not include the spatial geometries!
        api_response = api_instance.get_public_indicator_by_spatial_unit_id_and_id_and_year_and_month_without_geometry(day, indicator_id, month, spatial_unit_id, year)
        print("The response of IndicatorsPublicControllerApi->get_public_indicator_by_spatial_unit_id_and_id_and_year_and_month_without_geometry:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IndicatorsPublicControllerApi->get_public_indicator_by_spatial_unit_id_and_id_and_year_and_month_without_geometry: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **day** | **float**| day | [default to 1.0]
 **indicator_id** | **str**| indicatorId | 
 **month** | **float**| month | [default to 1.0]
 **spatial_unit_id** | **str**| spatialUnitId | 
 **year** | **float**| year | [default to 2023.0]

### Return type

**Dict[str, str]**

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

# **get_public_indicator_by_spatial_unit_id_and_id_without_geometry**
> Dict[str, str] get_public_indicator_by_spatial_unit_id_and_id_without_geometry(indicator_id, spatial_unit_id)

retrieve the public indicator values and other properties for the selected public spatial unit. It does not include the spatial geometries!

retrieve the public indicator values and other properties for the selected public spatial unit. It does not include the spatial geometries!

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
    api_instance = openapi_client.IndicatorsPublicControllerApi(api_client)
    indicator_id = 'indicator_id_example' # str | indicatorId
    spatial_unit_id = 'spatial_unit_id_example' # str | spatialUnitId

    try:
        # retrieve the public indicator values and other properties for the selected public spatial unit. It does not include the spatial geometries!
        api_response = api_instance.get_public_indicator_by_spatial_unit_id_and_id_without_geometry(indicator_id, spatial_unit_id)
        print("The response of IndicatorsPublicControllerApi->get_public_indicator_by_spatial_unit_id_and_id_without_geometry:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IndicatorsPublicControllerApi->get_public_indicator_by_spatial_unit_id_and_id_without_geometry: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **indicator_id** | **str**| indicatorId | 
 **spatial_unit_id** | **str**| spatialUnitId | 

### Return type

**Dict[str, str]**

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

