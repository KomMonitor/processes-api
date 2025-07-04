"""

import necessary Node Module Dependencies

"""
import copy

from scipy import stats
import numpy
import geopandas as gpd
import geojson
import json
import math
import shapely
import datetime
from logging import Logger
from enum import Enum
import openapi_client
from openapi_client import IndicatorOverviewType, IndicatorsControllerApi, SpatialUnitsControllerApi, GeorecourcesControllerApi, ApiException
from openapi_client.exceptions import ForbiddenException
from .base import KommonitorProcess, KommonitorProcessConfig, KommonitorResult, KommonitorJobSummary, KOMMONITOR_DATA_MANAGEMENT_URL, DataManagementException
from typing import Optional, Tuple

# Define custom CONSTANTS used within the script

# This constant is required to aquire the unique identifier of a certain feature of a spatial unit
spatialUnitFeatureIdPropertyName = "ID"

# This constant is required to aquire the unique name of a certain feature of a spatial unit
spatialUnitFeatureNamePropertyName = "NAME"

# This constant is required to access indicator timeseries values correctly (i.e. DATE_2018-01-01)
indicator_date_prefix = "DATE_"

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

API_HELPER_METHODS_UTILITY

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def getBaseIndicatorByName(indicatorName, baseIndicatorsDict):
    """Aquire the base indicator with the name 'indicatorName' from the delivered dictionary 'baseIndicatorsDict'

    Args:
        indicatorID (string): the ID of the base indicator
        baseIndicatorsDict (Dict<string, FeatureCollection<Polygon>): Dict containing all indicators, whereas key='meaningful name or id of the indicator' an value='indicator as FeatureCollection '(it contains duplicate entries, one for the indicator name and one for the indicator id)

    Raises:
        Exception: if the Dict does not contain an entry with given Name

    Returns:
        FeatureCollection<Polygon>: baseIndicatorCandidate (FeatureCollection<Polygon>): returns the base indicator as FeatureCollection or throws an error if the baseIndicatorsDict does not contain an entry with key=indicatorID 
    """
    if indicatorName in baseIndicatorsDict:
        return baseIndicatorsDict[indicatorName]
    else:
        log("Tried to acquire a baseIndicator with name '" + str(indicatorName) + "', but the baseIndicatorDict does not contain such an  entry")
        throwError("Tried to acquire a baseIndicator with name '" + str(indicatorName) + "', but the baseIndicatorDict does not contain such an  entry")


def getBaseIndicatorByID(indicatorID, baseIndicatorsDict):
    """Aquire the base indicator with the id 'indicatorID' from the delivered dictionary 'baseIndicatorsDict'

    Args:
        indicatorID (string): the ID of the base indicator
        baseIndicatorsDict (Dict<string, FeatureCollection<Polygon>>): Dict containing all indicators, whereas key='meaningful name or id of the indicator' an value='indicator as FeatureCollection<Polygon>'(it contains duplicate entries, one for the indicator name and one for the indicator id)

    Raises:
        Exception: if the Dict does not contain an entry with given ID

    Returns:
        FeatureCollection<Polygon>: baseIndicatorCandidate (FeatureCollection<Polygon>): returns the base indicator as FeatureCollection<Polygon> or throws an error if the baseIndicatorsDict does not contain an entry with key=indicatorID 
    """
    
    if indicatorID in baseIndicatorsDict:
        return baseIndicatorsDict[indicatorID]
    else:
        log("Tried to acquire a baseIndicator with name '" + str(indicatorID) + "', but the baseIndicatorDict does not contain such an  entry")
        throwError("Tried to acquire a baseIndicator with name '" + str(indicatorID) + "', but the baseIndicatorDict does not contain such an  entry")


def getGeoressourceByName(georesourceName, georesourcesDict):
    """Acqiures the georesource with the name 'georesourceName' from the submitted 'georesourcesDict'

    Args:
        georesourceName (string): the name of the georesource
        georesourcesDict (Dict<string, FeatureCollection<Polygon|LineString|Point>): Dict containing all georesources, whereas key='meaningful name or id of the georesource' and value='georesource as FeatureCollection<Polygon> object' (it contains duplicate entries, one for the georesource's name and one for the georesource's id)

    Raises:
        Exception: if the dict does not contain an entry with 'georesourceName'

    Returns:
        FeatureCollection<Polygon|LineString|Point>: returns the georesource 
    """
    if georesourceName in georesourcesDict:
        return georesourcesDict[georesourceName]
    else:
        log("Tried to acquire a georesource with name '" + str(georesourceName) + "', but the georesourceDict does not contain such an  entry")
        throwError("Tried to acquire a georesource with name '" + str(georesourceName) + "', but the georesourceDict does not contain such an  entry")

def getGeoresourceByID(georesourceID, georesourcesDict):
    """Acqiures the georesource with the id 'georesourceID' from the submitted 'georesourcesDict'

    Args:
        georesourceName (string): the name of the georesource
        georesourcesDict (Dict<string, FeatureCollection<Polygon|LineString|Point>): Map containing all georesources, whereas key='meaningful name or id of the georesource' and value='georesource as FeatureCollection<Polygon|LineString|Point>' (it contains duplicate entries, one for the georesource's name and one for the georesource's id)

    Raises:
        Exception: if the dict does not contain an entry with 'georesourceID'

    Returns:
        FeatureCollection<Polygon|LineString|Point>: returns the georesource 
    """
    if georesourceID in georesourcesDict:
        return georesourcesDict[georesourceID]
    else:
        log("Tried to acquire a georesource with name '" + str(georesourceID) + "', but the georesourceDict does not contain such an  entry")
        throwError("Tried to acquire a georesource with name '" + str(georesourceID) + "', but the georesourceDict does not contain such an  entry")

def getProcessParameterByName_asString(parameterName, processParameters):
    """Acuires the process parameter with the name 'parameterName' from the submitted processParameters Array. 

    Args:
        parameterName (string): the name of the process parameter
        processParameters (Array<Dict<string, (string|number|boolean)>>>): an array containing dictionaries containing the keys 'name' and 'value' describing the name and value of a processParameter. Representing variable additional process parameters that are required to perform the indicator computation.

    Raises:
        Exception: if the dict does not contain a parameter with given name

    Returns:
        String: returns the values of the requested process Parameter as String. Useres should know the real type i. e. boolean or number
    """
    value = None

    for parameter in processParameters:
        if parameter["name"] == parameterName:
            value = str(parameter["value"])
                
    if value is None:
        throwError(f"Tried to acquire a process parameter with name '" + str(parameterName) + "', but the Array of processParameter Dictionarys does not contain such an entry")

    return value

def getProcessParameterByName_asNumber(parameterName, processParameters):
    """Acuires the process parameter with the name 'parameterName' from the submitted processParameters Array. 

    Args:
        parameterName (string): the name of the process parameter
        processParameters (Array<Dict<string, (string|number|boolean)>>>): an array containing dictionaries containing the keys 'name' and 'value' describing the name and value of a processParameter. Representing variable additional process parameters that are required to perform the indicator computation.

    Raises:
        Exception: if the dict does not contain a parameter with given name

    Returns:
        float: returns the values of the requested process Parameter as float. Useres should know the real type i. e. boolean or string.
    """
    value = None

    for parameter in processParameters:
        if parameter["name"] == parameterName:
            try:
                value = float(parameter["value"])
            except ValueError:
                throwError("Error while parsing parameter value '" + str(parameter["value"]) + "' from parameter with name '" + str(parameterName) + "' as float.")
                
    if value is None:
        throwError(f"Tried to acquire a process parameter with name '" + str(parameterName) + "', but the Array of processParameter Dictionarys does not contain such an entry")

    return value

def getProcessParameterByName_asBoolean(parameterName, processParameters):
    """Acuires the process parameter with the name 'parameterName' from the submitted processParameters Array. 

    Args:
        parameterName (string): the name of the process parameter
        processParameters (Array<Dict<string, (string|number|boolean)>>>): an array containing dictionaries containing the keys 'name' and 'value' describing the name and value of a processParameter. Representing variable additional process parameters that are required to perform the indicator computation.

    Raises:
        Exception: if the dict does not contain a parameter with given name

    Returns:
        bool: returns the values of the requested process Parameter as boolean. Useres should know the real type i. e. float or string.
    """
    value = None

    for parameter in processParameters:
        if parameter["name"] == parameterName:
            try:
                value = eval(parameter["value"])
            except NameError:
                throwError("Error while parsing parameter value '" + str(parameter["value"]) + "' from parameter with name '" + str(parameterName) + "' as float.")
                
    if value is None:
        throwError(f"Tried to acquire a process parameter with name '" + str(parameterName) + "', but the Array of processParameter Dictionarys does not contain such an entry")

    return value
    
def getSpatialUnitFeatureIdValue(feature):
    """Acquire the unique feature id of the submitted GeoJSON feature representing a spatial unit. (i.e. city districts, building blocks, etc).

    Args:
        feature (GeoJSONFeature<Polygon>): the GeoJSON feature representing a spatial unit (i.e. city districts, building blocks, etc), which must accord to the KomMonitor specific data model. It then has a property named "ID" that holds the value of the unique feature id.

    Returns:
        string: returns the unique feature id of the unique GeoJSON Feature
    """
    return str(feature["properties"][spatialUnitFeatureIdPropertyName])

def getSpatialUnitFeatureNameValue(feature):
    """Acquire the unique feature name of the submitted GeoJSON feature representing a spatial unit. (i.e. city districts, building blocks, etc).

    Args:
        feature (GeoJSONFeature<Polygon>): the GeoJSON feature representing a spatial unit (i.e. city districts, building blocks, etc), which must accord to the KomMonitor specific data model. It then has a property named "ID" that holds the value of the unique feature id.

    Returns:
        string: returns the unique feature name of the unique GeoJSON Feature
    """
    return str(feature["properties"][spatialUnitFeatureNamePropertyName])

def log(logMessage):
    """Implement function 'log' from module 'logging' to write an output Message to the console

    Args:
        logMessage (string): the message the shall be logged
    """
    print(logMessage)
    # TODO: ProgressHelperService

def throwError(logMessage):
    """Implement function 'error' from module 'logging' to raise an error to the console

    Args:
        logMessage (string): the error message that shall be raised
    """
    raise RuntimeError(logMessage)
    # TODO: ProgressHelperService


def isGeoJSONFeature(feature):
    """Checks whether the submitted object is a valid GeoJSON Feature

    Args:
        feature (GeoJSONFeature): a candidate for a GeoJsonFeature

    Returns:
        bool: wheter the object is a valid GeoJSONFeature('True') or not ('False')
    """
    if feature["type"] == "Feature" and bool(feature["geometry"]) and bool(feature["geometry"]["coordinates"]) and bool(feature["geometry"]["type"]):
        return True
    else:
        return False

def isGeoJSONPointFeature(feature):
    """Checks whether the submitted object is a valid GeoJSON feature with geometryType Point. The Feature must contain a property ("type"="Feature") and a property named ("geometry")
    which must have a Coordinates Array and a property ("type"="Point"). The Method does not check if the feature contains a "properties" attribute.

    Args:
        feature (GeoJSONFeature): a candidate for the GeoJSON Point Feature

    Returns:
        bool: whether the Feature is a valid GeoJSON Point Feature or not
    """
    if feature["type"] == "Feature" and bool(feature["geometry"]) and bool(feature["geometry"]["coordinates"]) and feature["geometry"]["type"] == "Point":
        return True
    else:
        return False
    
def isGeoJSONLineStringFeature(feature):
    """Checks whether the submitted object is a valid GeoJSON feature with geometryType LineString. The Feature must contain a property ("type"="Feature") and a property named ("geometry")
    which must have a Coordinates Array and a property ("type"="LineString"). The Method does not check if the feature contains a "properties" attribute.

    Args:
        feature (GeoJSONFeature): a candidate for the GeoJSON LineString Feature

    Returns:
        bool: whether the Feature is a valid GeoJSON LineString Feature or not
    """
    if feature["type"] == "Feature" and bool(feature["geometry"]) and bool(feature["geometry"]["coordinates"]) and (feature["geometry"]["type"] == "LineString" or feature["geometry"]["type"] == "MultiLineString"):
        return True
    else:
        return False
    
def isGeoJSONPolygonFeature(feature):
    """Checks whether the submitted object is a valid GeoJSON feature with geometryType Polygon. The Feature must contain a property ("type"="Feature") and a property named ("geometry")
    which must have a Coordinates Array and a property ("type"="Polygon"). The Method does not check if the feature contains a "properties" attribute.

    Args:
        feature (GeoJSONFeature): a candidate for the GeoJSON Polygon Feature

    Returns:
        bool: whether the Feature is a valid GeoJSON Polygon Feature or not
    """
    if feature["type"] == "Feature" and bool(feature["geometry"]) and bool(feature["geometry"]["coordinates"]) and (feature["geometry"]["type"] == "Polygon" or feature["geometry"]["type"] == "MultiPolygon"):
        return True
    else:
        return False

def isGeoJSONFeatureCollection(featureCollection):
    """Checks whether the submitted object is a valid GeoJSON FeatureCollection. The Feature must contain a property ("type"="Feature") and a property named ("geometry")
    which must have a Coordinates Array and a property ("type"="Polygon"). The Method does not check if the feature contains a "properties" attribute.

    Args:
        feature (GeoJSONFeature): a candidate for the GeoJSON FeatureCollection

    Returns:
        bool: whether the Feature is a valid GeoJSON FeatureCollection or not
    """
    if featureCollection["type"] == "FeatureCollection" and bool(featureCollection["features"]):
        isValid = True
        
        # check all child features
        for feature in featureCollection["features"]:
            if not isGeoJSONFeature(feature):
                isValid = False
                break
    
    else:
        isValid = False
    return isValid

def getPropertyValue(feature, propertyName):
    """Acquire the feature´s property value for the specified 'propertyName'

    Args:
        feature (Feature): a valid GeoJSON Feature which must contain a properties attribute storing a certain property value
        propertyName (string): the name of the queried property

    Returns:
        number|string|none: returns the value of the specified property or none if the feature does not contain such a property
    """
    if propertyName in feature["properties"]:
        return feature["properties"][propertyName]
    else:
        return None

def setPropertyValue(feature, propertyName, propertyValue):
    """Add a new property to the 'feature'

    Args:
        feature (Feature): a valid GeoJSON Feature, which must contain a 'properties' attribute storing certain property values
        propertyName (string): the name of the property
        propertyValue (object): the value of the property

    Returns:
        Feature: returns the submitted feature which was enriched with the submitted property
    """
    feature["properties"][propertyName] = propertyValue
    return feature

def setAggregationWeight(feature, weightValue):
    """Add a new weight-specific property ('aggregationWeight') to the given Feature. It can be utilized when aggregating lower spatial units to higher spatial units,
    where relevant features might be weighted differently in an average-based aggretation process

    Args:
        feature (Feature): a valid GeoJSON Feature which must contain a 'properties' attribute storing certain property values.
        weightValue (object): the value of the aggregation weight, if no value is submitted the aggregation weight will be set to 1

    Returns:
        Feature: returns the submitted feature which was enriched with the submitted property. The property is available under feature["properties"]["aggregationWeight"]
    """
    if bool(weightValue):
        feature["properties"]["aggregationWeight"] = weightValue
    else:
        feature["properties"]["aggregationWeight"] = 1
    return feature

def getAggregationWeight(feature):
    """Query the weight-specific property ('aggregationWeight') from the given Feature. It can be utilized when aggregating lower spatial units to higher spatial units,
    where relevant features might be weighted differently in an average-based aggretation process

    Args:
        feature (Feature): a valid GeoJSON Feature which must contain a 'properties' attribute storing certain property values.
        
    Returns:
        Feature: returns the value of the 'aggregationWeight' property. If the submitted Feature has no property 'aggregationWeight' the return value is 1
    """
    if bool(feature["properties"]["aggregationWeight"]):
        return feature["properties"]["aggregationWeight"]
    else:
        return 1
    
def getIndicatorValue(feature, targetDate):
    """Acquire the feature´s indicator value for the specified 'targetDate'

    Args:
        feature (Feature): a valid GeoJSON Feature, which must contain a properties attribute storing the indicator time series according to KomMonitors data model
        targetDate (string): string representing the target date for which the indicator value shall be extracted, following the pattern 'YYYY-MM-DD', e.g. '2018-01-01'

    Returns:
        number|none: returns the indicator value for the specified 'targetDate' or 'none' if the feature does not contain an indicator value for the specified 'targetDate'  
    """
    if indicator_date_prefix in targetDate:
        targetDateWithPrefix = targetDate
    else:
        targetDateWithPrefix = getTargetDateWithPropertyPrefix(targetDate)
    
    indicatorValue = feature[targetDateWithPrefix]

    if indicatorValue is None:
        return None
    else:
        return float(indicatorValue)
    
def getIndicatorValueArray(featureCollection, targetDate):
    """Aquire the array of indicator values for the specified 'targetDate'

    Args:
        featureCollection (FeatureCollection): a valid GeoJSON FeatureCollection, whose features must contain a 'properties' attribute storing the indicator time series according to KomMonitor's data model
        targetDate (string): string representing the target date for which the indicator value shall be extracted, following the pattern 'YYYY-MM-DD', e.g. '2018-01-01'

    Returns:
        Array<Number>|None: returns the indicator values of all features of the FeatureCollection for the specified 'targetDATe' or none if none of the feature include a property with given value
    """
    targetDateWithPrefix = getTargetDateWithPropertyPrefix(targetDate)

    resultArray = []

    for feature in featureCollection["features"]:
        indicatorValue = feature["properties"][targetDateWithPrefix]

        if bool(indicatorValue):
            resultArray.append(indicatorValue)
        else: 
            log("A feature did not contain an indicator value for the targetDate " + str(targetDate) + ". Feature was: " + str(feature))
    
    if len(resultArray) == 0:
        log("No feature of the featureCollection contains an indicator value for the specified targetDate " + str(targetDate) + ". Thus return null.")
        return None

    return resultArray    

def getIndicatorIDValueDict(featureCollection, targetDate):
    """Aquire a map of all indicator id and value pairs for the specified 'targetDate', where key=id and value=indicatorValue.

    Args:
        featureCollection (FeatureCollection): a valid GeoJSON FeatureCollection, whose features must contain a 'properties' attribute storing the indicator time series according to KomMonitor's data model
        targetDate (string): string representing the target date for which the indicator value shall be extracted, following the pattern 'YYYY-MM-DD', e.g. '2018-01-01'

    Returns:
        Dict<string, number>: returns dictionary of all indicator id and value pairs for the specified 'targetDate' where key=id and value=indicatorValue; or 'None' if the features do not contain an indicator value for the specified date.
    """
    targetDateWithPrefix = getTargetDateWithPropertyPrefix(targetDate)

    resultDict = {}

    for feature in featureCollection["features"]:
        indicatorValue = feature["properties"][targetDateWithPrefix]
        featureID = getSpatialUnitFeatureIdValue(feature)

        if bool(indicatorValue):
            resultDict[featureID] = indicatorValue
        else:
            log("A feature did not contain an indicator value for the targetDate " + str(targetDate) + ". Feature was: " + str(feature))
    
    if len(resultDict) == 0:
        log("No feature of the featureCollection contains an indicator value for the specified targetDate " + str(targetDate) + ". Thus return null.")
        return None
    
    return resultDict

def getIndicatorValueArray_fromIdValueDict(indicatorIdValueDict: dict):
    """transform an existing dictionary 'indicatorIdValueDict' into an array storing the values of the indicators

    Args:
        indicatorIdValueDict (dict): dict of all indicator id and value pairs where key=id and value=indicatorValue

    Returns:
        Array<number>: returns alle indicator values of all features of the 'indicatorIdValueDict
    """
    resultArray = []

    for key in indicatorIdValueDict.keys():
        if bool(key):
            resultArray.append(indicatorIdValueDict[key])
        else:
            log("A feature from indicator id value map did not contain an indicator value. Feature has ID: " + str(key))
    
    return resultArray

def getPropertyValueArray(featureCollection, propertyName):
    """Aquire the array of property values for the specified 'propertyName'.

    Args:
        featureCollection (FeatureCollection): a valid GeoJSON FeatureCollection, whose features must contain a 'properties' attribute storing at least one property with the submitted 'propertyName'
        propertyName (string): string representing the propertyName for which the value array shall be extracted

    Returns:
        Array<Object>: returns the property values of all features of the FeatureCollection for the specified 'propertyName' or 'None' of no property with the given Name exists
    """
    resultArray = []

    for feature in featureCollection["features"]:
        propertyValue = feature["properties"][propertyName]

        if bool(propertyValue):
            resultArray.append(propertyValue)
        else:
            log("A feature did not contain a property value for the propertyName " + str(propertyName) + ". Feature was: " + str(feature))
    
    if len(resultArray) == 0:
        throwError("No feature of the featureCollection contains a property value for the specified propertyName " + str(propertyName) + ". Thus return null.")
        return None
    
    return resultArray

def setIndicatorValue(feature, targetDate, value):
    """set the features indicator value for the specified 'targetDate' with the specified 'value'

    Args:
        feature (Feature): a valid GeoJSON Feature
        targetDate (string): string representing the target date for which the indicator value shall be set, following the pattern 'YYYY-MM-DD', e.g. '2018-01-01'
        value (number): a numeric value which shall be set as the 'feature''s indicator value for the specified 'targetDate'

    Returns:
        Feature: returns the GeoJSON Feature
    """
    if type(value) != float and type(value) != int:
        log("The submitted value is not a valid number. Indicator values must be numeric (float, int) though. The submitted value was: " + str(value))
        log("Affected has ID : " + str(getSpatialUnitFeatureIdValue(feature)) + " and NAME : " + str(getSpatialUnitFeatureNameValue(feature)))
        setIndicatorValue_asNoData(feature, targetDate)

    targetDateWithPrefix = getTargetDateWithPropertyPrefix(targetDate)

    feature["properties"][targetDateWithPrefix] = value

    return feature

def setIndicatorValue_asNoData(feature, targetDate):
    """Set the 'feature''s indicator value for the specified  'targetDate' s so-called 'NoData Values', i.e. as 'None'. I.e. if there are data protection mechanisms
    that mark a certain feature's indicator value as too low, then the value must be set as NoData. Or another reason could be, that when performing spatial analysis, certain Features
    simply do not contain the queried elements. To distuinguish between features whose indicator value is actually 0, one might set the value as 'None'. Which can be very important when average-aggregating
    indicaors from lower spatial units to upper spatial units, as 'None' means somenhing different than 0.

    Args:
        feature (Feature): a valid GeoJSON Feature
        targetDate (string): string representing the target date for which the indicator value shall be set, following the pattern 'YYYY-MM-DD', e.g. '2018-01-01'

    Returns:
        Feature: returns the GeoJSON Feature
    """
    targetDateWithPrefix = getTargetDateWithPropertyPrefix(targetDate)

    # None as NoData Value in Pyton 
    feature["properties"][targetDateWithPrefix] = None

    return feature

def setIndicatorValues_fromIdValueDict(targetFeatureCollection, targetDate, indicatorIdValueDict):
    """Set the 'feature''s indicator value for all features of the  'targetFeatureCollection' for the specified 'targetDate' with the respective indicator value from the input 'indicatorIdValueMap'.

    Args:
        targetFeatureCollection (FeatureCollection): a valid GeoJSON FeatureCollection containing all target features   
        targetDate (string): string representing the target date for which the indicator value shall be set, following the pattern 'YYYY-MM-DD', e.g. '2018-01-01'
        indicatorIdValueDict (dict): a dict of indicator features (key=featureId, value=indicatorValue) whose values shall be set as the respective target features indicator value for the specified 'targetDate'

    Returns:
        FeatureCollection  : returns the GeoJSON FeatureCollection
    """
    for feature in targetFeatureCollection["features"]:
        featureId = getSpatialUnitFeatureIdValue(feature)

        if featureId in indicatorIdValueDict and not isNoDataValue(indicatorIdValueDict[featureId]) and not math.isnan(indicatorIdValueDict[featureId]):
            feature = setIndicatorValue(feature, targetDate, indicatorIdValueDict[featureId])
        else:
            feature = setIndicatorValue_asNoData(feature, targetDate)

    return targetFeatureCollection

def indicatorValueIsNoDataValue(feature, targetDate):
    """Checks whether the features indicator value for the specified 'targetDate' is a nodata value

    Args:
        feature (Feature): a valid GeoJSON Feature
        targetDate (string): string representing the target date for which the indicator value shall be set, following the pattern 'YYYY-MM-DD', e.g. '2018-01-01'

    Returns:
        bool: returns 'True' if indicator value is NoData value
    """
    targetDateWithPrefix = getTargetDateWithPropertyPrefix(targetDate)

    value = feature["properties"][targetDateWithPrefix]

    return isNoDataValue(value)

def isNoDataValue(value):
    """Checks wheter the value is a NoData value

    Args:
        value (Object): the Value object to be inspected

    Returns:
        bool: returns 'True' if the value is a NoData Value (i. e. 'None', 'NaN')
    """
    try: 
        if math.isnan(float(value)) or value == None:
            return True
        else:
            return False
    except TypeError:
        return True


def getTargetDateWithPropertyPrefix(targetDate):
    """Concatenates indicator date property prefix and submitted targetDate.
    I.e, for exemplar targetDate="2018-01-01" it produces targetDateWithPrefix="DATE_2018-01-01".
    This is necessary in order to query timeseries property values from an indicator feature.
 
    indicatorFeature.properties[targetDate] --> null
    indicatorFeature.properties[targetDateWithPrefix] --> indicator value, (if timestamp is present)

    Args:
        targetDate (string): string representing the target date for which the indicator shall be computed, following the pattern 'YYYY-MM-DD', e.g. '2018-01-01'

    Returns:
        string: the targetDate string with the additional prefix
    """
    if indicator_date_prefix in targetDate:
        return targetDate
    else:
        return indicator_date_prefix + targetDate

def asFeature(geometry):
    """creates a GeoJSON Feature from a sumitted Geometry. The geojson Module provides the required Feature. 

    Args:
        geometry (geometry): a GeoJSON Geometry consisting of an attribute and a Geometry

    Returns:
        Feature: a GeoJSON Feature wrapping the submitted geometry and the attributes together
    """
    return geojson.Feature(id=None, geometry=geometry)

def asFeatureCollection(features):
    """creates a GeoJSON FeatureCollection from the submitted Array of Features, using the GeoJSON FeatureCollection class.

    Args:
        features (Array<Feature>): an array of GeoJSON Feature to unite in a single FeatureCollection

    Returns:
        FeatureCollection: a GeoJSON FeatureCollection containing all the submitted Features.
    """
    return geojson.FeatureCollection(features) 

def hasMultiLineString(featureCollection):
    """Inspects the submitted GeoJSON FeatureCollection for any features of type 'MultiLineString'

    Args:
        featureCollection (FeatureCollection): a valid GeoJSON FeatureCollection

    Returns:
        Bool: returns 'True' if the featurecollection contains any features of type 'MultiLineString', otherwise returns 'False'
    """
    for feature in featureCollection["features"]:
        if feature["geometry"]["type"] == "MultiLineString":
            return True
    return False

# This function should not be necessary, the function 'transformMultiLineStringsToLineStrings' does all necessary things to eliminate all MulitLineStrings in a submitted FeatureCollection
# def replaceMultiLineStringsByLineStrings(featureCollection):
#     """Replaces any feature of type 'MultiLineString' of the submitted featureCollection by the individual features of type 'LineString'.

#     Args:
#         featureCollection (FeatureCollection<LineString|MultiLineString>): valid GeoJSON FeatureCollection with line geometries (MultiLineStrings will be replaced by multiple lines).

#     Returns:
#         FeatureCollection<LineString>: the GeoJSON FeatureCollection where features of type 'MultiLineString' have been replaced by multiple features of type 'LineString'.
#     """
#     gdf = geoJSONtoGDF(featureCollection)
#     gdf = gdf.explode(index_parts=False)

#     featureOut = geojson.loads(gdf.to_json(drop_id=True))
#     return featureOut

def transformMultiLineStringToLineStrings(featureCollection):
    """Replaces any feature of type 'MultiLineString' of the submitted featureCollection by the individual features of type 'LineString'.

    Args:
        featureCollection (FeatureCollection<LineString|MultiLineString>): valid GeoJSON FeatureCollection with line geometries (MultiLineStrings will be replaced by multiple lines).

    Returns:
        FeatureCollection<LineString>: the GeoJSON FeatureCollection where features of type 'MultiLineString' have been replaced by multiple features of type 'LineString'.
    """
    gdf = geoJSONtoGDF(featureCollection)
    gdf = gdf.explode(index_parts=False)

    featureOut = geojson.loads(gdf.to_json(drop_id=True))
    return featureOut
        
def hasMultiPolygon(featureCollection):
    """Inspects the submitted GeoJSON FeatureCollection for any features of type 'MultiPolygon'

    Args:
        featureCollection (FeatureCollection): a valid GeoJSON FeatureCollection

    Returns:
        Bool: returns 'True' if the featurecollection contains any features of type 'MultiPolygon', otherwise returns 'False'
    """
    for feature in featureCollection["features"]:
        if feature["geometry"]["type"] == "MultiPolygon":
            return True
    return False

def transformMultiPolygonsToPolygons(featureCollection):
    """Replaces any feature of type 'MultiPolygon' of the submitted featureCollection by the individual features of type 'Polygon'.

    Args:
        featureCollection (FeatureCollection<Polygon|MultiPolygon>): valid GeoJSON FeatureCollection with line geometries (MultiPolygons will be replaced by multiple lines).

    Returns:
        FeatureCollection<Polygon>: the GeoJSON FeatureCollection where features of type 'MultiPolygon' have been replaced by multiple features of type 'Polygon'.
    """
    gdf = geoJSONtoGDF(featureCollection)
    gdf = gdf.explode(index_parts=False)

    featureOut = geojson.loads(gdf.to_json(drop_id=True))
    return featureOut
    
# def replaceMultiPolygonsByPolygons():
#     # this function is not required (see LineStrings)
#     return None

#############################################################################################################################################
# API_HELPER_METHODS_UTILITY   --   with the special purpose to reduce content in the computation scripts at 'KomMonitor-Script-Ressources' #  
#############################################################################################################################################
def bool_filterValue_byOperator(currentValue: str, computationFilterOperator: str, computationFilterValue: str):
    """Encapsulates different filter operations on two submitted values. The filter method has to be submitted in a string format which is getting checked.

    Args:
        currentValue (str): the value from the timeline which is getting compared to a static compare value
        computationFilterOperator (str): the filter operator in a string format (for allowed operators compare with GUI)
        computationFilterValue (str): the static filter value

    Raises:
        ValueError: if an invalid filter operator is submitted

    Returns:
        Bool: returns bool if the currentValue fits to the filter operator or false if it doesnt
    """
    currentValue = float(currentValue)
    
    if computationFilterOperator == "Equal":
        return currentValue == float(computationFilterValue)
    elif computationFilterOperator == "Unequal":
        return currentValue != float(computationFilterValue)
    elif computationFilterOperator == "Greater_than":
        return currentValue > float(computationFilterValue)
    elif computationFilterOperator == "Less_than":
        return currentValue < float(computationFilterValue)
    elif computationFilterOperator == "Greater_than_or_equal":
        return currentValue >= float(computationFilterValue)
    elif computationFilterOperator == "Less_than_or_equal":
        return currentValue <= float(computationFilterValue)
    elif computationFilterOperator == "Contains":
        computationFilterPropertyValueArray = computationFilterValue.split(",")
        
        for trimmed_element in (element.strip() for element in computationFilterPropertyValueArray):
            if float(trimmed_element) == currentValue:
                return True
        
        return False
    elif computationFilterOperator == "Range":
        value = int(currentValue)
        computationFilterPropertyValueArray = computationFilterValue.split("-")
        computationFilterPropertyValueArray = map(lambda x: int(x), computationFilterPropertyValueArray)

        return currentValue >= computationFilterPropertyValueArray[0] and currentValue < computationFilterPropertyValueArray[1]
     
    else:
        raise ValueError(f"Ungültiger computationFilterOperator: {computationFilterOperator}")
    

def applyComputationFilter_onFeatureCollection(featureCollection, propertyName: str, computationFilterOperator: str, computationFilterPropertyValue: str):
    """takes a geojson feature collection and removes all features that do not fulfill a filter operation based on a filterValue and filter operator

    Args:
        featureCollection (dict): a valid geojson feature collection
        propertyName (str): the string name of a property which contains the values used for filtering
        computationFilterOperator (str): the filter operator
        computationFilterPropertyValue (str): the static filter value where the property values of the feature collection are compared to

    Returns:
        dict: returns a geojson featurecollection with only features fitting to the filter operator
    """
    result_collection = copy.deepcopy(featureCollection)
    del result_collection["features"]
    result_collection["features"] = []

    for feature in featureCollection["features"]:
        if bool_filterValue_byOperator(feature["properties"][propertyName], computationFilterOperator, computationFilterPropertyValue):
            result_collection["features"].append(feature)
    
    return result_collection

def applyComputationFilter_onValueArray(valueArray, computationFilterOperator, computationFilterPropertyValue):
    """applys a computation filter to a submitted value array and returns the filtered Array. Several filter operators are valid.

    Args:
        valueArray (Array): the array for which the filter shall be applied
        computationFilterOperator (string): the operator which shall be used to filter the array. Valid entrys are Equal, Greater_than, Greater_than_or_equal, Less_than, Less_than_or_equal, Unequal, Contains, Range
        computationFilterPropertyValue (string): the filter value

    Returns:
        Array | None: returns the filtered Array or None if the wrong computation filter is used. None value has to be handeld separately in the script.
    """
    filteredArray = []    

    if computationFilterOperator == "Equal":
        filteredArray = filter(lambda x: x == computationFilterPropertyValue, valueArray)
    elif computationFilterOperator == "Greater_than":
        filteredArray = filter(lambda x: x > computationFilterPropertyValue, valueArray)
    elif computationFilterOperator == "Greater_than_or_equal":
        filteredArray = filter(lambda x: x >= computationFilterPropertyValue, valueArray)
    elif computationFilterOperator == "Less_than":
        filteredArray = filter(lambda x: x < computationFilterPropertyValue, valueArray)
    elif computationFilterOperator == "Less_than_or_equal":
        filteredArray = filter(lambda x: x <= computationFilterPropertyValue, valueArray)
    elif computationFilterOperator == "Unequal":
        filteredArray = filter(lambda x: x != computationFilterPropertyValue, valueArray)
    elif computationFilterOperator == "Contains":
        computationFilterPropertyValueArray = computationFilterPropertyValue.split(",")
        
        for trimmed_element in (element.strip() for element in computationFilterPropertyValueArray):
            tmp = [item for item in valueArray if item == trimmed_element]
            filteredArray.extend(tmp)
    elif computationFilterOperator == "Range":
        computationFilterPropertyValueArray = computationFilterPropertyValue.split("-")
        computationFilterPropertyValueArray = map(lambda x: int(x), computationFilterPropertyValueArray)

        filteredArray = filter(lambda x: x >= computationFilterPropertyValueArray[0] and x < computationFilterPropertyValueArray[1])
    else:
        return None

    return filteredArray    

def applyComputationMethod(valueArray, computationMethod):
    """applys a computation method to a submitted value array and sets the features indicator value to the computed value.

    Args:
        valueArray (Array): the array which is used for computation of the value
        computationMethod (string): the method used to compute the value (i.e. sum, min, mean ...) 
    """
    if computationMethod == "SUM":
        value = sum(valueArray)
        return float(value)
    elif computationMethod == "MIN":
        value = min(valueArray)
        return float(value)
    elif computationMethod == "MAX":
        value = max(valueArray)
        return float(value)
    elif computationMethod == "MEAN":
        value = mean(valueArray)
        return float(value)
    elif computationMethod == "MEDIAN":
        value = median(valueArray)
        return float(value)
    elif computationMethod == "STANDARD_DEVIATION":
        value = standardDeviation(valueArray, True)
        return float(value)
    else:
        throwError("Indicator was not computed from computation ressources because no valid computation method was chosen. Indicator value is set to None.")

def filter_feature_lifespan(feature_collection, targetDate: str):
    """Applys a filter on a feature collection. Therefore it gets checked, whether a specified "targetDate" is included in the lifespan of each feature of the collection.

    Args:
        feature_collection (FeatureCollection): a valid GeoJSON Feature Collection with a number of features the shall be filtered
        targetDate (str): a date in the form 'YYYY-MM-DD' which should be inside the features lifespan

    Returns:
        FeatureCollection: returns the FeatureCollection where all features are valid for the submitted targetDate
    """
    targetDate = formatStringAsDate(targetDate)

    result_collection = copy.deepcopy(feature_collection)
    del result_collection["features"]
    result_collection["features"] = []

    for feature in feature_collection["features"]:
        startDate = formatStringAsDate(feature["properties"]["validStartDate"])
        if "validEndDate" in feature["properties"]:
            endDate = formatStringAsDate(feature["properties"]["validEndDate"])
        else: 
            endDate = datetime.date.today()

        if startDate <= targetDate <= endDate:
            result_collection["features"].append(feature)

    if len(result_collection["features"]) == 0 and len(feature_collection["features"]) > 0:
        throwError(f"None of the features has a lifespan which contains the requested date: {targetDate}")

    return result_collection
    
# Classes designed for use in km-script-resources
# class ProcessingError:
#     resource_type: str
#     dataset_id: str
#     affectedTimestamps: list
#     affectedSpatialUnitFeatures: list
#     errorMessage: str    
    
# class ProcessingErrorList:
#     errorList: list[ProcessingError]    
    
#     def __init__(self):
#         self.errorList = []

    
class IndicatorCalculationType(str, Enum):
    """This class represents an enum which defines allowed indicator types

    Args:
        str (str): the type of the indicator
        Enum (_type_): _description_
    """
    TARGET_INDICATOR = "TARGET_INDICATOR"
    COMPUTATION_INDICATOR = "COMPUTATION_INDICATOR"
    BASE_INDICATOR = "BASE_INDICATOR"
    REFERENCE_INDICATOR = "REFERENCE_INDICATOR"
    NUMERATOR_INDICATOR = "NUMERATOR_INDICATOR"
    DENOMINATOR_INDICATOR = "DENOMINATOR_INDICATOR"

class IndicatorType:
    id: str
    type: IndicatorCalculationType
    meta: Optional[IndicatorOverviewType]
    values: Optional[list]
    bool_missing_timestamp: bool
    missing_timestamps: list
    applicable_su: list
    time_series: dict[dict]
    applicable_su_features: list

    def __init__(self, id : str, type : IndicatorCalculationType):
        """creates an IndicatorType object which stores all Data that belongs to the indicator

        Args:
            id (str): the unique indicator id 
            type (IndicatorCalculationType): the type of the indicator
        """
        self.id = id
        self.type = type
        self.bool_missing_timestamp = False
        self.time_series = {}
        self.missing_timestamps = []
        self.applicable_su = []
        self.applicable_su_features = []
    
    def check_su_allowedRoles(self, spatialUnit: str):
        """checks whether an indicator contains allowedRoles for an explicit spatial unit, if not the allowedRoles of the indicator itself are used

        Args:
            spatialUnit (str): the id of the spatial unit

        Returns:
            str: returns the allowedRoles of the indicator and spatial unit
        """
        for su in self.meta.applicable_spatial_units:
            if su.spatial_unit_id == spatialUnit and len(su.allowed_roles) > 0:
                return su.allowed_roles
    
        return self.meta.allowed_roles
    
    def get_indicator_by_id(self, indicator_controller: IndicatorsControllerApi):
        """encapsulates the equal named function from the data management api in order to raise a data management exception which allows to catch this error clearly

        Args:
            indicator_controller (IndicatorsControllerApi): the openapi module which provides the functionality

        Raises:
            DataManagementException: cath the datamanagementapierror correctly
        """
        try:
            self.meta = indicator_controller.get_indicator_by_id(self.id)
        except (ForbiddenException, ApiException) as e:
            raise DataManagementException(e, self.id, "INDICATOR", e.status)
        
    def get_indicator_by_spatial_unit_id_and_id_without_geometry(self, indicators_controller: IndicatorsControllerApi, spatial_unit: str):
        """encapsulates the equal named function from the data management api in order to raise a data management exception which allows to catch this error clearly

        Args:
            indicators_controller (IndicatorsControllerApi): _description_
            spatial_unit (str): the spatial unit id which shall be queried

        Raises:
            DataManagementException: catch the datamanagementapierror correctly
        """
        try:
            self.values = indicators_controller.get_indicator_by_spatial_unit_id_and_id_without_geometry(
                            self.id, 
                            spatial_unit)
        except (ForbiddenException, ApiException) as e:
            raise DataManagementException(e, self.id, "INDICATOR", e.status, spatial_unit) 
        
class IndicatorCollection:
    indicators: dict[str, IndicatorType]
    intersection_su_features: list
    intersection_target_dates: set
    all_target_dates: list
    all_su_features: list

    def __init__(self):
        """create a collection which provides more functionality to the indicators
        """
        self.indicators = {}
        self.intersection_su_features = []
        self.all_target_dates = []
    
    def add_indicator(self, indicator: IndicatorType):
        """add an indicator to the collection

        Args:
            indicator (IndicatorType): the indicator which will be added
        """
        self.indicators[indicator.id] = indicator

    def fetch_all_spatial_unit_features(self, spatial_unit_controller, spatial_unit: str):
        # query data-management-api to get all spatial unit features for the current spatial unit.
        # store the list containing all features-IDs as an attribute for the collection
        self.all_su_features = fetch_spatial_unit_features(spatial_unit_controller, spatial_unit)


    def find_intersection_target_dates_from_meta(self):
        """finds all targetDates the are available in every indicator and also all targetDates that exist in every indicator
        """
        listApplicableDates = [] 

        for item in self.indicators:
            listApplicableDates.append(set(self.indicators[item].meta.applicable_dates))
        
        intersection = listApplicableDates[0].copy()
        union = listApplicableDates[0].copy()
        for dates in listApplicableDates[1:]:
            intersection.intersection_update(dates)
            union = union | dates

        self.intersection_target_dates = intersection
        self.all_target_dates = list(union)

    
    def find_intersection_target_dates_from_values(self) -> None:
        # TODO
        return None
    
    def find_intersection_applicable_su_features(self) -> list:
        """finds all suFeatures that exist for every indicator
        """
        listApplicableSuFeatures = [] 

        for item in self.indicators:
            listApplicableSuFeatures.append(set(self.indicators[item].applicable_su_features))
        
        intersection = listApplicableSuFeatures[0].copy()
        # union = listApplicableSuFeatures[0].copy()
        for su_features in listApplicableSuFeatures[1:]:
            intersection.intersection_update(su_features)
            # union = union | su_features

        self.intersection_su_features = intersection
        # self.all_su_features = union

    def check_applicable_spatial_units(self, spatial_unit: str, job_summary: KommonitorJobSummary):
        """checks whether spatial units are missing for certain indicators and in this case adds a missingSpatialUnitError to the jobsummary

        Args:
            spatial_unit (str): id of the spatial unit
            job_summary (KommonitorJobSummary): the current kommmonitor jobSummary for spatial_unit
        """
        for indicator in self.indicators:
            for unit in self.indicators[indicator].meta.applicable_spatial_units:
                self.indicators[indicator].applicable_su.append(unit.spatial_unit_id)

            if not spatial_unit in self.indicators[indicator].applicable_su:
                job_summary.add_missing_spatial_unit_error(indicator)

    def check_applicable_target_dates(self, job_summary: KommonitorJobSummary):
        """checks whether targetDates are missing for certain indicators and in this case adds a missing timestamp error to the jobSummary

        Args:
            job_summary (KommonitorJobSummary): the current kommonitor jobSummary
        """
        # catch missing timestamp error
        for indicator in self.indicators:
            if self.indicators[indicator].bool_missing_timestamp:
                job_summary.add_missing_timestamp_error("INDICATOR", indicator, self.indicators[indicator].missing_timestamps)

    def check_applicable_spatial_unit_features(self, job_summary: KommonitorJobSummary):
        """checks whether spatial unit features are missing for certain indicators and in this case adds a missing timestamp error to the jobSummary

        Args:
            job_summary (KommonitorJobSummary): the current kommonitor jobSummary
        """
        for indicator in self.indicators:
            missing_su_features = []
            for feature in self.all_su_features:
                if not feature in self.indicators[indicator].applicable_su_features:
                    missing_su_features.append(feature)

            if len(missing_su_features) > 0:
                job_summary.add_missing_spatial_unit_feature_error(indicator, missing_su_features)

    def fetch_indicator_feature_time_series(self):
        """creates a time series which allows direct access to the data using indicator id and su feature id and target date
        """
        for indicator in self.indicators:
            su_features = []
            for feature in self.indicators[indicator].values:
                id = feature["ID"]
                self.indicators[indicator].time_series[id] = feature
                su_features.append(id)

            self.indicators[indicator].applicable_su_features = su_features

        self.intersection_su_features = self.find_intersection_applicable_su_features()

def get_all_spatial_unit_features_by_id_without_preload_content(spatial_unit_controller: SpatialUnitsControllerApi, spatial_unit: str):
    """encapsulates the function from data management api to query a valid geojson feature collection from database due to an exception an error gets reported

    Args:
        spatial_unit_controller (SpatialUnitsControllerApi): the spatial unit controller from openapi client
        spatial_unit (str): the spatial unit id

    Raises:
        DataManagementException: raises exception to catch datamanagementapierror

    Returns:
        dict: returns a valid geojson featurecollection containing the spatial unit
    """
    try:
        # query data-management-api to get all spatial unit features for the current spatial unit.
        response_data = spatial_unit_controller.get_all_spatial_unit_features_by_id_without_preload_content(spatial_unit)
        su_feature_collection = json.loads(response_data.data)
        
        return su_feature_collection
    except (ForbiddenException, ApiException) as e:
        raise DataManagementException(e, spatial_unit, "SPATIAL_UNIT", e.status, spatial_unit) 
        
def get_all_georesource_features_by_id_without_preload_content(georesource_controller: GeorecourcesControllerApi, georesource: str):
    """encapsulates the function from data management api to query a valid geojson feature collection from database due to an exception an error gets reported

    Args:
        georesource_controller (GeorecourcesControllerApi): the georecource controller from openapi client
        georesource (str): the georesource id

    Raises:
        DataManagementException: raises exception to catch datamanagementapierror

    Returns:
        dict: returns a valid geojson featurecollection containing the georesource dataset
    """
    try:
        # fetch the georesource feature collection
        georesource = georesource_controller.get_all_georesource_features_by_id_without_preload_content(georesource)
        georesource_collection = json.loads(georesource.data)

        return georesource_collection
    except (ForbiddenException, ApiException) as e:
        raise DataManagementException(e, georesource, "SPATIAL_UNIT", e.status) 
    

def fetch_spatial_unit_features(spatial_unit_controller: SpatialUnitsControllerApi, spatial_unit: str):
    """Queries the data management api using the spatial unit controller. The API response gets parsed into correct json to extract all spatial unit features that belong to the requested spatial unit.

    Args:
        spatial_unit_controller (SpatialUnitControllerApi): the openapi client for querying spatial unit data
        spatial_unit (str): the string ID which identifies the spatial unit

    Returns:
        List: returns a list containing all spatial unit features which belong to the spatial unit
    """
    try:
        response_data = spatial_unit_controller.get_all_spatial_unit_features_by_id_without_preload_content(spatial_unit)
        geojson_all_features = json.loads(response_data.data)

        all_su_features = [feature["properties"]["ID"] for feature in geojson_all_features["features"]]

        return all_su_features
    except (ForbiddenException, ApiException) as e:
        raise DataManagementException(e, spatial_unit, "SPATIAL_UNIT", e.status, spatial_unit) 
        

def getTargetDate_without_prefix(dateWithPrefix: str):
    """Removes the date prefix from a submitted date string

    Args:
        dateWithPrefix (str): the target date with 'DATE_' prefix

    Returns:
        string: returns the date without 'DATE_'
    """
    if indicator_date_prefix in dateWithPrefix:
        return dateWithPrefix[5:15]
    elif len(dateWithPrefix) == 10:
        return dateWithPrefix

def getAll_target_time(targetTimeDict, target_applicable_dates: set, all_input_applicable_dates: list):
    """returns all applicable target dates for the target indicator and all computation indicators, based on the the applicable target dates from indicator metadata

    Args:
        targetTimeDict (dict): the dictionary containing the target times according to kommonitors schema
        target_applicable_dates (set): applicable dates of target indicator, typically from metadata
        all_input_applicable_dates (list): a list containing sets of applicable dates for all computation indicators

    Returns:
        list: returns a list containing all applicable dates for all indicators
    """      
    computeDates = []

    if targetTimeDict["mode"] == "ALL":
        # get all dates that exist in every input indicator
        allDates = all_input_applicable_dates[0].copy()
        for input_applicable_dates in all_input_applicable_dates:
            allDates.intersection_update(input_applicable_dates)

        # remove excluded Dates 
        for date in allDates:
            if not date in targetTimeDict["excludeDates"]:
                computeDates.append(date)
 
    elif targetTimeDict["mode"] == "DATES":
        # get all dates that exist in every input indicator
        allDates = all_input_applicable_dates[0].copy()
        for input_applicable_dates in all_input_applicable_dates:
            allDates.intersection_update(input_applicable_dates)
        
        # add needed dates to list
        for date in allDates:
            if date in targetTimeDict["includeDates"]:
                computeDates.append(date)
    
    elif targetTimeDict["mode"] == "MISSING":
        # get all dates that exist in every input indicator
        allDates = all_input_applicable_dates[0].copy()
        for input_applicable_dates in all_input_applicable_dates:
            allDates.intersection_update(input_applicable_dates)
        
        # compare existing target indicator dates with applicable dates of inputs
        for date in allDates:
            if not date in target_applicable_dates and not date in targetTimeDict["excludeDates"]:
                computeDates.append(date)
    
    return computeDates

def getAll_target_time_from_indicator_collection(target_indicator: IndicatorType, 
                                                collection: IndicatorCollection, 
                                                target_time_dict: dict) -> Tuple[bool, list]:
    """returns all applicable target dates for the target indicator and all computation indicators, based on the the applicable target dates from the time series

    Args:
        targetTimeDict (dict): the dictionary containing the target times according to kommonitors schema
        collection (IndicatorCollection): the indicator collection
        target_indicator (IndicatorType): the target indicator which is a single indicator type

    Returns:
        Bool: returns true if timestamps are missing
        list: returns the list of the computation dates
    """
    collection.find_intersection_target_dates_from_meta()
    intersectionDates = collection.intersection_target_dates
    computeDates = []
    missing_timestamps = False

    if target_time_dict["mode"] == "ALL":
        # remove excluded Dates 
        for date in intersectionDates:
            if not date in target_time_dict["excludeDates"]:
                computeDates.append(date)

        # add missing timestamp informations to indicator collection
        for indicator in collection.indicators:
            for date in collection.all_target_dates:
                if not date in collection.indicators[indicator].meta.applicable_dates and not date in target_time_dict["excludeDates"]:
                    missing_timestamps = True
                    collection.indicators[indicator].bool_missing_timestamp = True
                    collection.indicators[indicator].missing_timestamps.append(date)

    elif target_time_dict["mode"] == "DATES":
        # add needed dates to list
        for date in intersectionDates:
            if date in target_time_dict["includeDates"]:
                computeDates.append(date)

        # add missing timestamp informations to indicator collection
        for indicator in collection.indicators:
            for date in target_time_dict["includeDates"] :
                if not date in collection.indicators[indicator].meta.applicable_dates:
                    missing_timestamps = True
                    collection.indicators[indicator].bool_missing_timestamp = True
                    collection.indicators[indicator].missing_timestamps.append(date)


    elif target_time_dict["mode"] == "MISSING":
        # compare existing target indicator dates with applicable dates of inputs
        for date in intersectionDates:
            if not date in target_indicator.meta.applicable_dates and not date in target_time_dict["excludeDates"]:
                computeDates.append(date)

        # add missing timestamp informations to indicator collection
        for indicator in collection.indicators:
            for date in collection.all_target_dates:
                if not date in collection.indicators[indicator].meta.applicable_dates and not date in target_indicator.meta.applicable_dates and not date in target_time_dict["excludeDates"]:
                    missing_timestamps = True
                    collection.indicators[indicator].bool_missing_timestamp = True
                    collection.indicators[indicator].missing_timestamps.append(date)

    return missing_timestamps, computeDates
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""                                                                                                                 ""
""                    API_HELPER_METHODS_GEOMETRIC_OPERATIONS                                                      ""
""                                                                                                                 ""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""




def geoJSONtoGDF(geoJSON):
    """writes the submitted GeoJSON 'Feature' or 'FeatureCollection' to a GeoPandas GeoDataFrame.

    Args:
        geojson (Feature|FeatureCollection): must be a correct feature or featureCollection

    Returns:
        GeoDataFrame: returns a GeoDataFrame containing a row with properties and geometry for every submitted Feature.
    """
    try:
        if isGeoJSONFeature(geoJSON):
            gdf = gpd.GeoDataFrame.from_features([geoJSON])
            return gdf
        elif isGeoJSONFeatureCollection(geoJSON):
            gdf = gpd.GeoDataFrame.from_features(geoJSON)
            return gdf
        elif bool(geoJSON["coordinates"]):
            feature = asFeature(geoJSON)
            gdf = gpd.GeoDataFrame.from_features([feature])
            return gdf
    except:
            throwError("Something is wrong with your submitted GeoJSON, whether it is a correct Feature nor is it a correct FeatureCollection")

def geom2Feature(geom):
    """transforms a GeoSeries like geometry into a GeoJSON Feature.

    Args:
        geom (GeoSeries): an Object of type GeoSeries with the properties 'is_empty' and 'geom_type'

    Returns:
        Feature: returns a GeoJSON Feature of the correct type
    """
    try:
        if geom.is_empty == "True":
            return None    
        elif geom.geom_type == "Point":
            return geojson.Feature(id=None, geometry=shapely.Point(geom))
        elif geom.geom_type == "LineString":
            return geojson.Feature(id=None, geometry=shapely.LineString(geom))
        elif geom.geom_type == "Polygon":
            return geojson.Feature(id=None, geometry=shapely.Polygon(geom))
        elif geom.geom_type == "Multipoint":
            return geojson.Feature(id=None, geometry=shapely.MultiPoint(geom))
        elif geom.geom_type == "MultiLineString":
            return geojson.Feature(id=None, geometry=shapely.MultiLineString(geom))
        elif geom.geom_type == "MultiPolygon":
            return geojson.Feature(id=None, geometry=shapely.MultiPolygon(geom))
    except:
        throwError("An Error occured in function 'geom2Feature'! The geom from which the feature shall be created is none of type (Point, Linestring, Polygon, MultiPoint, MultiLineString, MultiPolygon)")

def area(geoJSON):
    """Encapsulated geopandas function 'area' to compute the area of the submitted Features in square meters

    Args:
        geoJSON (GeoJSON): a valid geojson Object like a 'Feature' or a 'FeatureCollection' with polygonal geometries, non polygonal geometries have as result an area of 0m²

    Returns:
        array<float>: returns an array containing the area from all submitted features 
    """
    gdf = geoJSONtoGDF(geoJSON)
    return gdf.area[0]

def area_feature_asProperty(feature):
    """Compute the area of the submitted Feature in square meters and append it as a new property named 'area_SquareMeters'

    Args:
        feature (Feature<Polygon>): a valid and single GeoJSON Feature with a polygonal geometry

    Returns:
        Feature: returns the submitted Feature with the new Property 'area_SquareMeters' and its calculated value
    """
    if isGeoJSONPolygonFeature(feature):
        gdf = geoJSONtoGDF(feature)
        feature["properties"]["area_SquareMeters"] = gdf.area[0]
        return feature
    else:
        throwError("input Feature is no Polygon Feature!")

def area_featureCollection_asProperty(featureCollection):    
    """Computes the area in square meters (m²) of each feature of the submitted 'featureCollection_geoJSON' as new property 'area_SquareMeters'

    Args:
        featureCollection (FeatureCollection): a valid FeatureCollection containing polygonal features, none polygonal Features a skipped

    Returns:
        FeatureCollection: returns the submitted FeatureCollection with an additional property 'area_SquareMeters' in all polygonal Features
    """
    for feature in featureCollection["features"]:
        try:
            area_feature_asProperty(feature)
        except Exception as error:
            print("Input feature is no valid Feature with polygonal geometry! Continue with next feature of the FeatureCollection")
            continue
    return featureCollection

def bbox_feature(feature):
    """encapsulates the Geopandas function 'envelope' to compute the bounding box of a submitted single Feature

    Args:
        feature (Feature):  a single GeoJSON feature consisting of geometry and properties, for whom the bounding box shall be computed

    Returns:
        Feature: the GeoJSON feature whose geometry has been replaced by the bounding box geometry an contains all properties of the original Feature
    """
    gdf = geoJSONtoGDF(feature)
    gdf.loc[0, "geometry"] = gdf.envelope[0]
    featureOut = geojson.loads(gdf.to_json(drop_id=True))
    return featureOut["features"][0]

def bbox_featureCollection(featureCollection):
    """Computes the bounding boxes of all features of the submitted 'FeatureCollection'

    Args:
        featureCollection (FeatureCollection):  a GeoJSON FeatureCollection consisting of multiple features, for whom the bounding box shall be computed

    Returns:
        FeatureCollection: the GeoJSON features whose geometry has been replaced by the bounding box geometry as GeoJSON FeatureCollection.
        The resulting features contain all properties of the original features.
    """
    newFeatures = []
    for feature in featureCollection["features"]:
        newFeatures.append(bbox_feature(feature))
    return asFeatureCollection(newFeatures)

def buffer_feature(feature, radiusInMeters):
    """Encapsulates Geopandas buffer function to compute the buffered geometry of a single submitted feature.

    Args:
        feature (Feature): a single GeoJSON Feature consisting of geometry and properties, for whom the buffer shall be computed
        radiusInMeters (Number): the buffer radius in Meters

    Returns:
        Feature<Polygon>: the GeoJSON feature whose geometry has been replaced by the buffered geometry of type 'Polygon'.
        The resulting feature contains all properties of the original feature
    """
    gdf = geoJSONtoGDF(feature)
    gdf.loc[0, "geometry"] = gdf.buffer(radiusInMeters)[0]
    featureOut = geojson.loads(gdf.to_json(drop_id=True))
    return featureOut["features"][0]

def buffer_featureCollection(featureCollection, radiusInMeters):
    """Computes the buffered geometries of all features of the submitted 'FeatureCollection'.

    Args:
        featureCollection (FeatureCollection): a GeoJSON FeatureCollection consisting of multiple features, for whom the buffers shall be computed
        radiusInMeters (Number): the buffer radius in meters

    Returns:
        FeatureCollection<Polygon>: the GeoJSON features whose geometry has been replaced by the buffered geometry of type 'Polygon' as GeoJSON FeatureCollection.
        The resulting features contain all properties of the original features.
    """
    newFeatures = []
    for feature in featureCollection["features"]:
        newFeatures.append(buffer_feature(feature, radiusInMeters))
    return asFeatureCollection(newFeatures)

def center_usingBBOX(geoJSON):
    """Computes the center of a submitted FeatureCollection. For that the BBOX of all submitted Features gets determined and its center gets computed.  

    Args:
        geoJSON (GeoJSON): a valid GeoJSON geometry (i.e. Feature or FeatureCollection)

    Returns:
        Feature: returns a Feature containing the geometry of the center point and a property 'type':'Geometric Center'
    """
    gdf = geoJSONtoGDF(geoJSON)
    box = shapely.box(*gdf.total_bounds)
    center = shapely.centroid(box)
    featureOut = geojson.Feature(id=None, geometry=shapely.Point(center),properties={'type':'Geometric Center'})
    return featureOut

def center_representative(geoJSON):
    """Computes a representative Point which is safely inside a submitted Polygon. Its most likely the center of a geometry but for the exact geometric centroid use function 'centroid'. 

    Args:
        geoJSON (GeoJSON): a valid GeoJSON Geometry (i.e. Feature) containing a polygonal Geomtry.

    Returns:
        Feature<Point>: returns a GeoJSON Feature containing the point geometry representing the most likely center inside a polygon.
    """
    gdf = geoJSONtoGDF(geoJSON)
    geom = gdf.representative_point()[0]
    return geom2Feature(geom)


def centroid(geoJSON):
    """Computes the centroid of a single submitted GeoJSON Geometry (i.e. Feature). Note that the Centroid of a geometry can also be outside of a polygon!

    Args:
        geoJSON (Feature): a single valid GeoJSON Geometry (i.e. Feature) containing the Polygon which centroid Point should get determined.

    Returns:
        Feature<Point>: returns a Feature containing the Point geometry representing the centroid.
    """
    gdf = geoJSONtoGDF(geoJSON)
    geom = gdf.centroid[0]
    return geom2Feature(geom)



def pointOnFeature(feature):
    """compute a point which is guaranteed on the submitted Feature. Encapsulates geopandas function 'sample_points'. The number of points on the feature is variabel.

    Args:
        feature (Feature): a valid GeoJSON Feature

    Returns:
        Feature<Point>: the GeoJSON Point Feature on the surface of the submitted Feature. The submitted feature propertys are kept.
    """
    gdf = geoJSONtoGDF(feature)
    gdf.loc[0, "geometry"] = gdf.sample_points(1)[0]
    featureOut = geojson.loads(gdf.to_json(drop_id=True))
    return featureOut["features"][0]

def contains(feature_A, feature_B):
    """Encapsulates geopandas function 'contains' to check if the submitted 'feature_A' contains the submitted 'feature_B'

    Args:
        feature_A (Feature): a valid GeoJSON Feature of any type
        feature_B (Feature): a valid GeoJSON Feature of any type

    Returns:
        Bool: returns 'True' if 'feature_A' contains 'feature_B'
    """
    gdfA = geoJSONtoGDF(feature_A)
    gdfB = geoJSONtoGDF(feature_B)
    return gdfA.contains(gdfB)[0]

def difference(polygonFeature_A, polygonFeature_B):
    """computes the difference between two polygonal GeoJSON Features using geopandas 'difference' function. 

    Args:
        polygonFeature_A (Feature<Polygon>): a GeoJSON Feature of type Polygon
        polygonFeature_B (_type_): _description_

    Returns:
        Feature<Polygon|Multipolygon>: returns a Feature containing a polygonal or muli-polygonal geometry representing the difference. If the difference is an empty geometry the feature contains a 'null' geometry.
    """
    gdfA = geoJSONtoGDF(polygonFeature_A)
    gdfB = geoJSONtoGDF(polygonFeature_B)
    out = gdfA.difference(gdfB)[0]
    return geom2Feature(out)
    
def dissolve(featureCollection, propertyName):
    """Dissolve polygonal Features. 

    Args:
        featureCollection (FeatureCollection<Polygon|MultiPolygon>): a valid GeoJSON FeatureCollection with polygonal or multipolygonal geometries.
        propertyName (string): Optional parameter that points to an existing attribute used by the features. If set, only features with the same attribute value will be dissolved.

    Returns:
        FeatureCollection<Polygon>: the GeoJSON FeatureCollection containing the dissolved features (Note that attributes are not merged/aggregated).
    """
    gdf = geoJSONtoGDF(featureCollection)
    
    if bool(propertyName):
        gdf = gdf.dissolve(propertyName)
    else:
        gdf = gdf.dissolve()
    
    featureCollectionOut = geojson.loads(gdf.to_json(drop_id=True))
    return featureCollectionOut

def disjoint(feature_A, feature_B):
    """Checks whether the submitted GeoJSON Features a disjoint or not

    Args:
        feature_A (Feature): a GeoJSON Feature of any type
        feature_B (Feature): a GeoJSON feature of any type

    Returns:
        Bool: returns 'True' if the features are disjoint and do not intersect
    """
    gdfA = geoJSONtoGDF(feature_A)
    gdfB = geoJSONtoGDF(feature_B)
    return gdfA.disjoint(gdfB)[0]

def distance_direct_kilometers(feature_A, feature_B):
    """Calculates the shortest distance between the submitted Feature. It makes no difference which geometry type the submitted features are. 

    Args:
        feature_A (Feature): a valid GeoJSON Feature of any type
        feature_B (Feature): a valid GeoJSON Feature of any type

    Returns:
        Number: the distance between the submitted Features in kilometers
    """
    gdfA = geoJSONtoGDF(feature_A)
    gdfB = geoJSONtoGDF(feature_B)
    return gdfA.distance(gdfB)[0]/1000

def intersects(feature_A, feature_B):
    """Negates the result of function 'disjoint' to check whether two features intersect each other

    Args:
        feature_A (Feature): a GeoJSON Feature of any type
        feature_B (Feature): a GeoJSON Feature of any type

    Returns:
        Bool: returns 'True' if the submitted features intersect each other
    """
    return not disjoint(feature_A, feature_B)

def intersection(feature_A, feature_B):
    """Encapsulates geopandas function 'intersection' to compute the intersection between two GeoJSON Feature.

    Args:
        feature_A (Feature): a valid GeoJSON Feature of any type
        feature_B (Feature): a valid GeoJSON Feature of any type

    Returns:
        Feature: returns a feature representing the geometry both submitted features share. If they dont share any points the output is an empty feature.
    """
    gdfA = geoJSONtoGDF(feature_A)
    gdfB = geoJSONtoGDF(feature_B)
    
    out = gdfA.intersection(gdfB)[0]
    return geom2Feature(out)

def nearestPoint_directDistance(targetPoint, pointCollection):
    """Identify the nearest Point to a target Point within a submitted FeatureCollection<Point> using Geopandas function 'sjoin_nearest'

    Args:
        targetPoint (Feature<Point>): a GeoJSON feature with geometry type 'Point', for which the nearest point will be searched
        pointCollection (FeatureCollection<Point>):  a GeoJSON FeatureCollection of features with geometry type  'Point'

    Returns:
        Feature<Point>: returns the nearest GeoJSON Point Feature with the shortest direct distance to 'targetPoint'.
    """
    if not isGeoJSONPointFeature(targetPoint):
        throwError("The submitted object targetPoint is not a valid GeoJSON point feature. It was: " + str(targetPoint))
    
    for pointCandidate in pointCollection["features"]:
        if not isGeoJSONPointFeature(targetPoint):
            throwError("The submitted pointCollection contains features that are no valid GeoJSON point features. PointCandidate was: " + str(pointCandidate))
    
    gdfPoint = geoJSONtoGDF(targetPoint)
    gdfCollection = geoJSONtoGDF(pointCollection)

    joint = gpd.sjoin_nearest(gdfPoint, gdfCollection)
    indexNearestPoint = joint.loc[0, "index_right"]

    gdfOut = gpd.GeoDataFrame([gdfCollection.loc[indexNearestPoint]])
    featureOut = geojson.loads(gdfOut.to_json(drop_id=True))
    return featureOut["features"][0]



def nearestPointOnLine_directDistance(targetPoint, lineString):
    """Identifies the the closest Point to 'targetPoint' on the submitted 'lineString'. The used function 'shapely.ops.nearest_points' is also capable of calculating the distance to any other geometry type.

    Args:
        targetPoint (Feature<Point>): a GeoJSON feature with geometry type 'Point', for which the nearest point will be searched
        lineString (Feature<LineString|MultiLineString>): a GeoJSON feature  with geometry type 'LineString' or 'MultiLineString'

    Returns:
        Feature<Point>: returns the nearest GeoJSON Point Feature with the shortest direct distance to 'targetPoint'. Furthermore it contains the property 'dist', which
        contains the direct distance to 'targetPoint' in kilometers.
    """
    if not isGeoJSONPointFeature(targetPoint):
        throwError("The submitted object targetPoint is not a valid GeoJSON point feature. It was: " + str(targetPoint))
    
    if not isGeoJSONLineStringFeature(lineString):
        throwError("The submitted lineStringCandidate is not a valid GeoJSON LineString|MultiLineString feature. Candidate was: " + str(lineString))
    
    gdfPoint = geoJSONtoGDF(targetPoint)
    gdfLine = geoJSONtoGDF(lineString)

    nearestPoints = shapely.ops.nearest_points(gdfPoint.geometry, gdfLine.geometry)
    dist = nearestPoints[0].distance(nearestPoints[1])

    outFeature = geom2Feature(nearestPoints[1][0])
    outFeature["properties"]["dist"] = dist[0] / 1000
    return outFeature

def nearestPointOnLines_directDistance(targetPoint, lineStringCollection):
    """Identifies the the closest Point to 'targetPoint' on the submitted 'lineStringCollection'. The used function 'shapely.ops.nearest_points' is also capable of calculating the distance to any other geometry type.

    Args:
        targetPoint (Feature<Point>): a GeoJSON feature with geometry type 'Point', for which the nearest point will be searched
        lineString (FeatureCollection<LineString|MultiLineString>): a GeoJSON featureCollection  with geometry types 'LineString' or 'MultiLineString'

    Returns:
        Feature<Point>: returns the nearest GeoJSON Point Feature with the shortest direct distance to 'targetPoint'. Furthermore it contains the property 'dist', which
        contains the direct distance to 'targetPoint' in kilometers.
    """
    if not isGeoJSONPointFeature(targetPoint):
        throwError("The submitted object targetPoint is not a valid GeoJSON point feature. It was: " + str(targetPoint))
    
    for lineStringCandidate in lineStringCollection["features"]:
        if not isGeoJSONLineStringFeature(lineStringCandidate):
            throwError("The submitted lineStringCandidate is not a valid GeoJSON LineString|MultiLineString feature. Candidate was: " + str(lineStringCandidate))
    
    shortestDistance = None
    nearestPoint = None

    for lineStringCandidate in lineStringCollection["features"]:
        pointCandidate = nearestPointOnLine_directDistance(targetPoint, lineStringCandidate)

        if shortestDistance == None or pointCandidate["properties"]["dist"] < shortestDistance:
            shortestDistance = pointCandidate["properties"]["dist"]
            nearestPoint = pointCandidate
    
    return nearestPoint

def nearestPointOnPolygon_directDistance(targetPoint, polygon):
    """Calculate the nearest Point of a submitted polygon to a target Point. Therefore the polygon gets splitted in its boundary 'LineString' and the distance to the nearest Point on this LineString gets identified.

    Args:
        targetPoint (Feature<Point>): a GeoJSON feature with geometry type 'Point', for which the nearest point will be searched
        polygon (Feature<Polygon|MultiPolygon>): a GeoJSON feature with geometry type 'Polygon' or 'MultiPolygon'

    Returns:
        Feature<Point>: returns the nearest GeoJSON Point Feature with the shortest direct distance to 'targetPoint'. Furthermore it contains the property 'dist', which
        contains the direct distance to 'targetPoint' in kilometers.
    """
    if not isGeoJSONPointFeature(targetPoint):
        throwError("The submitted object targetPoint is not a valid GeoJSON point feature. It was: " + str(targetPoint))
    
    if not isGeoJSONPolygonFeature(polygon):
        throwError("The submitted Polygon is not a valid GeoJSON Polygon feature. Candidate was: " + str(polygon))
    
    gdfPoint = geoJSONtoGDF(targetPoint)
    gdfPolygon = geoJSONtoGDF(polygon)

    bounds = gdfPolygon.boundary

    nearestPoints = shapely.ops.nearest_points(gdfPoint.geometry, bounds)
    dist = nearestPoints[0].distance(nearestPoints[1])

    outFeature = geom2Feature(nearestPoints[1][0])
    outFeature["properties"]["dist"] = dist[0] / 1000
    return outFeature

def nearestPointOnPolygons_directDistance(targetPoint, polygonCollection):
    """Calculate the nearest Point of a submitted FeatureCollection<Polygon> to a target Point. Therefore the polygons gets splitted in its boundary 'LineString' and the distance to the nearest Point on this LineString gets identified.

    Args:
        targetPoint (Feature<Point>): a GeoJSON feature with geometry type 'Point', for which the nearest point will be searched
        polygon (FeatureCollection<Polygon|MultiPolygon>): a GeoJSON feature collection with geometry types 'Polygon' or 'MultiPolygon'

    Returns:
        Feature<Point>: returns the nearest GeoJSON Point Feature with the shortest direct distance to 'targetPoint'. Furthermore it contains the property 'dist', which
        contains the direct distance to 'targetPoint' in kilometers.
    """
    if not isGeoJSONPointFeature(targetPoint):
        throwError("The submitted object targetPoint is not a valid GeoJSON point feature. It was: " + str(targetPoint))
    
    for polygonCandidate in polygonCollection["features"]:
        if not isGeoJSONPolygonFeature(polygonCandidate):
            throwError("The submitted polygonCandidate is not a valid GeoJSON Polygon feature. Candidate was: " + str(polygonCandidate))
    
    shortestDistance = None
    nearestPoint = None

    for polygonCandidate in polygonCollection["features"]:
        pointCandidate = nearestPointOnPolygon_directDistance(targetPoint, polygonCandidate)

        if shortestDistance == None or pointCandidate["properties"]["dist"] < shortestDistance:
            shortestDistance = pointCandidate["properties"]["dist"]
            nearestPoint = pointCandidate
    
    return nearestPoint

def overlap(feature_A, feature_B):
    """encapsulates Geopandas.GeoSeries function 'overlaps' to check whether the submitted Features overlap or not

    Args:
        feature_A (Feature): a GeoJSON Feature of any type
        feature_B (Feature): a GeoJSON Feature of any type

    Returns:
        Bool: returns 'True' if 'feature_A' overlaps partially with 'feature_B'
    """
    gdfA = geoJSONtoGDF(feature_A)
    gdfB = geoJSONtoGDF(feature_B)

    return gdfA.overlaps(gdfB)[0]

def union(polygonFeature_A, polygonFeature_B):
    """Encapsulates GeoPandas function 'union' to compute the union of two or more polygonal GeoJSON Features.

    Args:
        polygonFeature_A (Feature<Polygon|MultiPolygon>): a GeoJSON Feature of type 'Polygon'
        polygonFeature_B (Feature<Polygon|MultiPolygon>): a GeoJSON Feature of type 'Polygon'

    Returns:
        Feature<Polygon|MultiPolygon>|None: the GeoJSON feature of type Polygon or MultiPolygon representing the union of the submitted features.
    """
    gdfA = geoJSONtoGDF(polygonFeature_A)
    gdfB = geoJSONtoGDF(polygonFeature_B)

    geom = gdfA.union(gdfB)[0]
    return geom2Feature(geom)


def within(feature_A, feature_B):
    """Encapsulates GeoPandas function 'within' to check whether 'feature_A' is completely inside 'feature_B'.

    Args:
        feature_A (Feature): a valid GeoJSON Feature of any type
        feature_B (Feature): a valid GeoJSON Feature of any type

    Returns:
        Bool: returns if 'feature_A' lies completely within 'feature_B'
    """
    gdfA = geoJSONtoGDF(feature_A)
    gdfB = geoJSONtoGDF(feature_B)

    return gdfA.within(gdfB)[0]

def pointsWithinPolygon(points, polygons):
    """Find all points that lie completely within a submitted polygon. 

    Args:
        points (Feature|FeatureCollection): a GeoJSON Point feature
        polygons (FeatureCollection|Feature|Geometry): a GeoJSON polygonal geometry (i.e. Feature, Geometry, FeatureCollection)

    Returns:
        FeatureCollection: returns a FeatureCollection that contains all points that lie within at least one polygon of the submitted polygons as FeatureCollection<Point>
    """
    gdfPoints = geoJSONtoGDF(points)
    gdfPolygons = geoJSONtoGDF(polygons)

    if "validEndDate" in polygons["properties"]:
        gdfPolygons = gdfPolygons.drop(columns=["validStartDate", "validEndDate"])
    else:
        gdfPolygons = gdfPolygons.drop(columns=["validStartDate"])

    joint = gdfPoints.sjoin(gdfPolygons, predicate="within")
    # print(joint)
    # gdfOut = joint.drop(columns=["index_right", "id"])

    featureOut = geojson.loads(joint.to_json(drop_id=True))
    return featureOut


def within_usingBBOX(feature_A, feature_B):
    """This method is an alternative implementation of a spatial 'within' function for spatial features.
    First of all, it computes bounding boxes of the relevant features to speed up the spatial comparison.
    Furthermore, instead of checking whether 'feature_A' lies completely within  'feature_B',
    it inspects whether the bounding boxes overlap for more than 90.0%. If the features's geometries might contain faulty coordinates for whatever reason that would
    cause a strict spatial 'within' comparison to output 'false', this alternative approach ensures that such small coordinate failures will still
    result in a positive 'within' check.

    Args:
        feature_A (Feature<Polygon>): a base indicator (input) feature as GeoJSON Feature
        feature_B (Feature<Polygon>): a target Feature as GeoJSON feature (for which indicator results shall be computed)

    Returns:
        Bool: returns 'true' if the 'feature_A' lies within 'feature_B'
        (precisely, if their bounding boxes overlap for more than 90.0%); 'false 'otherwise
    """
    feature_A_bbox = bbox_feature(feature_A)
    feature_B_bbox = bbox_feature(feature_B)
    feature_A_bbox_area = area(feature_A_bbox)

    intersect = intersection(feature_B_bbox, feature_A_bbox)

    # if there is no intersection (features are disjoint) then skip this
    if intersect == None:
        return False
    
    intersectionArea = area(intersect)
    overlapInPercent = abs(intersectionArea / feature_A_bbox_area) * 100

    #if indicatorFeature overlaps for at least 90% with feature_B, the assign it for aggregation to feature_B
    if overlapInPercent >= 90.0:
        return True
    
    return False

def intersectLineFeatureCollectionByPolygonFeature(lineStringCollection, polygonFeature):
    """computes the intersections of linestrings of a featureCollection and a polygon feature

    Args:
        lineStringCollection (FeatureCollection<LineString>): a valid GeoJSON FeatureCollection of type LineString
        polygonFeature (Feature<Polygon>): a valid GeoJSON Feature

    Returns:
        FeatureCollection<LineString>: returns the submitted FeatureCollection with the geometry replaced by the intersection
    """
    gdfLine = geoJSONtoGDF(lineStringCollection)
    gdfPolygon = geoJSONtoGDF(polygonFeature)

    featureCollection = geojson.FeatureCollection({})
    i = 0

    geoms = gdfLine.intersection(gdfPolygon.loc[0, "geometry"])

    for geom in geoms:
        gdfLine.loc[i, "geometry"] = geom
        i = i + 1

    featureOut = geojson.loads(gdfLine.to_json(drop_id=True))
    return featureOut



def summarizeLineSegmentLenghts(featureCollection):
    """Computes the lenght of all line segments of a linestring feature Collection.

    Args:
        featureCollection (FeatureCollection<LineString>): a valid GeoJSON FeatureCollection containing LineString Features

    Returns:
        float64: returns the summarized length of all line segments
    """
    gdf = geoJSONtoGDF(featureCollection)
    length = gdf.length
    return length.sum()

#
#   From Here OpenRouteService
#

def distance_waypath_kilometers():
    #TODO:  
    return None

def distance_matrix_kilometers():
    #TODO
    return None

def duration_matrix_seconds():
    #TODO
    return None

def isochrones_byTime():
    #TODO
    return None

def computeIsochrones_byTime():
    #TODO
    return None

def isochrones_byDistance():
    #TODO
    return None

def computeIsochrones_byDistance():
    #TODO
    return None

def executeOrsQuery():
    #TODO
    return None

def nearestPoint_waypathDistance():
    #TODO
    return None





"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

API_HELPER_METHODS_STATISTICAL_OPERATIONS

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def convertPropertyArrayToNumberArray(propertyArray):
    """Takes a property array of arbitrary input objects and returns a valueArray of numeric values which have been converted to a number by. 
    Any property value of the input array, whose conversion results in NaN using the check 'math.isnan(value)' or is boolean will be completely removed from the array
    Thus the resulting array may have fewer entries than the original array.

    Args:
        propertyArray (Array<any>): an array of arbitrary values (i.e. String, Float, Bool, ...)

    Returns:
        Array<Float>: returns the array of all values that were successfully converted to a number. responseArray.length may be smaller than inputArray.length, if inputArray contains boolean items or items whose Number-conversion result in NaN
    """
    numericArray = []
    
    for value in propertyArray:
        try:
           numericArray.append(float(value))
        except:
            print(str(value) + " is not convertible to float!")

    return numericArray

def convertPropertyDictToNumberDict_fromIdValueDict(indicatorIdValueDict):
    """Takes a property dictionary of arbitrary input objects and returns a valueDict of numeric values which have been converted to a number. 
    Any property value of the input dict, whose conversion results in NaN using the check 'math.isnan(value)' or is boolean will be completely removed from the dict
    Thus the resulting dict may have fewer entries than the original dict.

    Args:
        indicatorIdValueDict (Dict<String, any>): a dictionary containing key value pairs where key=ID and value=indicatorValue

    Returns:
        Dict<String, Float>: returns the dictionary of all input entries which have been successfully converted to float. The size may be smaller than the original dict.
    """
    resultDict = {}

    for key, value in indicatorIdValueDict.items():
        try:
            if value is True or value is False:
                exit
            elif math.isnan(float(value)):
                exit
            else:
                resultDict[key] = float((value))
        except:
            print(str(value) + " is not convertible to float!")

    return resultDict

def sum(valueArray):
    """Compute the sum of the submitted 'valueArray'

    Args:
        valueArray (Array<Any>): an array of arbitrary input object which should contain number values to calculate the sum. The array gets transformed using 'convertPropertyArrayToNumberArray'

    Returns:
        Float: returns the sum of the submitted Array
    """
    valueArray = convertPropertyArrayToNumberArray(valueArray)
    return numpy.sum(valueArray)
    

def covariance(populationArray_A, populationArray_B):
    """encapsulates numpys function 'cov' to compute the covariance of two arrays of the same lenght. 

    Args:
        populationArray_A (Array<Number>): first data array of numeric values (will be piped through function 'convertPropertyArrayToNumberArray()' to ensure that only numeric values are submitted)
        populationArray_B (Array<Number>): first data array of numeric values (will be piped through function 'convertPropertyArrayToNumberArray()' to ensure that only numeric values are submitted)

    Returns:
        Float: returns the covariance value of the submitted Arrays (or raises an Error if the submitted Arrays are not same length)
    """
    try:
        valueArray_A = convertPropertyArrayToNumberArray(populationArray_A)
        valueArray_B = convertPropertyArrayToNumberArray(populationArray_B)
        return numpy.cov(valueArray_A, valueArray_B)[0, 1]
    except ValueError:
        throwError("The submitted Arrays are not the same length, cannot compute a covariance!")
    
def max(populationArray):
    """Encapsulates numpys function 'max' to compute the max value of the submitted value array.

    Args:
        populationArray (Array<Float>): data array of numeric values (will be piped through function 'convertPropertyArrayToNumberArray()' to ensure that only numeric values are submitted)

    Returns:
        Float: returns the max value of the submitted array of numeric values
    """
    populationArray = convertPropertyArrayToNumberArray(populationArray)
    return numpy.max(populationArray)

def min(populationArray):
    """Encapsulates numpys function 'min' to compute the min value of the submitted value array.

    Args:
        populationArray (Array<Float>): data array of numeric values (will be piped through function 'convertPropertyArrayToNumberArray()' to ensure that only numeric values are submitted)

    Returns:
        Float: returns the min value of the submitted array of numeric values
    """
    populationArray = convertPropertyArrayToNumberArray(populationArray)
    return numpy.min(populationArray)

def minMaxNormalization_singleValue(min, max, value):
    """Implements a min max normalization value of the submitted value using the formula '(value - min) / (max) - (min)'

    Args:
        min (Float): the min value used in upper normalization formula
        max (Float): the max value used in upper normalization formula
        value (Float): the value to be normalized

    Returns:
        Float: returns the normalized value
    """
    normalizedValue = (float(value) - float(min)) / (float(max) - float(min))
    return normalizedValue

def minMaxNormalization_wholeValueArray(populationArray):
    """Implements a min max normalization for a whole submitted value array using function 'minMaxNormalization_singleValue'

    Args:
        populationArray (Array<Float>): an array of numeric values for which the min max normalized value array shall be computed (will be piped through function 'convertPropertyArrayToNumberArray()' to ensure that only numeric values are submitted)

    Returns:
        Array<Float>: returns the submitted value where each value is normalized
    """
    populationArray = convertPropertyArrayToNumberArray(populationArray)

    minValue = min(populationArray)
    maxValue = max(populationArray)

    normalizedArray = []

    for value in populationArray:
        normalizedArray.append(minMaxNormalization_singleValue(minValue, maxValue, value))

    return normalizedArray

def minMaxNormalization_inverted_singleValue(min, max, value):
    """Implements an inverted min max normalization value of the submitted value using the formula '1 - ((value - min) / (max) - (min))'

    Args:
        min (Float): the min value used in upper normalization formula
        max (Float): the max value used in upper normalization formula
        value (Float): the value to be normalized

    Returns:
        Float: returns the inverted normalized value
    """
    normalizedValue = 1 - minMaxNormalization_singleValue(min, max, value)
    return normalizedValue

def minMaxNormalization_inverted_wholeValueArray(populationArray):
    """Implements an inverted min max normalization for a whole submitted value array using function 'minMaxNormalization_inverted_singleValue'

    Args:
        populationArray (Array<Float>): an array of numeric values for which the inverted min max normalized value array shall be computed (will be piped through function 'convertPropertyArrayToNumberArray()' to ensure that only numeric values are submitted)

    Returns:
        Array<Float>: returns the submitted value where each value is inverted normalized
    """
    populationArray = convertPropertyArrayToNumberArray(populationArray)

    minValue = min(populationArray)
    maxValue = max(populationArray)

    invNormalizedArr = []

    for value in populationArray:
        invNormalizedArr.append(minMaxNormalization_inverted_singleValue(minValue, maxValue, value))

    return invNormalizedArr

def minMaxNormalization_fromIdValueDict(indicatorIdValueDict):
    """implements a min max normalization algorithm for an indicator id value dictionary. 

    Args:
        indicatorIdValueDict (Dict<String, Float>): Dictionary of all indicator id and value pairs where key=id and value=indicatorValue. Types get converted to float values if possible, if not possible the result dict is possibly shorter than the submitted.

    Returns:
        Dict<String, Float>: returns the same dict, but instead of the original indicator value the respective normalized value is set as the value for ech id.
    """
    resultDict = {}

    numericEntriesDict = convertPropertyDictToNumberDict_fromIdValueDict(indicatorIdValueDict)

    indicatorValues = getIndicatorValueArray_fromIdValueDict(numericEntriesDict)

    normalizedArray = minMaxNormalization_wholeValueArray(indicatorValues)

    if not len(normalizedArray) == len(numericEntriesDict):
        log("Error deteced during 'minMaxNormalization_fromIdValueMap'. The size of input id value map is not equal to the size of the computed normalization array. Hence cannot continue compute normalization values for whole map. Some values may not be numeric, and thus get lost in between?")

    i = 0

    for key, value in numericEntriesDict.items():
        resultDict[key] = normalizedArray[i]
        i = i + 1
    
    return resultDict
    
def minMaxNormalization_inverted_fromIdValueDict(indicatorIdValueDict):
    """implements an inverted min max normalization algorithm for an indicator id value dictionary. 

    Args:
        indicatorIdValueDict (Dict<String, Float>): Dictionary of all indicator id and value pairs where key=id and value=indicatorValue. Types get converted to float values if possible, if not possible the result dict is possibly shorter than the submitted.

    Returns:
        Dict<String, Float>: returns the same dict, but instead of the original indicator value the respective inverted normalized value is set as the value for ech id.
    """
    normalizedDict = minMaxNormalization_fromIdValueDict(indicatorIdValueDict)

    invertedDict = {}
    for key, value in normalizedDict.items():
        invertedDict[key] = 1 - value

    return invertedDict

def rank(populationArray):
    """encapsulates scipy.stats function 'rank' to compute the rank array of the submitted value array

    Args:
        populationArray (Array<Float>): an array of numeric values for which the mean shall be computed (will be piped through function 'convertPropertyArrayToNumberArray()' to make sure only numeric values are ranked. Therefore the result can be shorter than the input)

    Returns:
        numpy.ndarray<Float>: returns the ranks of the submitted array of numeric values
    """
    populationArray = convertPropertyArrayToNumberArray(populationArray)
    return stats.rankdata(populationArray)

def rank_fromIdValueDict(indicatorIdValueDict):
    """encapsulates scipy.stats function 'rank' to compute the rank array of the submitted 'indicatorIdValueDict'

    Args:
        indicatorIdValueDict (Dict<String, Float>): a dictionary of key value pairs. Where key = id and value = indicatorValue 

    Returns:
        Dict<String, Float>: returns the same dictionary like the submitted, but the values have been replaced by their rank inside the dictionary.
    """
    resultDict = {}

    numericEntriesDict = convertPropertyDictToNumberDict_fromIdValueDict(indicatorIdValueDict)

    indicatorValues = getIndicatorValueArray_fromIdValueDict(numericEntriesDict)

    rankedValues = rank(indicatorValues)

    if not len(rankedValues) == len(numericEntriesDict):
        log("Error deteced during 'rank_fromIdValueMap'. The size of input id value map is not equal to the size of the computed ranked array. Hence cannot continue compute rank values for whole map. Some values may not be numeric, and thus get lost in between?")

    i = 0

    for key, value in numericEntriesDict.items():
        resultDict[key] = rankedValues[i]
        i = i + 1
    
    return resultDict

def geomean(populationArray):
    """Encapsulates scipy.stats.mstats function 'gmean' to compute the geometric mean value of the submitted value array.

    Args:
        populationArray (Array<Float>): an array of numeric values for which the mean shall be computed (will be piped through function 'convertPropertyArrayToNumberArray()' to make sure only numeric values are ranked. Therefore the result can be shorter than the input)

    Returns:
        Float: returns the geometric mean value of the submitted array of numeric values. (If there are zero values in the input the output will be zero)
    """
    populationArray = convertPropertyArrayToNumberArray(populationArray)
    return stats.mstats.gmean(populationArray)

def geomean_fromIdValueDict(indicatorIdValueDictArray):
    """Encapsulates scipy.stats.mstats function 'gmean' to compute the geometric mean value of the submitted array of indicator id and value map objects. Only values for those features will be computed, that have an input value for all entries of the input 'indicatorIdValueMapArray'.

    Args:
        indicatorIdValueDictArray (Array<Dict<String, Float>>): an array of map objects containing indicator feature ID and numeric value pairs (will be piped through function  'convertPropertyMapToNumberMap_fromIdValueMap' to ensure that only numeric values are submitted)

    Returns:
        Dict<String, Float>: returns a map containing the indicator feature id and computed geometric mean value of the submitted array of indicator id and value map objects. Only values for those features will be computed, that have an input value for all entries of the input 'indicatorIdValueMapArray'.
    """
    resultDict = {}

    numericDictArray = []
    for dict in indicatorIdValueDictArray:
        numericDictArray.append(convertPropertyDictToNumberDict_fromIdValueDict(dict))
    
    refSize = len(numericDictArray[0])
    for dict in numericDictArray:
        if not len(dict) == refSize:
            log("Problem detected while computing geomean from indicatorIdValueMapArray. The sizes of the input base indicator map entries are not equal. Results might not be correct. Will continue computation.")

    # iterate over the first map entries; collect all values of all baseIndicators for each feature
    # compute mean and set it in result map
    refMap = numericDictArray[0]
    for key, value in refMap.items():

        baseIndicatorValues = []

        for numericDict in numericDictArray:
            # collect sub indicator values
            if key in numericDict:
                baseIndicatorValues.append(numericDict[key])

        # If not all baseIndicator have the required value, then DO NOT SET the value at all!
        # It seems to be the most transparent solution
        if len(baseIndicatorValues) == len(numericDictArray):
            resultDict[key] = stats.mstats.gmean(baseIndicatorValues)

    return resultDict

def mean(populationArray):
    """Encapsulates numpys function 'mean' to compute the mean value of the submitted value array

    Args:
        populationArray (Array<Float>): an array of numeric values for which the mean shall be computed (will be piped through function 'convertPropertyArrayToNumberArray()' to ensure that only numeric values are submitted)

    Returns:
        float: returns the mean value of the submitted array of numeric values
    """
    populationArray = convertPropertyArrayToNumberArray(populationArray)
    return numpy.mean(populationArray)

def mean_fromIdValueDict(indicatorIdValueDictArray):
    """Encapsulates numpys function 'mean' to compute the mean value of the submitted array of indicator id and value map objects. Only values for those features will be computed, that have an input value for all entries of the input 'indicatorIdValueMapArray'.

    Args:
        indicatorIdValueDictArray (Array<Dict<String, Float>>): an array of map objects containing indicator feature ID and numeric value pairs (will be piped through function  'convertPropertyMapToNumberMap_fromIdValueMap' to ensure that only numeric values are submitted)

    Returns:
        Dict<String, Float>: returns a map containing the indicator feature id and computed mean value of the submitted array of indicator id and value map objects. Only values for those features will be computed, that have an input value for all entries of the input 'indicatorIdValueMapArray'.
    """
    resultDict = {}

    numericDictArray = []
    for dict in indicatorIdValueDictArray:
        numericDictArray.append(convertPropertyDictToNumberDict_fromIdValueDict(dict))
    
    refSize = len(numericDictArray[0])
    for dict in numericDictArray:
        if not len(dict) == refSize:
            log("Problem detected while computing geomean from indicatorIdValueMapArray. The sizes of the input base indicator map entries are not equal. Results might not be correct. Will continue computation.")

    # iterate over the first map entries; collect all values of all baseIndicators for each feature
    # compute mean and set it in result map
    refMap = numericDictArray[0]
    for key, value in refMap.items():

        baseIndicatorValues = []

        for numericDict in numericDictArray:
            # collect sub indicator values
            if key in numericDict:
                baseIndicatorValues.append(numericDict[key])

        # If not all baseIndicator have the required value, then DO NOT SET the value at all!
        # It seems to be the most transparent solution
        if len(baseIndicatorValues) == len(numericDictArray):
            resultDict[key] = numpy.mean(baseIndicatorValues)

    return resultDict

def meanSquareError(populationArray):
    """Implements a function to compute the mean square error value of the submitted value array. For that the mean value is used as expectation.

    Args:
        populationArray (Array<Float>): an array of numeric values for which the mean square error value shall be computed (will be piped through function 'convertPropertyArrayToNumberArray()' to ensure that only numeric values are submitted)

    Returns:
        Float: returns the mean squared error value of the submitted array of numeric values
    """
    populationArray = convertPropertyArrayToNumberArray(populationArray)
    
    arithMean = numpy.mean(populationArray)
    err = list(map(lambda x : x - arithMean, populationArray))
    return   numpy.mean(err)

def median(populationArray):
    """Encapsulates numpys function 'median' to compute the median value of a submitted array.

    Args:
        populationArray (Array<Float>): an array of numeric values for which the mean square error value shall be computed (will be piped through function 'convertPropertyArrayToNumberArray()' to ensure that only numeric values are submitted)

    Returns:
        Float: returns the median value of the submitted array of numeric values.
    """
    populationArray = convertPropertyArrayToNumberArray(populationArray)
    return numpy.median(populationArray)

def min_fromIdValueDict(indicatorIdValueDictArray):
    """Encapsulates numpys function 'min' to compute the min value of the submitted array of indicator id and value dict objects. Only values for those features will be computed, that have an input value for all entries of the input 'indicatorIdValuedictArray'.

    Args:
        indicatorIdValueDictArray (Array<Dict<String, Float>>): an array of dict objects containing indicator feature ID and numeric value pairs (will be piped through function 'convertPropertydictToNumberdict_fromIdValuedict' to ensure that only numeric values are submitted)

    Returns:
        Dict<String, Float>: returns a dict containing the indicator feature id and computed min value of the submitted array of indicator id and value dict objects. Only values for those features will be computed, that have an input value for all entries of the input 'indicatorIdValuedictArray'.
    """
    resultDict = {}

    numericDictArray = []
    for dict in indicatorIdValueDictArray:
        numericDictArray.append(convertPropertyDictToNumberDict_fromIdValueDict(dict))
    
    refSize = len(numericDictArray[0])
    for dict in numericDictArray:
        if not len(dict) == refSize:
            log("Problem detected while computing geomean from indicatorIdValueMapArray. The sizes of the input base indicator map entries are not equal. Results might not be correct. Will continue computation.")

    # iterate over the first map entries; collect all values of all baseIndicators for each feature
    # compute mean and set it in result map
    refMap = numericDictArray[0]
    for key, value in refMap.items():

        baseIndicatorValues = []

        for numericDict in numericDictArray:
            # collect sub indicator values
            if key in numericDict:
                baseIndicatorValues.append(numericDict[key])

        # If not all baseIndicator have the required value, then DO NOT SET the value at all!
        # It seems to be the most transparent solution
        if len(baseIndicatorValues) == len(numericDictArray):
            resultDict[key] = numpy.min(baseIndicatorValues)

    return resultDict

def percentile(populationArray, k):
    """Encapsulates numpys function 'percentile' to compute the percentile of the submitted value array.

    Args:
        populationArray (Array<Float>): an array of numeric values for which the percentiles shall be computed (will be piped through function 'convertPropertyArrayToNumberArray()' to ensure that only numeric values are submitted)
        k (Float): the value between 0 - 100 to specify the percentile

    Returns:
        Float: returns the k-th percentile of the submitted array.
    """
    populationArray = convertPropertyArrayToNumberArray(populationArray)
    return numpy.percentile(populationArray, k)

def quantiles(populationArray, quantilesArray):
    """Encapsulates numpys function 'quantile' to compute the quantiles of a 'populationArray'. The Quantiles are submitted in an Array.

    Args:
        populationArray (Array<Float>): an array of numeric values for which the quantiles shall be computed (will be piped through function 'convertPropertyArrayToNumberArray()' to ensure that only numeric values are submitted)
        quantilesArray (Array<Float>): an array of quantile values in range (0 - 1).

    Returns:
        Array<Float>: returns the quantiles of the 'populationArray' according to the 'quantilesArray'
    """
    populationArray = convertPropertyArrayToNumberArray(populationArray)
    return numpy.quantile(populationArray, quantilesArray)

def quartiles(populationArray):
    """Encapsulates numpys function 'quantile' including an array with quartile borders to compute the quartiles of a submitted 'populationArray'

    Args:
        populationArray (Array<Float>): an array of numeric values for which the quartiles shall be computed (will be piped through function 'convertPropertyArrayToNumberArray()' to ensure that only numeric values are submitted)

    Returns:
        Array<Float>: returns the quartiles of the submitted array of numeric values
    """
    populationArray = convertPropertyArrayToNumberArray(populationArray)
    return numpy.quantile(populationArray, [0, 0.25, 0.5, 0.75, 1])

def rangeValue(populationArray):
    """Implements a function to compute the range value of the submitted value array.

    Args:
        populationArray (Array<Float>): an array of numeric values for which the range value shall be computed (will be piped through function 'convertPropertyArrayToNumberArray()' to ensure that only numeric values are submitted)

    Returns:
        Float: returns the range value using the following function 'max(populationArray) - min(populationArray)'
    """
    populationArray = convertPropertyArrayToNumberArray(populationArray)
    return max(populationArray) - min(populationArray)

def standardDeviation(values, computeSampledStandardDeviation):
    """Encapsulates numpys function 'std' to compute the standard deviation of a submitted values array. 

    Args:
        values (Array<float>): an array of numeric values for which the standard deviation value shall be computed (will be piped through function 'convertPropertyArrayToNumberArray()' to ensure that only numeric values are submitted)
        computeSampledStandardDeviation (bool): optionale value to specify the formula used to calculate the standard deviation. If set to 'True' the sample standard deviation gets calculated where the degrees of freedom are reduced by 1
        if set to 'False' the population standard deviation gets calculated which is also the uncorrect standard deviation.

    Returns:
        float: returns the standard deviation
    """
    values = convertPropertyArrayToNumberArray(values)

    if computeSampledStandardDeviation:
        return numpy.std(values, ddof=1)
    else:
        return numpy.std(values, ddof=0)

def variance(populationArray, computeSampledVariance):
    """Encapsulates numpys function 'var' to compute the variance of a submitted values array

    Args:
        populationArray (Array<float>): an array of numeric values for which the variance value shall be computed (will be piped through function 'convertPropertyArrayToNumberArray()' to ensure that only numeric values are submitted)
        computeSampledVariance (bool): optionale value to specify the formula used to calculate the standard deviation. If set to 'True' the sample standard deviation gets calculated where the degrees of freedom are reduced by 1
        if set to 'False' the population standard deviation gets calculated which is also the uncorrect standard deviation.

    Returns:
        float: returns the variance of the samples.
    """
    populationArray = convertPropertyArrayToNumberArray(populationArray)

    if computeSampledVariance:
        return numpy.var(populationArray, ddof=1)
    else:
        return numpy.var(populationArray, ddof=0)

def zScore_byMeanAndStdev(value, mean, stdev):
    """Implements a function to calculate the zscore by a given value, mean-value and the standard deviation.

    Args:
        value (float): numeric value for which the zscore shall be computed.
        mean (float): numeric value representing the mean value of a population.
        stdev (float): numeric value representing the standard deviation value of a population.

    Returns:
        float: returns the zscore for the submitted 'value'.
    """ 
    return (value - mean) / stdev

def zScore_byPopulationArray(value, populationArray, computeSampledStandardDeviation: bool):
    """Implements a function to calculate the zscore for a given value by calculating mean and standard deviation of a submitted 'populationArray'.

    Args:
        value (float): the numeric value for which the zscore shall be computed
        populationArray (Array<float>): an array of numeric values for which the standard deviation shall be computed (will be piped through function 'convertPropertyArrayToNumberArray()' to ensure that only numeric values are submitted)
        computeSampledStandardDeviation (bool):  optionale value to specify the formula used to calculate the standard deviation. If set to 'True' the sample standard deviation gets calculated where the degrees of freedom are reduced by 1
        if set to 'False' the population standard deviation gets calculated which is also the uncorrect standard deviation.

    Returns:
        value: returns the zscore of the submitted value.
    """
    meanPop = mean(populationArray)
    stdPop = standardDeviation(populationArray, computeSampledStandardDeviation)

    return (value - meanPop) / stdPop

def formatDateAsString(date: datetime.date):
    """Creates a string describing the date of a submitted datetime.date object.

    Args:
        date (datetime.date): a datetime.date Object (i.e. initialized by datetime.date(2024, 1, 1))

    Returns:
        string: the string representing the date in the format (YYYY-MM-DD) (i.e. 2024-01-01)
    """
    return date.__str__()
    
def formatStringAsDate(stringDate: str):
    """Creates a datetime.date Object based on the submitted string representing a date in format (YYY-MM-DD)

    Args:
        stringDate (str): the string describing the date (YYYY-MM-DD)

    Returns:
        datetime.date: returns a datetime.date Object containing the submitted date.
    """
    array = stringDate.split("-")
    return datetime.date(int(array[0]), int(array[1]), int(array[2]))

def getSubstractNMonthsDate_asString(referenceDateString: str, numberOfMonths: int):
    """Substract n months from the submitted date

    Args:
        referenceDateString (str): the reference date in the string format (YYYY-MM-DD)
        numberOfMonths (int): the number of months to substract from the submitted reference date.

    Returns:
        string: returns the date reduced by given number of months
    """
    array = referenceDateString.split("-")
    
    substractdays = int(numberOfMonths / 12)
    
    restMonths = numberOfMonths - (substractdays * 12)
    
    newMonth = int(array[1]) - restMonths
    newYear = int(array[0]) - substractdays

    if newMonth <= 0:
        newMonth = newMonth + 12
        newYear = newYear - 1
    
    return formatDateAsString(datetime.date(newYear, newMonth, int(array[2])))

def getSubstractNYearsDate_asString(referenceDateString, numberOfYears):
    """Substract n years from the submitted date

    Args:
        referenceDateString (str): the reference date in the string format (YYYY-MM-DD)
        numberOfYears (int): the number of years to substract from the submitted reference date.

    Returns:
        string: returns the date reduced by given number of years
    """
    array = referenceDateString.split("-")
    newYear = int(array[0]) - numberOfYears
    return formatDateAsString(datetime.date(int(newYear), int(array[1]), int(array[2])))

def getSubstractNDaysDate_asString(referenceDateString, numberOfDays):
    """Substract n days from the submitted date

    Args:
        referenceDateString (str): the reference date in the string format (YYYY-MM-DD)
        numberOfdays (int): the number of days to substract from the submitted reference date.

    Returns:
        string: returns the date reduced by given number of days
    """
    date = formatStringAsDate(referenceDateString)
    return formatDateAsString(date - datetime.timedelta(numberOfDays))

def getChange_absolute(feature, targetDate, compareDate):
    """computes the absolute difference/change of indicator values between the submitted dates (if both are present in the dataset) using the formula 'value[targetDate]  - value[compareDate]'

    Args:
        feature (Feature): a valid GeoJSON Feature, which must contain a 'properties' attribute storing the indicator time series according to KomMonitor's data model
        targetDate (string): the reference/target date in the string format 'YYYY-MM-DD', i.e. '2024-01-01'
        compareDate (string): the compare date in the string format 'YYYY-MM-DD', i.e. '2024-01-01' to who the indicator value difference/change shall be computed

    Returns:
        dict<string, float>: returns a dictionary of all input features that have both timestamps and whose cahngeValues were successfully converted to a number.  the response Dict may be smaller than the featureCollection size, if featureCollection contains boolean value items or items whose float-conversion returns in nan the value will be set to 'None'
    """
    targetDatePrefix = getTargetDateWithPropertyPrefix(targetDate)
    compareDatePrefix = getTargetDateWithPropertyPrefix(compareDate)
    targetValue = feature[targetDatePrefix]
    compareValue = feature[compareDatePrefix]

    if not isNoDataValue(compareValue) and not isNoDataValue(targetValue):
        resultValue = float(targetValue) - float(compareValue)
    else: 
        resultValue = None
        
    return resultValue

def getChange_relative_percent(feature, targetDate, compareDate):
    """computes the relative difference/change of indicator values between the submitted dates (if both are present in the dataset) using the formula '100 * ((value[targetDate] - value[compareDate]) / value[compareDate])'

    Args:
        feature (Feature): a valid GeoJSON FeatureCollection, whose features must contain a 'properties' attribute storing the indicator time series according to KomMonitor's data model
        targetDate (string): the reference/target date in the string format 'YYYY-MM-DD', i.e. '2024-01-01'
        compareDate (string): the compare date in the string format 'YYYY-MM-DD', i.e. '2024-01-01' to who the indicator value difference/change shall be computed

    Returns:
        dict<string, float>: returns a dictionary of all input features that have both timestamps and whose cahngeValues were successfully converted to a number.  the response Dict may be smaller than the featureCollection size, if featureCollection contains boolean value items or items whose float-conversion returns in nan the value will be set to 'None'
    """
    targetDatePrefix = getTargetDateWithPropertyPrefix(targetDate)
    compareDatePrefix = getTargetDateWithPropertyPrefix(compareDate)
    
    targetValue = feature[targetDatePrefix]
    compareValue = feature[compareDatePrefix]
    if not isNoDataValue(compareValue) and not isNoDataValue(targetValue):
        if float(compareValue) == 0:
            resultValue = None
            throwError("The reference value is zero, a computation is not possible.")
        
        resultValue = 100 * ((float(targetValue) - float(compareValue)) / float(compareValue))
    else:
        resultValue = None
    return resultValue

def changeAbsolute_n_years(feature, targetDate, numberOfYears):
    """computes the new indicator for an absolute change compared to number of previous Years
    internally tests are run, e.g. if a previous year is available or not

    Args:
        feature (Feature): a valid GeoJSON feature, whose must contain a 'properties' attribute storing the indicator time series according to KomMonitor's data model
        targetDate (string): the reference/target date in the string format 'YYYY-MM-DD', i.e. '2024-01-01'
        numberOfYears (int): the number of Years to substract from the submitted reference Date

    Returns:
        Dict<string, float>: returns the dictionary of all input features that have both timestamps and whose absolute changeValues were successfully converted to a float value. the response Dict may be smaller than the featureCollection size, if featureCollection contains boolean value items or items whose float-conversion returns in nan the value will be set to 'None'
    """
    compareDate = getSubstractNYearsDate_asString(targetDate, numberOfYears)

    return getChange_absolute(feature, targetDate, compareDate)

def changeAbsolute_n_months(featureCollection, targetDate, numberOfMonths):
    """computes the new indicator for an absolute change compared to number of previous months
    internally tests are run, e.g. if a previous year is available or not

    Args:
        featureCollectin (FeatureCollection): a valid GeoJSON FeatureCollection, whose features must contain a 'properties' attribute storing the indicator time series according to KomMonitor's data model
        targetDate (string): the reference/target date in the string format 'YYYY-MM-DD', i.e. '2024-01-01'
        numberOfmonths (int): the number of months to substract from the submitted reference Date

    Returns:
        Dict<string, float>: returns the dictionary of all input features that have both timestamps and whose absolute changeValues were successfully converted to a float value. the response Dict may be smaller than the featureCollection size, if featureCollection contains boolean value items or items whose float-conversion returns in nan the value will be set to 'None'
    """
    compareDate = getSubstractNMonthsDate_asString(targetDate, numberOfMonths)
    return getChange_absolute(featureCollection, targetDate, compareDate)

def changeAbsolute_n_days(featureCollection, targetDate, numberOfDays):
    """computes the new indicator for an absolute change compared to number of previous days
    internally tests are run, e.g. if a previous year is available or not

    Args:
        featureCollectin (FeatureCollection): a valid GeoJSON FeatureCollection, whose features must contain a 'properties' attribute storing the indicator time series according to KomMonitor's data model
        targetDate (string): the reference/target date in the string format 'YYYY-MM-DD', i.e. '2024-01-01'
        numberOfdays (int): the number of days to substract from the submitted reference Date

    Returns:
        Dict<string, float>: returns the dictionary of all input features that have both timestamps and whose absolute changeValues were successfully converted to a float value. the response Dict may be smaller than the featureCollection size, if featureCollection contains boolean value items or items whose float-conversion returns in nan the value will be set to 'None'
    """
    compareDate = getSubstractNDaysDate_asString(targetDate, numberOfDays)
    return getChange_absolute(featureCollection, targetDate, compareDate)

def changeRelative_n_years_percent(featureCollection, targetDate, numberOfYears):
    """computes the new indicator for an relative change compared to number of previous Years
    internally tests are run, e.g. if a previous year is available or not

    Args:
        featureCollectin (FeatureCollection): a valid GeoJSON FeatureCollection, whose features must contain a 'properties' attribute storing the indicator time series according to KomMonitor's data model
        targetDate (string): the reference/target date in the string format 'YYYY-MM-DD', i.e. '2024-01-01'
        numberOfYears (int): the number of Years to substract from the submitted reference Date

    Returns:
        Dict<string, float>: returns the dictionary of all input features that have both timestamps and whose relative changeValues were successfully converted to a float value. the response Dict may be smaller than the featureCollection size, if featureCollection contains boolean value items or items whose float-conversion returns in nan the value will be set to 'None'
    """
    compareDate = getSubstractNYearsDate_asString(targetDate, numberOfYears)
    return getChange_relative_percent(featureCollection, targetDate, compareDate)

def changeRelative_n_months_percent(featureCollection, targetDate, numberOfMonths):
    """computes the new indicator for an relative change compared to number of previous months
    internally tests are run, e.g. if a previous year is available or not

    Args:
        featureCollectin (FeatureCollection): a valid GeoJSON FeatureCollection, whose features must contain a 'properties' attribute storing the indicator time series according to KomMonitor's data model
        targetDate (string): the reference/target date in the string format 'YYYY-MM-DD', i.e. '2024-01-01'
        numberOfmonths (int): the number of months to substract from the submitted reference Date

    Returns:
        Dict<string, float>: returns the dictionary of all input features that have both timestamps and whose relative changeValues were successfully converted to a float value. the response Dict may be smaller than the featureCollection size, if featureCollection contains boolean value items or items whose float-conversion returns in nan the value will be set to 'None'
    """
    compareDate = getSubstractNMonthsDate_asString(targetDate, numberOfMonths)
    return getChange_relative_percent(featureCollection, targetDate, compareDate)

def changeRelative_n_days_percent(featureCollection, targetDate, numberOfDays):
    """computes the new indicator for an relative change compared to number of previous days
    internally tests are run, e.g. if a previous year is available or not

    Args:
        featureCollectin (FeatureCollection): a valid GeoJSON FeatureCollection, whose features must contain a 'properties' attribute storing the indicator time series according to KomMonitor's data model
        targetDate (string): the reference/target date in the string format 'YYYY-MM-DD', i.e. '2024-01-01'
        numberOfdays (int): the number of days to substract from the submitted reference Date

    Returns:
        Dict<string, float>: returns the dictionary of all input features that have both timestamps and whose relative changeValues were successfully converted to a float value. the response Dict may be smaller than the featureCollection size, if featureCollection contains boolean value items or items whose float-conversion returns in nan the value will be set to 'None'
    """
    compareDate = getSubstractNDaysDate_asString(targetDate, numberOfDays)
    return getChange_relative_percent(featureCollection, targetDate, compareDate)

def changeAbsolute_referenceDate(featureCollection, targetDate, referenceDate):
    """computes the new indicator for an absolute change compared to a previous reference date (e.g. prior year or month or day). internally tests are rin, e.g. if a previous reference date is available or not.

    Args:
        featureCollection (FeatureCollection): a valid GeoJSON FeatureCollection, whose features must contain a 'properties' attribute storing the indicator time series according to KomMonitor's data model
        targetDate (string): the reference/target date in the string format 'YYYY-MM-DD', i.e. '2018-01-01'
        referenceDate (string): the reference date in the past in the string format'YYYY-MM-DD', e.g. '2016-01-01' for two years past or '2017-12-01' for one month past

    Returns:
        Dict<string, float>: returns the dictionary of all input features that have both timestamps and whose relative changeValues were successfully converted to a float value. the response Dict may be smaller than the featureCollection size, if featureCollection contains boolean value items or items whose float-conversion returns in nan the value will be set to 'None'
    """
    targetDate_dateformat = formatStringAsDate(targetDate)
    referenceDate_dateformat = formatStringAsDate(referenceDate)

    if targetDate_dateformat <= referenceDate_dateformat:
        throwError("Change computation for fixed reference date does not allow targetDate being <= referenceDate. Values were: targetDate '" + str(targetDate) +"' and referenceDate '" + str(referenceDate) + "'")
    
    return getChange_absolute(featureCollection, targetDate, referenceDate)

def changeRelative_referenceDate_percent(featureCollection, targetDate, referenceDate):
    """computes the new indicator for an relative change compared to a previous reference date (e.g. prior year or month or day). internally tests are rin, e.g. if a previous reference date is available or not.

    Args:
        featureCollection (FeatureCollection): a valid GeoJSON FeatureCollection, whose features must contain a 'properties' attribute storing the indicator time series according to KomMonitor's data model
        targetDate (string): the reference/target date in the string format 'YYYY-MM-DD', i.e. '2018-01-01'
        referenceDate (string): the reference date in the past in the string format'YYYY-MM-DD', e.g. '2016-01-01' for two years past or '2017-12-01' for one month past

    Returns:
        Dict<string, float>: returns the dictionary of all input features that have both timestamps and whose relative changeValues were successfully converted to a float value. the response Dict may be smaller than the featureCollection size, if featureCollection contains boolean value items or items whose float-conversion returns in nan the value will be set to 'None'
    """
    targetDate_dateformat = formatStringAsDate(targetDate)
    referenceDate_dateformat = formatStringAsDate(referenceDate)

    if targetDate_dateformat <= referenceDate_dateformat:
        throwError("Change computation for fixed reference date does not allow targetDate being <= referenceDate. Values were: targetDate '" + str(targetDate) +"' and referenceDate '" + str(referenceDate) + "'")
    
    return getChange_relative_percent(featureCollection, targetDate, referenceDate)

def trend_consecutive_n_years(feature, targetDate, numberOfYears):
    """Computes the new indicator as trend for prior consecutive Years, internally tests are run, e.g. if a previous year is available or not

    Args:
        featureCollection (FeatureCollection): a valid FeatureCollection, whose features must contain a properties attribute storing the indicator time series according to kommonitors data model
        targetDate (string): the reference/target date in the string format 'YYYY-MM-DD', e.g. '2024-01-01'
        numberOfYears (int): the number of prior consecutive Years for which the trend shall be computed.

    Returns:
        Dict<string, float>: returns the dict of all input features whose trend value were successfully computed. ResponseDict may bei smaller than the submitted feature collection. If the feature collection contains values which cannot be converted in a float value the result is 'None'.
    """
    dates = []

    for i in range(numberOfYears, 0, -1):
        dates.append(getSubstractNYearsDate_asString(targetDate, i))
    
    dates.append(targetDate)

    trend = computeTrend(feature, dates)

    return trend

def trend_consecutive_n_months(featureCollection, targetDate, numberOfMonths):
    """Computes the new indicator as trend for prior consecutive months, internally tests are run, e.g. if a previous year is available or not

    Args:
        featureCollection (FeatureCollection): a valid FeatureCollection, whose features must contain a properties attribute storing the indicator time series according to kommonitors data model
        targetDate (string): the reference/target date in the string format 'YYYY-MM-DD', e.g. '2024-01-01'
        numberOfMonths (int): the number of prior consecutive months for which the trend shall be computed.

    Returns:
        Dict<string, float>: returns the dict of all input features whose trend value were successfully computed. ResponseDict may bei smaller than the submitted feature collection. If the feature collection contains values which cannot be converted in a float value the result is 'None'.
    """
    dates = []

    for i in range(numberOfMonths, 0, -1):
        dates.append(getSubstractNMonthsDate_asString(targetDate, i))
    
    dates.append(targetDate)

    resultDict = {}

    for feature in featureCollection["features"]:
        trend = computeTrend(feature, dates)
        if bool(trend) and not isNoDataValue(trend):
            resultDict[getSpatialUnitFeatureIdValue(feature)] = trend

    if len(resultDict) == 0:
        throwError("Trend computation resulted in NoData for each feature")

    return resultDict

def trend_consecutive_n_days(featureCollection, targetDate, numberOfDays):
    """Computes the new indicator as trend for prior consecutive days, internally tests are run, e.g. if a previous year is available or not

    Args:
        featureCollection (FeatureCollection): a valid FeatureCollection, whose features must contain a properties attribute storing the indicator time series according to kommonitors data model
        targetDate (string): the reference/target date in the string format 'YYYY-MM-DD', e.g. '2024-01-01'
        numberOfDays (int): the number of prior consecutive days for which the trend shall be computed.

    Returns:
        Dict<string, float>: returns the dict of all input features whose trend value were successfully computed. ResponseDict may bei smaller than the submitted feature collection. If the feature collection contains values which cannot be converted in a float value the result is 'None'.
    """
    dates = []

    for i in range(numberOfDays, 0, -1):
        dates.append(getSubstractNDaysDate_asString(targetDate, i))
    
    dates.append(targetDate)

    resultDict = {}

    for feature in featureCollection["features"]:
        trend = computeTrend(feature, dates)
        if bool(trend) and not isNoDataValue(trend):
            resultDict[getSpatialUnitFeatureIdValue(feature)] = trend

    if len(resultDict) == 0:
        throwError("Trend computation resulted in NoData for each feature")

    return resultDict


def computeTrend(feature, dates):
    """Computes the trend value for the feature considering the submitted array of consecutive dates. Using the formula: 'T  =100 * b / I', where b is the linear regression slope and I is the first indicator value of the time series.

    Args:
        feature (Feature): a valid GeoJSON Feature, that must contain a 'properties' attribute storing the indicator time series according to KomMonitor's data model
        dates (Array<string>): array of dates for which the trend value shall be computed as string of format 'YYYY-MM-DD' in increasing order, i.e. ["2015-12-31", "2016-12-31", "2017-12-31"]

    Returns:
        float: returns the trend value of the feature considering the concrete consecutive years of dates array. or 'null' if any date of dates array is not included within feature
    """
    indicatorValueArray = []

    # build array of indicator values corresponding to dates array
    for date in dates:
        indicatorValue = getIndicatorValue(feature, date)
        if not isNoDataValue(indicatorValue) and not math.isnan(indicatorValue):
            indicatorValueArray.append(indicatorValue)
        else:
            indicatorValueArray.append(None)

    # make sure that feature has relevant date properties
    if not len(dates) == len(indicatorValueArray):
        throwError("The length of the Array containing the dates and indicator values are not identical.")
    
    timeAxisArray = []

    for i in range(len(dates)):
        timeAxisArray.append(i + 1)
      
    try:
        # compute linear regression slope
        linearRegressionSlope = computeLinearRegressionSlope(indicatorValueArray, timeAxisArray)
        firstYearValue = float(getIndicatorValue(feature, dates[0]))
        
        if firstYearValue == 0:
            return None


        trend_percent = 100 * (linearRegressionSlope / firstYearValue)
        return trend_percent
    except:
        log("Error during trend computation, Returning None")
        return None
    

def computeLinearRegressionSlope(indicatorValueArray, daysArray):
    """Computes the slope of a linear regression using the following formula: 'b = sum((A - Amean) * (I - Imean)) / sum((A - Amean)^2)'. Where A are the consecutive years and I are the indicator Values.

    Args:
        indicatorValueArray (Array<float>): numeric indicator value array representing the time series in increasing order.
        daysArray (Array<float>): numeric value array containing consecutive years in increasing order, i.e. [2015,2016,2017,2018,2019] 

    Returns:
        float: returns the linear regression slope of the submitted indicator time series. The input Arrays should have the same length otherwise the result is 'None'.
    """
    if not len(indicatorValueArray) == len(daysArray):
        log("Error during Pearson Correlation. Lengths of input arrays are not equal.")
        return None
    
    indicatorValueArray = convertPropertyArrayToNumberArray(indicatorValueArray)
    daysArray = convertPropertyArrayToNumberArray(daysArray)

    if not len(indicatorValueArray) == len(daysArray):
        log("Error during Pearson Correlation. Input array(s) contain non numeric values.")
        return None
    
    A_mean = mean(daysArray)
    B_mean = mean(indicatorValueArray)
    sumAB = 0
    sumA2 = 0

    for i in range(len(indicatorValueArray)):
        if bool(indicatorValueArray[i]) and bool(daysArray[i]):
            a_NextValue = daysArray[i] - A_mean
            b_NextValue = indicatorValueArray[i]  - B_mean

            sumAB = sumAB + float(a_NextValue * b_NextValue)
            sumA2 = sumA2 + float(a_NextValue * a_NextValue)

    if sumA2 == 0:
        return None

    return float(sumAB / sumA2)     

def computeContinuity(feature, dates):
    """Computes the pearson correlation for the feature considering the submitted array of consecutive dates.

    Args:
        feature (Feature): a valid GeoJSON Feature, that must contain a 'properties' attribute storing the indicator time series according to KomMonitor's data model
        dates (Array<string>): array of dates for which the continuity value shall be computed as string of format 'YYYY-MM-DD' in increasing order, i.e. ["2015-12-31", "2016-12-31", "2017-12-31"]

    Returns:
        float: returns the continuity value for the feature, at this moment the continuity value is the pearson correlation value calculated with the following formula 'sum((Xi - Xmean) * (Yi - Ymean)) / sqrt(sum(Xi - Xmean)^2 * sum(Yi - Ymean)^2)'
    """
    indicatorValueArray = []
    countArray = []

    for date in dates: 
        indicatorValue = getIndicatorValue(feature, date)
        if bool(indicatorValue) and not isNoDataValue(indicatorValue) and not math.isnan(float(indicatorValue)):
            indicatorValueArray.append(indicatorValue)

    if not len(dates) == len(indicatorValueArray):
        throwError("Error during Pearson Correlation. Length of input arrays are not equal.")
        return None

    for i in range(len(dates), 0, -1):
        countArray.append(i)

    result = stats.pearsonr(indicatorValueArray, countArray)

    return float(result[0])

def continuity_consecutive_n_years(feature, targetDate, numberOfYears):
    """computes the new Indicator as continuity for prior consecutive years. The formula used is the pearson correlation.

    Args:
        feature (Feature): a valid GeoJSON Feature,which must contain a 'properties' attribute storing the indicator time series according to Kommonitors data model.
        targetDate (string): the reference/target date in the string format 'YYYY-MM-DD', e.g. '2018-01-01'
        numberOfYears (int): the number of prior consecutive years for which the continuity shall computed

    Returns:
        Dict<string, float>: returns the dict of all input features whose continuity value were successfully computed. responseMap.size may be smaller than featureCollection.features.size, if featureCollection contains boolean value items or items whose Number-conversion result in Number.NaN
    """
    dates = []

    for i in range(numberOfYears, 0, -1):
        dates.append(getSubstractNYearsDate_asString(targetDate, i))
    
    dates.append(targetDate)

    trend = computeContinuity(feature, dates)
    if not bool(trend) or isNoDataValue(trend):
        throwError(f"Trend computation resulted in NoData for feature {getSpatialUnitFeatureIdValue(feature)}")
    
    return trend

def continuity_consecutive_n_months(feature, targetDate, numberOfMonths):
    """computes the new Indicator as continuity for prior consecutive months. The formula used is the pearson correlation.

    Args:
        feature (Feature): a valid GeoJSON Feature,which must contain a 'properties' attribute storing the indicator time series according to Kommonitors data model.
        targetDate (string): the reference/target date in the string format 'YYYY-MM-DD', e.g. '2018-01-01'
        numberOfMonths (int): the number of prior consecutive Months for which the continuity shall computed

    Returns:
        Dict<string, float>: returns the dict of all input features whose continuity value were successfully computed. responseMap.size may be smaller than featureCollection.features.size, if featureCollection contains boolean value items or items whose Number-conversion result in Number.NaN
    """
    dates = []

    for i in range(numberOfMonths, 0, -1):
        dates.append(getSubstractNMonthsDate_asString(targetDate, i))
    
    dates.append(targetDate)

    trend = computeContinuity(feature, dates)
    if not bool(trend) or isNoDataValue(trend):
        throwError(f"Trend computation resulted in NoData for feature {getSpatialUnitFeatureIdValue(feature)}")
    
    return trend

def continuity_consecutive_n_days(feature, targetDate, numberOfDays):
    """computes the new Indicator as continuity for prior consecutive days. The formula used is the pearson correlation.

    Args:
        feature (Feature): a valid GeoJSON Feature,which must contain a 'properties' attribute storing the indicator time series according to Kommonitors data model.
        targetDate (string): the reference/target date in the string format 'YYYY-MM-DD', e.g. '2018-01-01'
        numberOfDays (int): the number of prior consecutive days for which the continuity shall computed

    Returns:
        Dict<string, float>: returns the dict of all input features whose continuity value were successfully computed. responseMap.size may be smaller than featureCollection.features.size, if featureCollection contains boolean value items or items whose Number-conversion result in Number.NaN
    """
    dates = []

    for i in range(numberOfDays, 0, -1):
        dates.append(getSubstractNDaysDate_asString(targetDate, i))
    
    dates.append(targetDate)

    trend = computeContinuity(feature, dates)
    if not bool(trend) or isNoDataValue(trend):
        throwError(f"Trend computation resulted in NoData for feature {getSpatialUnitFeatureIdValue(feature)}")
    
    return trend


#TODO

# Process Parameter (Objekt oder Dictionary)

# prefect get_run_logger() schon im KmHelper (schonmal vorbereiten)



    

