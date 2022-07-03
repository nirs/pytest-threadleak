.. SPDX-FileCopyrightText: Nir Soffer <nirsof@gmail.com>
..
.. SPDX-License-Identifier: MIT

=================
pytest-threadleak
=================

.. image:: https://img.shields.io/pypi/v/pytest-threadleak.svg
    :target: https://pypi.python.org/pypi/pytest-threadleak
    :alt: Current version
.. image:: https://img.shields.io/pypi/pyversions/pytest-threadleak
    :target: https://pypi.python.org/pypi/pytest-threadleak
    :alt: Supports Python 2.7, 3.10, 3.9, 3.8, 3.7, 3.7
.. image:: https://img.shields.io/pypi/dm/pytest-threadleak
    :target: https://pypi.python.org/pypi/pytest-threadleak
    :alt: Downloads per month
.. image:: https://github.com/nirs/pytest-threadleak/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/nirs/pytest-threadleak/actions/workflows/ci.yml
    :alt: Tests status
.. image:: https://img.shields.io/pypi/l/pytest-threadleak
    :target: https://pypi.python.org/pypi/pytest-threadleak
    :alt: MIT license


Detects tests leaking threads
=============================

Installation
------------

You can install "pytest-threadleak" via `pip`_ from `PyPI`_::

    $ pip install pytest-threadleak


Usage
-----

The threadleak pytest plugin will fail leaking threads. This can be an issue in
the test, or in the tested code.

Here is an example leaking test::

    $ cat leak_test.py
    import threading
    import time

    def test_leak():
        threading.Thread(target=time.sleep, args=(1,)).start()

Here is an example run with thread leak plugin enabled::

    $ pytest --threadleak leak_test.py
    ...
    leak_test.py::test_leak FAILED
    ...
    >   ???
    E   Failed: Test leaked [<Thread(Thread-1, started 139762716391168)>]

If you want to enable thread leak by default, you can enable it in your
pytest.ini or tox.ini::

    [pytest]
    threadleak = True

If you want to enable thread leak on a per test/module basis, you can
use the `threadleak` pytest marker:

To enable it for a single test::

    @pytest.mark.threadleak
    def test_leak():
       ...

To disable it for a single test::

    @pytest.mark.threadleak(enabled=False)
    def test_leak():
       ...

For an entire test module::

    import pytest

    pytestmark = pytest.mark.threadleak(enabled=False)

If you want to exclude some threads from the leak check, you can specify a
regex to match excluded thread names::

    [pytest]
    threadleak = True
    threadleak_exclude = pool/\d+

Contributing
------------

Running the tests::

    $ tox


License
-------

Distributed under the terms of the `MIT`_ license, "pytest-threadleak" is free
and open source software


Credits
-------

This `Pytest`_ plugin was generated with `Cookiecutter`_ along with
`@hackebrot`_'s `Cookiecutter-pytest-plugin`_ template.


.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.python.org/pypi/pip/
.. _`PyPI`: https://pypi.python.org/pypi
