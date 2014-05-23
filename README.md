[![Build Status](https://travis-ci.org/mpaolino/pypvwatts.svg?branch=master)](https://travis-ci.org/mpaolino/pypvwatts)
=========
pypvwatts
=========

A NREL PVWAtts API v4 thin Python wrapper built around requests library.

Developed by <http://renooble.com>.



PVWatts API v4 Documentation: <http://developer.nrel.gov/docs/solar/pvwatts-v4/>

Python requests library: <http://docs.python-requests.org/en/latest/>


Installing
----------

pypvwatts can be installed using distutils/setuptools, either using the setup.py included or directly over PyPi package repository:


Using PyPi


    $ pip install pypvwatts


Download the tarball, unpack and then run setup.py


    $ python setup.py install


Usage - with class methods
--------------------------


    >>> from pypvwatts import PVWatts
    >>> PVWatts.api_key = 'myapikeyHLM6x2In2KmX4fxsTRRBT2r9KfDagJjU'
    >>> result = PVWatts.request(system_size=4, dataset='tmy2', derate=0.77, lat=40, lon=-105)
    >>> result.ac_annual
    7607.97607421875    

Usage - with instance methods
-----------------------------


    >>> from pypvwatts import PVWatts
    >>> p = PVWatts(api_key='myapikeyHLM6x2In2KmX4fxsTRRBT2r9KfDagJjU')
    >>> result = p.request(system_size=4, dataset='tmy2', derate=0.77, lat=40, lon=-105)
    >>> result.ac_annual
    7607.97607421875    


Request parameters and responses
--------------------------------

All request parameters correspond to NREL PVWatts API parameters.

This library provides shortcuts for all response output fields, all can be
accessed as a result property.

Please refer to NREL PVWatts documentation for further details.

http://developer.nrel.gov/docs/solar/pvwatts-v4/

Raw data
--------

Raw result data can be queried using the result.raw attribute.


    >>> from pypvwatts import PVWatts
    >>> result = PVWatts.request(system_size=4, dataset='tmy2', derate=0.77, lat=40, lon=-105)
    >>> result.raw
    {u'errors': [u'You have exceeded your rate limit. Try again later or contact us at http://developer.nrel.gov/contact for assistance']}


Errors
------

All API errors are reported via JSON response, using the errors attribute.


    >>> from pypvwatts import PVWatts
    >>> result = PVWatts.request(system_size=4, dataset='tmy2', derate=0.77, lat=40, lon=-105)
    >>> result.errors
    [u'You have exceeded your rate limit. Try again later or contact us at http://developer.nrel.gov/contact for assistance']


All parameters feeded to make the request are validated, all validations follow the restrictions documented in NREL v4 API docs at <http://developer.nrel.gov/docs/solar/pvwatts-v4/>.  All validation errors will be raised with *pypvwatts.pvwattserror.PVWattsValidationError* exception.

pypvwatts does not try to hide the fact is a thin wrapper around requests library so all other service errors such as connectivity or timeouts are raised as requests library exceptions <http://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions>.


Tests
-----

Simple tests are provided in test.py. Run them with:

    $ python -m unittest pypvwatts.test

Changelog
---------

1.1.1 - Updated copyright notice

1.1.0 - Minor import fix and README update

1.0.0 - First release

Author: Miguel Paolino <mpaolino@gmail.com> - Copyright <http://renooble.com>
