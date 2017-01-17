************
Installation
************

Getting Started using Ubuntu
============================
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

Prerequisites
-------------

First you need to checkout the GitHub Repository using: ::

	git clone https://github.com/dcentralize/swarm-intelligence.git

It is highly recommended to run everything in an virtualenv. The environment can be set up using: ::

	mkvirtualenv --python python3.4 -a . si

To create a local database, install Mariadb: ::

	apt-get install mariadb-server

In order to run or deploy the project, it is necessary to download the dependencies: ::

	pip3 install -r requirements.txt

Installation
------------

A step by step series of examples that tell you how to get a development env running.

Starting mariadb: ::

	service mariadb start

Setting up the database: ::

	mysql -u root -e 'CREATE DATABASE swarm_intelligence'

Adding the directory 'swarm-intelligence' to your PYTHONPATH: ::

	export PYTHONPATH=$PYTHONPATH:/path/of/swarm-intelligence

You can now navigate to the app.py and run it using: ::

	cd swarm-intelligence
	python3 swarm_intelligence_app/app.py

You can now access the API at localhost:5000. Please not that accessing the API via 127.0.0.1:5000 will not work.

Running the tests
=================
Normally our tests are run using Travis-CI. In order to run the tests locally, navigate to the /tests directory and run: ::

	py.test

Coding style tests
------------------
Our coding style is conform to flake8, except for some minor exceptions which can be found in the tox.ini.

Built With
==========
* [PyCharm](https://www.jetbrains.com/pycharm/)
* [Travis-CI](https://travis-ci.org/)
* [Mariadb](https://mariadb.org/)
* [Flask](http://flask.pocoo.org/docs/0.11/)
* [Flask-Cors](https://github.com/corydolphin/flask-cors)
* [Flask-HTTPAuth](https://flask-httpauth.readthedocs.io/en/latest/)
* [Flask-RESTful](https://flask-restful-cn.readthedocs.io/en/0.3.5/)
* [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.1/)
* [Jinja2](http://jinja.pocoo.org/)
* [PyJWT](http://github.com/jpadilla/pyjwt)
* [PyMySQL](https://media.readthedocs.org/pdf/pymysql/latest/pymysql.pdf)
* [SQLAlchemy](http://www.sqlalchemy.org)
* [SQLAlchemy-Utils](https://github.com/kvesteri/sqlalchemy-utils)
* [Py](https://pypi.python.org/pypi)
* [Pytest](http://doc.pytest.org/en/latest/)
* [Pytest-Flask](https://pytest-flask.readthedocs.io/en/latest/)
* [requests](http://python-requests.org)
* [Tox](https://tox.readthedocs.io/en/latest/)
