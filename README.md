=========
pypvwatts
=========

A NREL PVWAtts API v4 Python wrapper.

Installing
----------

There are two ways


Using PIP


    $ pip install pypvwatts


Using setup.py


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


All other service errors, such as connectivity are raised as request's python library exceptions.


Tests
-----

Unit tests are provided in test.py


Changelog
---------

1.0.0 - First release

Author: Miguel Paolino <mpaolino@gmail.com>
