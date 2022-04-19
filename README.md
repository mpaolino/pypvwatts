pypvwatts
=========

[![Build Status](https://travis-ci.org/mpaolino/pypvwatts.svg?branch=master)](https://travis-ci.org/mpaolino/pypvwatts)

A NREL PVWAtts API v6 thin Python wrapper built around requests library.

Originally developed by <http://renooble.com>.

Github repository: <https://github.com/mpaolino/pypvwatts>


PVWatts API v6 Documentation: <https://developer.nrel.gov/docs/solar/pvwatts/v6/>

Python requests library: <http://docs.python-requests.org/en/latest/>

Supports
--------

Python 2 & Python 3

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
    >>> PVWatts.api_key = 'myapikey'
    >>> result = PVWatts.request(
            system_capacity=4, module_type=1, array_type=1,
            azimuth=190, tilt=30, dataset='tmy2',
            losses=13, lat=40, lon=-105)
    >>> result.ac_annual
    6683.64501953125

Usage - with instance methods
-----------------------------


    >>> from pypvwatts import PVWatts
    >>> p = PVWatts(api_key='myapikey')
    >>> result = p.request(
            system_capacity=4, module_type=1, array_type=1,
            azimuth=190, tilt=30, dataset='tmy2',
            losses=13, lat=40, lon=-105)
    >>> result.ac_annual
    6683.64501953125


Request parameters and responses
--------------------------------

All request parameters correspond to NREL PVWatts API parameters.

This library provides shortcuts for all response output fields, all can be
accessed as a result property.

Please refer to NREL PVWatts documentation for further details.

https://developer.nrel.gov/docs/solar/pvwatts/v6/

Raw data
--------

Raw result data can be queried using the result.raw attribute.


	>>> from pypvwatts import PVWatts
	>>> PVWatts.api_key = 'DEMO_KEY'
	>>> result = PVWatts.request(
			system_capacity=4, module_type=1, array_type=1,
			azimuth=190, tilt=30, dataset='tmy2',
			losses=13, lat=40, lon=-105)
	>>> print(result.raw)
	{'inputs': {'system_capacity': '4', 'module_type': '1', 'losses': '13', 'array_type': '1', 'tilt': '30', 'azimuth': '190', 'lat': '40', 'lon': '-105', 'dataset': 'tmy2', 'radius': '0','timeframe': 'monthly'}, 'errors': [], 'warnings': [], 'version': '1.1.0', 'ssc_info': {'version': 45, 'build': 'Linux 64 bit GNU/C++ Jul  7 2015 14:24:09'}, 'station_info': {'lat': 40.01666641235352, 'lon': -105.25, 'elev': 1634.0, 'tz': -7.0, 'location': '94018', 'city': 'BOULDER', 'state': 'CO', 'solar_resource_file': '94018.tm2', 'distance': 21235}, 'outputs': {'ac_monthly': [418.8210754394531, 422.0429992675781, 588.85791015625, 586.0773315429688, 612.3723754882812, 598.5872802734375, 595.2975463867188, 597.31396484375, 569.5850219726562, 524.8071899414062, 419.6332397460938, 401.0901184082031], 'poa_monthly': [124.2255630493164, 127.3401947021484, 180.2367248535156, 183.1153717041016, 193.9059143066406, 193.1558837890625, 195.6830749511719, 196.3893127441406, 184.4766387939453, 165.8097991943359, 126.6421508789062, 118.6332244873047], 'solrad_monthly': [4.007276058197021, 4.547863960266113, 5.814087867736816, 6.103845596313477, 6.255029678344727, 6.438529491424561, 6.312357425689697, 6.335139274597168, 6.149221420288086, 5.348703384399414, 4.221405029296875, 3.826878309249878], 'dc_monthly': [437.2481384277344, 441.5818176269531, 617.2501831054688, 614.1566162109375, 639.8923950195312, 625.9356689453125, 622.40185546875, 623.8253173828125, 594.6722412109375, 547.7664794921875, 438.1986389160156, 418.7980346679688], 'ac_annual': 6334.48486328125, 'solrad_annual': 5.446694850921631, 'capacity_factor': 18.07786750793457}}


Errors
------

All API errors are reported via JSON response, using the errors attribute.


    >>> from pypvwatts import PVWatts
    >>> result = PVWatts.request(
            system_capacity=4, module_type=1, array_type=1,
            azimuth=190, tilt=30, dataset='tmy2',
            losses=13, lat=40, lon=-105)
    >>> result.errors
    [u'You have exceeded your rate limit. Try again later or contact us at http://developer.nrel.gov/contact for assistance']


All parameters feeded to make the request are validated, all validations follow the restrictions documented in NREL v6 API docs at <https://developer.nrel.gov/docs/solar/pvwatts/v6/>.
All validation errors will be raised with *pypvwatts.pvwattserror.PVWattsValidationError* exception.

pypvwatts does not try to hide the fact is a thin wrapper around requests library so all other service errors such as connectivity or timeouts are raised as requests library exceptions <http://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions>.


Tests
-----

Simple tests are provided in test.py. Run them with:

    $ python -m unittest pypvwatts.test

Or the preferred way, testing Python 2.7 and Python 3.9 together using tox (you need to install it):
    
    $ tox


Author: Miguel Paolino <miguel@renooble.com>, Hannes Hapke <hannes@renooble.com> - Copyright <http://renooble.com>
