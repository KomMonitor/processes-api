# coding: utf-8

"""
    KomMonitor Data Access API

    erster Entwurf einer Datenzugriffs-API, die den Zugriff auf die KomMonitor-Datenhaltungsschicht kapselt.

    The version of the OpenAPI document: 0.0.1
    Contact: christian.danowski-buhren@hs-bochum.de
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import date
from typing import Any, ClassVar, Dict, List, Optional, Union
from pydantic import BaseModel, StrictFloat, StrictInt
from pydantic import Field
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class IndicatorPUTInputTypeValueMapping(BaseModel):
    """
    IndicatorPUTInputTypeValueMapping
    """ # noqa: E501
    indicator_value: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="the numeric extent of the indicator for the timestamp", alias="indicatorValue")
    timestamp: Optional[date] = Field(default=None, description="timestamp consisting of year, month and day according to ISO 8601 (e.g. 2018-01-30)")
    __properties: ClassVar[List[str]] = ["indicatorValue", "timestamp"]

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of IndicatorPUTInputTypeValueMapping from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={
            },
            exclude_none=True,
        )
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of IndicatorPUTInputTypeValueMapping from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "indicatorValue": obj.get("indicatorValue"),
            "timestamp": obj.get("timestamp")
        })
        return _obj


