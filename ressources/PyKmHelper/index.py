"""
import necessary Node Module Dependencies


"""
import geojson.feature
from scipy import stats
import geopandas as gpd
import requests
import logging
import geojson
import math
import shapely

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
    """Acuires the process parameter with the name 'parameterName' from the submitted processParameters Dictionary 

    Args:
        parameterName (string): the name of the process parameter
        processParameters (Dict<string, (string|number|boolean)>>): an dictionary containing keys and values whereas key='name' and value='paramter value' representing variable additional process parameters that are required to perform the indicator computation.

    Raises:
        Exception: if the dict does not contain a parameter with given name

    Returns:
        String: returns the values of the requested process Parameter as String. Useres should know the real type i. e. boolean or number
    """
    if parameterName in processParameters:
        return str(processParameters[parameterName])
    else:        
        throwError(f"Tried to acquire a process parameter with name '{parameterName}', but the Dictionary of processParameters does not contain such an entry")

def getProcessParameterByName_asNumber(parameterName, processParameters):
    """Acuires the process parameter with the name 'parameterName' from the submitted processParameters Dictionary 

    Args:
        parameterName (string): the name of the process parameter
        processParameters (Dict<string, (string|number|boolean)>>): an dictionary containing keys and values whereas key='name' and value='paramter value' representing variable additional process parameters that are required to perform the indicator computation.

    Raises:
        Exception: if the dict does not contain a parameter with given name
        ValueError: if the parameter Value could not be resolved to type number

    Returns:
        Float: returns the values of the requested process Parameter as Float.
    """
    if parameterName in processParameters:
        try:
            return float(processParameters[parameterName])
        except ValueError:
            raise ValueError("Error while parsing parameter value '" + str(processParameters[parameterName]) + "' from parameter with name '" + str(parameterName) + "' as Number.")
    else:
        throwError(f"Tried to acquire a process parameter with name '" + str(parameterName) + "', but the list of processParameters does not contain such an entry")
    
def getProcessParameterByName_asBoolean(parameterName, processParameters):
    """Acuires the process parameter with the name 'parameterName' from the submitted processParameters Dictionary 

    Args:
        parameterName (string): the name of the process parameter
        processParameters (Dict<string, (string|number|boolean)>>): an dictionary containing keys and values whereas key='name' and value='paramter value' representing variable additional process parameters that are required to perform the indicator computation.

    Raises:
        Exception: if the dict does not contain a parameter with given name
        ValueError: if the parameter Value could not be resolved to type boolean

    Returns:
        Boolean: returns the values of the requested process Parameter as bool.
    """
    if parameterName in processParameters:
        try:
            return eval(processParameters[parameterName])
        except NameError:
            raise NameError("Error while parsing parameter value '" + str(processParameters[parameterName]) + "' from parameter with name '" + str(parameterName) + "' as Boolean.")
    else:
        throwError(f"Tried to acquire a process parameter with name '" + str(parameterName) + "', but the list of processParameters does not contain such an entry")
    
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
    print(logMessage)
    # TODO: ProgressHelperService and Docstring

def logError(logMessage):
    raise Exception(logMessage)
    # TODO: ProgressHelperService and Docstring

def throwError(message):
    """Throw an Error Object with a custom Messgae

    Args:
        message (string): the custom message the error should contain

    Raises:
        Exception: throws the exception
    """
    raise Exception(message)


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
    
    indicatorValue = feature["properties"][targetDateWithPrefix]

    if indicatorValue is None:
        return None
    else:
        return indicatorValue
    
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
        log("No feature of the featureCollection contains a property value for the specified propertyName " + str(propertyName) + ". Thus return null.")
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

    targetDateWithPrefix = getTargetDateWithPropertyPrefix()

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
    if math.isnan(value) or value == None:
        return True
    else:
        return False

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
    

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
API_HELPER_METHODS_GEOMETRIC_OPERATIONS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# class gdf:
#     def __init__(self, input):
#         self.gdf = geoJSONtoGDF(input)
#         self.geoJsonType = input["type"]

    
def geoJSONtoGDF(geoJSON):
    """writes the submitted GeoJSON 'Feature' or 'FeatureCollection' to a GeoPandas GeoDataFrame.

    Args:
        geojson (Feature|FeatureCollection): must be a correct feature or featureCollection

    Returns:
        GeoDataFrame: returns a GeoDataFrame containing a row with properties and geometry for every submitted Feature.
    """
    #TODO: erweitern für GeoJSON Geometrie (außerhalb von Feature und FeatureCollection)?
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
    try:    
        if geom.geom_type == "Point":
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
    return gdf.area

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

def center_geometric(geoJSON):
    """compute the geometric center of the submitted geoJSON geometries. When more than one Feature is submitted it computes the total boundary rectangle and its center. 

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

def center_mass():
    #TODO: braucht man wirklich alle drei Funktionen?
    return None

def centroid():
    #TODO: 
    return None

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

def nearesPoint_directDistance(targetPoint, pointCollection):
    #TODO
    return None


def distance_waypath_kilometers():
    #TODO: Take a look at OpenRouteService  
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




#TODO

# arbeitet Kommonitor nur mit features und featurecollections oder auch rohen geojson geometrien

# braucht man ein object für Process Parameters oder genügt ein dictionary, weil eigentlich sind die ja auch nichts anderes als key value pairs also ist das array im moment doch überflüssig


    

