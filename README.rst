This project contains the API for the Swarm Intelligence platform.


Environment setup
=================


Python
------

It is highly recommended to run everything in an up-to-date virtualenv.
The environment can be set up using:

.. code-block:: sh

    $ mkvirtualenv si --python=python3.5 -a .

In order to run or deploy the project, it is necessary to download the
dependencies:

.. code-block:: sh

    $ pip install -r requirements.txt


Running
=======

The project can be run normally using:

.. code-block:: sh

    $ XXX


Tests
=====

In order to run tests, :pypi:`tox` need to be installed first:

.. code-block:: sh

    $ pip install tox


Test can now be run using:

.. code-block:: sh

    $ tox
