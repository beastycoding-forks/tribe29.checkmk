#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, NewType, TypedDict

__all__ = [
    "ServiceName",
    "ContactgroupName",
    "AgentRawData",
    "HostOrServiceConditionRegex",
    "HostOrServiceConditionsSimple",
    "HostOrServiceConditionsNegated",
    "HostOrServiceConditions",
    "CheckPluginNameStr",
    "Item",
    "Seconds",
    "Timestamp",
    "TimeRange",
    "ServiceState",
    "ServiceDetails",
    "ServiceAdditionalDetails",
    "MetricName",
    "LegacyCheckParameters",
    "ParametersTypeAlias",
    "state_markers",
]

ServiceName = str
ContactgroupName = str


AgentRawData = NewType("AgentRawData", bytes)

HostOrServiceConditionRegex = TypedDict(
    "HostOrServiceConditionRegex",
    {"$regex": str},
)
HostOrServiceConditionsSimple = list[HostOrServiceConditionRegex | str]
HostOrServiceConditionsNegated = TypedDict(
    "HostOrServiceConditionsNegated",
    {"$nor": HostOrServiceConditionsSimple},
)

HostOrServiceConditions = (
    HostOrServiceConditionsSimple | HostOrServiceConditionsNegated
)  # TODO: refine type

CheckPluginNameStr = str
Item = str | None


Seconds = int
Timestamp = int
TimeRange = tuple[int, int]

ServiceState = int
ServiceDetails = str
ServiceAdditionalDetails = str

MetricName = str

LegacyCheckParameters = None | Mapping[Any, Any] | tuple[Any, ...] | list[Any] | str | int | bool
ParametersTypeAlias = Mapping[str, Any]  # Modification may result in an incompatible API change.


# Symbolic representations of states in plugin output
# TODO(ml): Should probably be of type enum::int -> str
state_markers = ("", "(!)", "(!!)", "(?)")
