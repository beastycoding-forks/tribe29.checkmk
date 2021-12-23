#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.gui.i18n import _
from cmk.gui.plugins.wato.utils import (
    CheckParameterRulespecWithoutItem,
    rulespec_registry,
    RulespecGroupCheckParametersApplications,
)
from cmk.gui.valuespec import CascadingDropdown, Dictionary, Percentage, Tuple


def _parameter_valuespec_cpu():
    return Dictionary(
        help=_(
            "Here you can configure percentual levels for CPU request "
            "utilization and CPU limit utilization, respectively."
        ),
        title=_("CPU"),
        elements=[
            (
                "request",
                CascadingDropdown(
                    title=_("Upper levels for request utilization"),
                    choices=[
                        (
                            "perc_used",
                            _("Percentual levels"),
                            Tuple(
                                elements=[
                                    Percentage(title=_("Warning at"), default_value=80.0),
                                    Percentage(title=_("Critical at"), default_value=90.0),
                                ]
                            ),
                        ),
                        ("ignore", _("Do not impose levels")),
                    ],
                    default_value="ignore",
                ),
            ),
            (
                "limit",
                CascadingDropdown(
                    title=_("Upper levels for limit utilization"),
                    choices=[
                        (
                            "perc_used",
                            _("Percentual levels"),
                            Tuple(
                                elements=[
                                    Percentage(title=_("Warning at"), default_value=80.0),
                                    Percentage(title=_("Critical at"), default_value=90.0),
                                ]
                            ),
                        ),
                        ("ignore", _("Do not impose levels")),
                    ],
                    default_value="ignore",
                ),
            ),
        ],
    )


rulespec_registry.register(
    CheckParameterRulespecWithoutItem(
        check_group_name="kube_cpu_usage",
        group=RulespecGroupCheckParametersApplications,
        parameter_valuespec=_parameter_valuespec_cpu,
        title=lambda: _("Kubernetes CPU resource utilization"),
    )
)
