# coding: utf-8
#
# Miguel Paolino <mpaolino@gmail.com> - 2014
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""
Python wrapper for NREL PVWatt version 4.
"""
from pvwattsresult import PVWattsResult
from pvwattserror import PVWattsError
import requests
from __version__ import VERSION

import functools

__all__ = ['PVWatts', 'PVWattsResult', 'PVWattsError']


# this decorator lets me use methods as both static and instance methods
class omnimethod(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        return functools.partial(self.func, instance)


class PVWatts():
    '''
    A Python wrapper for NREL PVWatts V4.0.0 API
    '''

    PVWATTS_QUERY_URL = 'http://developer.nrel.gov/api/pvwatts/v4.json'

    def __init__(self, api_key='DEMO_KEY', proxy=None):
        self.api_key = api_key
        self.proxy = proxy 

    @omnimethod
    def validate_system_size(self, system_size):
        if system_size == None:
            return

        if not isinstance(system_size, (int, long, float)):
            raise ValueError('system_size must be int, long or float')

        if not (0.05 <= system_size and system_size <= 500000):
            raise ValueError('system_size must be >= 0.05 and <= 500000')

        return system_size

    @omnimethod
    def validate_lat(self, lat):
        if lat == None:
            return

        if not isinstance(lat, (int, long, float)):
            raise ValueError('lat must be int, long or float')

        if not (-90 <= lat and lat <= 90):
            raise ValueError('lat must be >= -90 and <= 90')

        return lat

    @omnimethod
    def validate_lon(self, lon):
        if lon == None:
            return

        if not isinstance(lon, (int, long, float)):
            raise ValueError('lon must be int, long or float')

        if not (-180 <= lon and lon <= 180):
            raise ValueError('lon must be >= -90 and <= 90')

        return lon

    @omnimethod
    def validate_dataset(self, dataset):
        if dataset == None:
            return

        if not isinstance(dataset, (str, unicode)):
            raise ValueError('dataset must be str or unicode')

        if dataset not in ('tmy2', 'tmy3', 'intl'):
            raise ValueError('dataset must be \'tmy2\', \'tmy3\' or \'intl\'')

        return dataset

    @omnimethod
    def validate_timeframe(self, timeframe):
        if timeframe == None:
            return

        if not isinstance(timeframe, (str, unicode)):
            raise ValueError('timeframe must be str or unicode')

        if timeframe not in ('hourly', 'monthly'):
            raise ValueError('dataset must be \'hourly\' or \'monthly\'')

        return timeframe

    @omnimethod
    def validate_azimuth(self, azimuth):
        if azimuth == None:
            return

        if not isinstance(azimuth, (int, long, float)):
            raise ValueError('azimuth must be int, long or float')

        if not (0 <= azimuth and azimuth <= 360):
            raise ValueError('azimuth must be >= 0 and <= 360')

        return azimuth

    @omnimethod
    def validate_derate(self, derate):
        if derate == None:
            return

        if not isinstance(derate, (int, long, float)):
            raise ValueError('derate must be int, long or float')

        if not (0 <= derate and derate <= 1):
            raise ValueError('derate must be >= 0 and <= 1')

        return derate

    @omnimethod
    def validate_tilt(self, tilt):
        if tilt == None:
            return

        if not isinstance(tilt, (int, long, float)):
            raise ValueError('tilt must be int, long or float')

        return tilt

    @omnimethod
    def validate_tilt_eq_lat(self, tilt_eq_lat):
        if tilt_eq_lat == None:
            return

        if not isinstance(tilt_eq_lat, (int, long, float)):
            raise ValueError('tilt_eq_lat must be int, long or float')

        if tilt_eq_lat not in (0, 1):
            raise ValueError('tilt_eq_lat must be 0 or 1')

        return tilt_eq_lat

    @omnimethod
    def validate_track_mode(self, track_mode):
        if track_mode == None:
            return

        if not isinstance(track_mode, (int, long, float)):
            raise ValueError('track_mode must be int, long or float')

        if track_mode not in (0, 1, 2):
            raise ValueError('track_mode must be 0, 1 or 2')

        return track_mode

    @omnimethod
    def validate_inoct(self, inoct):
        if inoct == None:
            return

        if not isinstance(inoct, (int, long, float)):
            raise ValueError('inoct must be int, long or float')

        if not (30 <= inoct and inoct <= 80):
            raise ValueError('inoct must be >= 30 and <= 80')

        return inoct

    @omnimethod
    def validate_gamma(self, gamma):
        if gamma == None:
            return

        if not isinstance(gamma, (int, long, float)):
            raise ValueError('gamma must be int, long or float')

        if not (-2 <= gamma and gamma <= -0.01):
            raise ValueError('gamma must be >= -2 and <= -0.01')

        return gamma

    @property
    def version(self):
        return VERSION

    @omnimethod
    def get_data(self, params={}):
        """
        Retrieve a JSON object from a (parameterized) URL.

        :param params: Dictionary mapping (string) query parameters to values
        :type params: dict
        :return: JSON object with the data fetched from that URL as a JSON-format object.
        :rtype: (dict or array)

        """
        request = requests.Request('GET',
                       url = PVWatts.PVWATTS_QUERY_URL,
                       params = params,
                       headers = {
                            'User-Agent': 'pypvwatts/' + VERSION + ' (Python)'
                       })

        session = requests.Session()

        if self and self.proxy:
            session.proxies = {'https': self.proxy}

        response = session.send(request.prepare())
        session.close()

        if response.status_code == 403:
            raise PVWattsError("Forbidden, 403")
        return response.json()

    @omnimethod
    def request(self, format=None, system_size=None, address=None, lat=None,
                lon=None, file_id=None, dataset='tmy3', timeframe='monthly',
                azimuth=None, derate=None, tilt=None, tilt_eq_lat=0,
                track_mode=1, inoct=None, gamma=None, callback=None):
      
        params = {'format': format,
                  'system_size': PVWatts.validate_system_size(system_size),
                  'address': address,
                  'lat': PVWatts.validate_lat(lat),
                  'lon': PVWatts.validate_lon(lon),
                  'file_id': file_id,
                  'dataset': PVWatts.validate_dataset(dataset),
                  'timeframe': PVWatts.validate_timeframe(timeframe),
                  'azimuth': PVWatts.validate_azimuth(azimuth),
                  'derate': PVWatts.validate_derate(derate),
                  'tilt': PVWatts.validate_tilt(tilt),
                  'tilt_eq_lat': PVWatts.validate_tilt_eq_lat(tilt_eq_lat),
                  'track_mode': PVWatts.validate_track_mode(track_mode),
                  'inoct': PVWatts.validate_inoct(inoct),
                  'gamma': PVWatts.validate_gamma(gamma),
                  'callback': callback}

        if self and self.api_key:
            params['api_key'] = self.api_key
        else:
            params['api_key'] = 'DEMO_KEY'

        request = requests.Request('GET',
                       url = PVWatts.PVWATTS_QUERY_URL,
                       params = params,
                       headers = {
                            'User-Agent': 'pypvwatts/' + VERSION + ' (Python)'
                       })

        if self is not None:
            return PVWattsResult(self.get_data(params=params))
        else:
            return PVWattsResult(PVWatts.get_data(params=params))
