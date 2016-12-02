# Swarm Intelligence Plattform

A simple holacracy implementation

## Table of Contents
1. [Getting Started on Linux](#linux)
    1. [Prerequisites](#linuxpre)
    2. [Installing](#linuxinstall)
2. [Running the tests](#test)
    1. [Codingstyle tests](#codingstyle)
3. [Build with](#tools)
4. [Authors](#authors)

## Getting Started using Bash <a name="linux"></a>
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites <a name="linuxpre"></a>
First you need to checkout the GitHub Repository using:
```
git -clone https://github.com/dcentralize/swarm-intelligence.git
```
It is highly recommended to run everything in an virtualenv. The environment can be set up using:
```
mkvirtualenv si --python=python3.4 -a
```
To create a local database, install Mariadb:
```
apt-get install mariadb-server
```
In order to run or deploy the project, it is necessary to download the dependencies:
```
pip3 install -r .travis.requirements.txt
```

### Installing <a name="linuxinstall"></a>
A step by step series of examples that tell you have to get a development env running.

Starting mariadb:
```
service mariadb-server start
```
Setting up the database:
```
mysql -u root -e 'CREATE DATABASE swarm_intelligence'
```
Adding the directory to PYTHONPATH:
```
export PYTHONPATH=$PYTHONPATH:/path/of/directory/
```
You can now navigate to the app.py and run it using:
```
python3 app.py
```
You can now access your application via your browser at localhost:5432.

## Running the tests <a name="tests"></a>
In order to run the tests navigate to the /tests directory and run:
```
py.test
```

### Coding style tests <a name="codingstyle"></a>
Our coding style is conform to flake8, except for some minor exceptions which can be found in the tox.ini.

## Built With <a name="tools"></a>
* [PyCharm](https://www.jetbrains.com/pycharm/)
* [Mariadb](https://mariadb.org/)
* [Flask](http://flask.pocoo.org/docs/0.11/)
* [Flask-RESTful](https://flask-restful-cn.readthedocs.io/en/0.3.5/)
* [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.1/)
* [SQLAlchemy-Utils](https://github.com/kvesteri/sqlalchemy-utils)
* [Flask-HTTPAuth](https://flask-httpauth.readthedocs.io/en/latest/)
* [PyMySQL](https://media.readthedocs.org/pdf/pymysql/latest/pymysql.pdf)
* [Pytest](http://doc.pytest.org/en/latest/)
* [Pytest-Flask](https://pytest-flask.readthedocs.io/en/latest/)
* [Py](https://pypi.python.org/pypi)
* [Tox](https://tox.readthedocs.io/en/latest/)

## Authors <a name="authors"></a>
* **Tobias Wählen**
* **Felix Borst**
* **Andreas Fischer**
* **Marvin Rüsenberg**
* **Moha Messri**
