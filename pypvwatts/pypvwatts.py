# coding: utf-8
"""
Python wrapper for NREL PVWatt version 4.
"""
from .pvwattsresult import PVWattsResult
from .pvwattserror import PVWattsError, PVWattsValidationError
import requests
from __version__ import VERSION

import functools


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
    api_key = 'DEMO_KEY'

    def __init__(self, api_key='DEMO_KEY', proxy=None):
        PVWatts.api_key = api_key
        self.proxy = proxy

    @omnimethod
    def validate_system_size(self, system_size):
        if system_size is None:
            return

        if not isinstance(system_size, (int, long, float)):
            raise PVWattsValidationError('system_size must be int, long or float')

        if not (0.05 <= system_size and system_size <= 500000):
            raise PVWattsValidationError('system_size must be >= 0.05 and <= 500000')

        return system_size

    @omnimethod
    def validate_lat(self, lat):
        if lat is None:
            return

        if not isinstance(lat, (int, long, float)):
            raise PVWattsValidationError('lat must be int, long or float')

        if not (-90 <= lat and lat <= 90):
            raise PVWattsValidationError('lat must be >= -90 and <= 90')

        return lat

    @omnimethod
    def validate_lon(self, lon):
        if lon is None:
            return

        if not isinstance(lon, (int, long, float)):
            raise PVWattsValidationError('lon must be int, long or float')

        if not (-180 <= lon and lon <= 180):
            raise PVWattsValidationError('lon must be >= -90 and <= 90')

        return lon

    @omnimethod
    def validate_dataset(self, dataset):
        if dataset is None:
            return

        if not isinstance(dataset, (str, unicode)):
            raise PVWattsValidationError('dataset must be str or unicode')

        if dataset not in ('tmy2', 'tmy3', 'intl'):
            raise PVWattsValidationError('dataset must be \'tmy2\', \'tmy3\' or \'intl\'')

        return dataset

    @omnimethod
    def validate_timeframe(self, timeframe):
        if timeframe is None:
            return

        if not isinstance(timeframe, (str, unicode)):
            raise PVWattsValidationError('timeframe must be str or unicode')

        if timeframe not in ('hourly', 'monthly'):
            raise PVWattsValidationError('dataset must be \'hourly\' or \'monthly\'')

        return timeframe

    @omnimethod
    def validate_azimuth(self, azimuth):
        if azimuth is None:
            return

        if not isinstance(azimuth, (int, long, float)):
            raise PVWattsValidationError('azimuth must be int, long or float')

        if not (0 <= azimuth and azimuth <= 360):
            raise PVWattsValidationError('azimuth must be >= 0 and <= 360')

        return azimuth

    @omnimethod
    def validate_derate(self, derate):
        if derate is None:
            return

        if not isinstance(derate, (int, long, float)):
            raise PVWattsValidationError('derate must be int, long or float')

        if not (0 <= derate and derate <= 1):
            raise PVWattsValidationError('derate must be >= 0 and <= 1')

        return derate

    @omnimethod
    def validate_tilt(self, tilt):
        if tilt is None:
            return

        if not isinstance(tilt, (int, long, float)):
            raise PVWattsValidationError('tilt must be int, long or float')

        return tilt

    @omnimethod
    def validate_tilt_eq_lat(self, tilt_eq_lat):
        if tilt_eq_lat is None:
            return

        if not isinstance(tilt_eq_lat, (int, long, float)):
            raise PVWattsValidationError('tilt_eq_lat must be int, long or float')

        if tilt_eq_lat not in (0, 1):
            raise PVWattsValidationError('tilt_eq_lat must be 0 or 1')

        return tilt_eq_lat

    @omnimethod
    def validate_track_mode(self, track_mode):
        if track_mode is None:
            return

        if not isinstance(track_mode, (int, long, float)):
            raise PVWattsValidationError('track_mode must be int, long or float')

        if track_mode not in (0, 1, 2):
            raise PVWattsValidationError('track_mode must be 0, 1 or 2')

        return track_mode

    @omnimethod
    def validate_inoct(self, inoct):
        if inoct is None:
            return

        if not isinstance(inoct, (int, long, float)):
            raise PVWattsValidationError('inoct must be int, long or float')

        if not (30 <= inoct and inoct <= 80):
            raise PVWattsValidationError('inoct must be >= 30 and <= 80')

        return inoct

    @omnimethod
    def validate_gamma(self, gamma):
        if gamma is None:
            return

        if not isinstance(gamma, (int, long, float)):
            raise PVWattsValidationError('gamma must be int, long or float')

        if not (-2 <= gamma and gamma <= -0.01):
            raise PVWattsValidationError('gamma must be >= -2 and <= -0.01')

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
        :return: JSON object with the data fetched from that URL as a
                 JSON-format object.
        :rtype: (dict or array)

        """
        request = requests.Request('GET',
                                   url=PVWatts.PVWATTS_QUERY_URL,
                                   params=params,
                                   headers={'User-Agent': ''.join(
                                            ['pypvwatts/', VERSION,
                                             ' (Python)'])})

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

        params['api_key'] = PVWatts.api_key

        request = requests.Request('GET',
                                   url=PVWatts.PVWATTS_QUERY_URL,
                                   params=params,
                                   headers={'User-Agent': ''.join(
                                            ['pypvwatts/', VERSION,
                                             ' (Python)'])})

        if self is not None:
            return PVWattsResult(self.get_data(params=params))
        return PVWattsResult(PVWatts.get_data(params=params))
