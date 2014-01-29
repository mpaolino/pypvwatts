=========
pypvwatts
=========

A NREL PVWAtts API Python wrapper.

API Doc: http://developer.nrel.gov/docs/solar/pvwatts-v4/

This library provides shortcuts for all response output fields, all can be
accessed as a result property.

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


Errors
------

All API errors are reported via JSON response, using the errors field.


    >>> from pypvwatts import PVWatts
    >>> result = PVWatts.request(system_size=4, dataset='tmy2', derate=0.77, lat=40, lon=-105)
    >>> result.errors
    [u'You have exceeded your rate limit. Try again later or contact us at http://developer.nrel.gov/contact for assistance']


All other service errors, such as connectivity are reported using Request's exceptions.


Tests
-----

Unit tests are provided in test.py

Author: Miguel Paolino <mpaolino@gmail.com>
