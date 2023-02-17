#!/usr/bin/env python3
# Copyright (C) 2023 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import pytest
import requests

from cmk.special_agents import agent_aws_health

RSS_STR = """
<rss version="2.0">
  <channel>
    <title><![CDATA[Amazon Web Services Service Status]]></title>
    <link>http://status.aws.amazon.com/</link>
    <language>en-us</language>
    <lastBuildDate>Thu, 16 Feb 2023 00:05:51 PST</lastBuildDate>
    <generator>AWS Service Health Dashboard RSS Generator</generator>
    <description><![CDATA[Amazon Web Services Service Status]]></description>
    <ttl>5</ttl>
    <!-- You seem to care about knowing about your events, why not check out https://docs.aws.amazon.com/health/latest/ug/getting-started-api.html -->


  </channel>
</rss>
"""


def test_write_sections(capsys: pytest.CaptureFixture[str]) -> None:
    # Assemble
    def _get_rss() -> requests.Response:
        response = requests.Response()
        response._content = RSS_STR.encode("utf-8")
        return response

    args = agent_aws_health.parse_arguments([])

    # Act
    agent_aws_health.write_section(args, get_rss=_get_rss)
    # Assert
    captured = capsys.readouterr()
    assert captured.out.split("\n") == [
        "<<<aws_health:sep(0)>>>",
        agent_aws_health.AgentOutput(rss_str=RSS_STR).json(),
        "",
    ]
    assert captured.err == ""
