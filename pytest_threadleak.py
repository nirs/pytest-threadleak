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
    return (item.config.getoption("threadleak") or
            item.config.getini("threadleak"))


def current_threads():
    return frozenset(threading.enumerate())


def sorted_by_name(threads):
    return sorted(threads, key=operator.attrgetter("name"))
