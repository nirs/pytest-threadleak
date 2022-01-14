# SPDX-FileCopyrightText: Nir Soffer <nirsof@gmail.com>
#
# SPDX-License-Identifier: MIT

import operator
import threading
import pytest


def pytest_addoption(parser):
    group = parser.getgroup('threadleak')
    group.addoption(
        '--threadleak',
        action='store_true',
        dest='threadleak',
        default=False,
        help='Detect tests leaking threads')
    parser.addini(
        'threadleak',
        'Detect thread leak (default: False)',
        type="bool",
        default=False)


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "threadleak(enabled=True): enable or disable the threadleak plugin",
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    start_threads = None
    if is_enabled(item):
        start_threads = current_threads()
    yield
    if start_threads:
        leaked_threads = current_threads() - start_threads
        if leaked_threads:
            pytest.fail("Test leaked %s" % sorted_by_name(leaked_threads))


def is_enabled(item):
    """
    Test can enabled via config file, command line option, module marker, class
    marker, and function marker. The most specific settings wins.
    """
    marker = item.get_closest_marker(name='threadleak')
    if marker:
        check_marker(marker)
        return marker.kwargs.get("enabled", True)

    return (item.config.getoption("threadleak") or
            item.config.getini("threadleak"))


def check_marker(marker):
    """
    Help users deal with typos by failing if called incorrectly.
    """
    if marker.args:
        raise ValueError(
            "Unexpected threadleak args: {}".format(marker.args))

    if marker.kwargs and list(marker.kwargs) != ["enabled"]:
        raise ValueError(
            "Unexpected threadleak kwargs: {}".format(marker.kwargs))


def current_threads():
    return frozenset(threading.enumerate())


def sorted_by_name(threads):
    return sorted(threads, key=operator.attrgetter("name"))
