# SPDX-FileCopyrightText: Nir Soffer <nirsof@gmail.com>
#
# SPDX-License-Identifier: MIT

import operator
import re
import threading

import pytest


def pytest_addoption(parser):
    group = parser.getgroup("threadleak")
    group.addoption(
        "--threadleak",
        action="store_true",
        dest="threadleak",
        default=False,
        help="Detect tests leaking threads",
    )
    parser.addini(
        "threadleak", "Detect thread leak (default: False)", type="bool", default=False
    )
    parser.addini("threadleak_exclude", "Regex of thread names to exclude")
    parser.addini(
        "threadleak_exclude_daemons",
        "When True, ignores leaked daemon threads",
        type="bool",
        default=False,
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "threadleak(enabled=True): enable or disable the threadleak plugin",
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    enabled = is_enabled(item)
    if enabled:
        exclude_regex = get_exclude_regex(item)
        exclude_daemons = is_exclude_daemons(item)
        start_threads = current_threads(exclude_regex, exclude_daemons)
    yield
    if enabled:
        end_threads = current_threads(exclude_regex, exclude_daemons)
        leaked_threads = end_threads - start_threads
        if leaked_threads:
            pytest.fail("Test leaked %s" % sorted_by_name(leaked_threads))


def is_enabled(item):
    """
    Test can enabled via config file, command line option, module marker, class
    marker, and function marker. The most specific settings wins.
    """
    marker = item.get_closest_marker(name="threadleak")
    if marker:
        check_marker(marker)
        return marker.kwargs.get("enabled", True)

    return item.config.getoption("threadleak") or item.config.getini("threadleak")


def get_exclude_regex(item):
    marker = item.get_closest_marker(name="threadleak")
    if marker:
        return marker.kwargs.get("exclude")
    return item.config.getini("threadleak_exclude")


def is_exclude_daemons(item):
    marker = item.get_closest_marker(name="threadleak")
    if marker:
        return marker.kwargs.get("exclude_daemons", False)
    return item.config.getini("threadleak_exclude_daemons")


def check_marker(marker):
    """
    Help users deal with typos by failing if called incorrectly.
    """
    if marker.args:
        raise ValueError("Unexpected threadleak args: {}".format(marker.args))

    expected_keys = frozenset(["enabled", "exclude", "exclude_daemons"])
    unexpected_kwargs = {}
    for key, value in marker.kwargs.items():
        if key not in expected_keys:
            unexpected_kwargs[key] = value

    if unexpected_kwargs:
        raise ValueError("Unexpected threadleak kwargs: {}".format(unexpected_kwargs))


def current_threads(exclude_regex=None, exclude_daemons=False):
    threads = threading.enumerate()

    if exclude_regex:
        threads = [
            thread for thread in threads if not re.match(exclude_regex, thread.name)
        ]

    if exclude_daemons:
        threads = [thread for thread in threads if not thread.daemon]

    return frozenset(threads)


def sorted_by_name(threads):
    return sorted(threads, key=operator.attrgetter("name"))
