# SPDX-FileCopyrightText: Nir Soffer <nirsof@gmail.com>
#
# SPDX-License-Identifier: MIT

import pytest

pytest_plugins = "pytester"

LEAKING_TEST = """
import threading
import time
import pytest

{function_marker}
def test_leak():
    for i in range(2):
        t = threading.Thread(
            target=time.sleep,
            args=(0.5,),
            name="leaked-thread-%d" % i)
        t.daemon = True
        t.start()
"""

INI_ENABLED = """
[pytest]
threadleak = True
"""

INI_DISABLED = """
[pytest]
threadleak = False
"""

def make_source(function_marker=""):
    return LEAKING_TEST.format(function_marker=function_marker)


def test_leak_enabled_option(testdir):
    testdir.makepyfile(make_source())
    result = testdir.runpytest('--threadleak', '-v')
    result.stdout.fnmatch_lines([
        '*::test_leak FAILED*',
        '*Failed: Test leaked *leaked-thread-0*leaked-thread-1*',
    ])
    assert result.ret == 1


def test_leak_enabled_ini(testdir):
    testdir.makeini(INI_ENABLED)
    testdir.makepyfile(make_source())
    result = testdir.runpytest('-v')
    result.stdout.fnmatch_lines([
        '*::test_leak FAILED*',
        '*Failed: Test leaked *leaked-thread-0*leaked-thread-1*',
    ])
    assert result.ret == 1


def test_leak_option_overrides_ini(testdir):
    testdir.makeini(INI_DISABLED)
    testdir.makepyfile(make_source())
    result = testdir.runpytest('--threadleak', '-v')
    result.stdout.fnmatch_lines([
        '*::test_leak FAILED*',
        '*Failed: Test leaked *leaked-thread-0*leaked-thread-1*',
    ])
    assert result.ret == 1


def test_leak_disabled(testdir):
    testdir.makepyfile(make_source())
    result = testdir.runpytest('-v')
    result.stdout.fnmatch_lines(['*::test_leak PASSED*'])
    assert result.ret == 0


def test_leak_disabled_ini(testdir):
    testdir.makeini(INI_DISABLED)
    testdir.makepyfile(make_source())
    result = testdir.runpytest('-v')
    result.stdout.fnmatch_lines(['*::test_leak PASSED*'])
    assert result.ret == 0


def test_leak_disabled_marker(testdir):
    testdir.makeini(INI_ENABLED)
    testdir.makepyfile(make_source(
        function_marker="@pytest.mark.threadleak(enabled=False)"))
    result = testdir.runpytest('-v')
    result.stdout.fnmatch_lines(['*::test_leak PASSED*'])
    assert result.ret == 0


@pytest.mark.parametrize("marker", ["threadleak", "threadleak(enabled=True)"])
def test_leak_enabled_marker(testdir, marker):
    testdir.makeini(INI_DISABLED)
    testdir.makepyfile(make_source(
        function_marker="@pytest.mark.{}".format(marker)))
    result = testdir.runpytest('-v')
    result.stdout.fnmatch_lines([
        '*::test_leak FAILED*',
        '*Failed: Test leaked *leaked-thread-0*leaked-thread-1*',
    ])
    assert result.ret == 1


def test_unexpected_marker_args(testdir):
    testdir.makeini(INI_DISABLED)
    testdir.makepyfile(make_source(
        function_marker="@pytest.mark.threadleak('unexpected')"))
    result = testdir.runpytest('-v')
    result.stdout.fnmatch_lines([
        '*::test_leak FAILED*',
        "*ValueError: Unexpected threadleak args: ('unexpected',)"
    ])
    assert result.ret == 1


def test_unexpected_marker_kwargs(testdir):
    testdir.makeini(INI_DISABLED)
    testdir.makepyfile(make_source(
        function_marker="@pytest.mark.threadleak(unexpected=True)"))
    result = testdir.runpytest('-v')
    result.stdout.fnmatch_lines([
        '*::test_leak FAILED*',
        "*ValueError: Unexpected threadleak kwargs: {'unexpected': True}"
    ])
    assert result.ret == 1

def test_no_leak(testdir):
    testdir.makepyfile("""
        def test_no_leak():
            pass
    """)
    result = testdir.runpytest('--threadleak', '-v')
    result.stdout.fnmatch_lines(['*::test_no_leak PASSED*'])
    assert result.ret == 0


def test_help_message(testdir):
    result = testdir.runpytest('--help')
    result.stdout.fnmatch_lines([
        'threadleak:',
        '*--threadleak*Detect tests leaking threads',
    ])
