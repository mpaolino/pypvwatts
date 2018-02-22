# coding: utf-8
"""
Unit tests for pypvwatts.

"""
from .pypvwatts import PVWatts, PVWattsResult
from .pvwattserror import PVWattsValidationError

import unittest
import json

SAMPLE_RESPONSE = """
{
   "inputs":{
      "lat":"40",
      "lon":"-105",
      "system_capacity":"4",
      "azimuth":"180",
      "tilt":"40",
      "array_type":"1",
      "module_type":"1",
      "losses":"10"
   },
   "errors":[

   ],
   "warnings":[

   ],
   "version":"1.0.1",
   "ssc_info":{
      "version":34,
      "build":"Unix 64 bit GNU/C++ Aug 18 2014 13:38:36"
   },
   "station_info":{
      "lat":40.016666412353516,
      "lon":-105.25,
      "elev":1634.0,
      "tz":-7.0,
      "location":"94018",
      "city":"BOULDER",
      "state":"CO",
      "solar_resource_file":"94018.tm2",
      "distance":21235
   },
   "outputs":{
      "ac_monthly":[
         474.3351745605469,
         465.9206237792969,
         628.4765625,
         602.564208984375,
         611.0515747070312,
         591.2024536132812,
         596.1395874023438,
         610.1753540039062,
         598.2145385742188,
         574.7982177734375,
         471.78070068359375,
         458.9857177734375
      ],
      "poa_monthly":[
         136.04103088378906,
         136.04443359375,
         185.7895965576172,
         181.16891479492188,
         185.77963256835938,
         182.52105712890625,
         187.89971923828125,
         193.35572814941406,
         187.40081787109375,
         175.5979461669922,
         137.59872436523438,
         131.25526428222656
      ],
      "solrad_monthly":[
         4.388420581817627,
         4.858729839324951,
         5.993212699890137,
         6.038963794708252,
         5.992891311645508,
         6.084035396575928,
         6.061281204223633,
         6.237281322479248,
         6.246694087982178,
         5.664449691772461,
         4.5866241455078125,
         4.2340407371521
      ],
      "dc_monthly":[
         495.09564208984375,
         487.5823669433594,
         657.702880859375,
         629.8565063476562,
         638.9706420898438,
         618.6126708984375,
         623.68994140625,
         637.5205688476562,
         624.635009765625,
         599.9056396484375,
         492.5662841796875,
         479.1076354980469
      ],
      "ac_annual":6683.64501953125,
      "solrad_annual":5.5322184562683105
   }
}
"""


class Test(unittest.TestCase):
    """
    Unit tests for PVWatts.

    """
    def test_pvwatts_results(self):
        """Test PVWattsResult attrib handling"""
        result = PVWattsResult(json.loads(SAMPLE_RESPONSE))
        self.assertEqual(result.solrad_annual, 5.5322184562683105)
        self.assertEqual(result.station_info['city'], 'BOULDER')

    def test_pypvwatts_validation(self):
        """Test pypvwatts validations"""
        self.assertRaises(PVWattsValidationError, PVWatts.request,
                          system_capacity='a', module_type=1, array_type=1,
                          azimuth=190, tilt=30,
                          dataset='tmy2', losses=0.13,
                          lat=40, lon=-105)
        self.assertRaises(PVWattsValidationError, PVWatts.request,
                          system_capacity=4, module_type='1', array_type=1,
                          azimuth=190, tilt=30,
                          dataset='tmy2', losses=0.13,
                          lat=40, lon=-105)
        self.assertRaises(PVWattsValidationError, PVWatts.request,
                          system_capacity=4, module_type=1, array_type='1',
                          azimuth=190, tilt=30,
                          dataset='tmy2', losses=0.13,
                          lat=40, lon=-105)
        self.assertRaises(PVWattsValidationError, PVWatts.request,
                          system_capacity=4, module_type=1, array_type=1,
                          azimuth=-190, tilt=30,
                          dataset='1', losses=0.13,
                          lat=40, lon=-105)
        self.assertRaises(PVWattsValidationError, PVWatts.request,
                          system_capacity=4, module_type=1, array_type=1,
                          azimuth=190, tilt=100,
                          dataset='1', losses=0.13,
                          lat=40, lon=-105)
        self.assertRaises(PVWattsValidationError, PVWatts.request,
                          system_capacity=4, module_type=1, array_type=1,
                          azimuth=190, tilt=30,
                          dataset='1', losses=0.13,
                          lat=40, lon=-105)
        self.assertRaises(PVWattsValidationError, PVWatts.request,
                          system_capacity=4, module_type=1, array_type=1,
                          azimuth=190, tilt=30,
                          dataset='tmy2', losses=-400,
                          lat=40, lon=-105)
        self.assertRaises(PVWattsValidationError, PVWatts.request,
                          system_capacity=4, module_type=1, array_type=1,
                          azimuth=190, tilt=30,
                          dataset='tmy2', losses=0.13,
                          lat=-100, lon=-105)
        self.assertRaises(PVWattsValidationError, PVWatts.request,
                          system_capacity=4, module_type=1, array_type=1,
                          azimuth=190, tilt=30,
                          dataset='tmy2', losses=0.13,
                          lat=40, lon=400)
        self.assertRaises(PVWattsValidationError, PVWatts.request,
                          system_capacity=4, module_type=1, array_type=1,
                          azimuth=190, tilt=30,
                          dataset='tmy2', losses=0.13,
                          lat=40, lon=-105, timeframe='notvalid')
        self.assertRaises(PVWattsValidationError, PVWatts.request,
                          system_capacity=4, module_type=1, array_type=1,
                          azimuth=190, tilt='a',
                          dataset='tmy2', losses=0.13,
                          lat=40, lon=-105)
        self.assertRaises(PVWattsValidationError, PVWatts.request,
                          system_capacity=4, module_type=1, array_type=1,
                          azimuth=190, tilt=30,
                          dataset='tmy2', losses=0.13,
                          lat=40, lon=-105, dc_ac_ratio=-10)
        self.assertRaises(PVWattsValidationError, PVWatts.request,
                          system_capacity=4, module_type=1, array_type=1,
                          azimuth=190, tilt=30,
                          dataset='tmy2', losses=0.13,
                          lat=40, lon=-105, gcr=10)
        self.assertRaises(PVWattsValidationError, PVWatts.request,
                          system_capacity=4, module_type=1, array_type=1,
                          azimuth=190, tilt=30,
                          dataset='tmy2', losses=0.13,
                          lat=40, lon=-105, inv_eff=0)

    def test_pypvwatts(self):
        """Test pypvwatts"""
        PVWatts.api_key = 'DEMO_KEY'
        results = PVWatts.request(
            system_capacity=4, module_type=1, array_type=1,
            azimuth=190, tilt=30, dataset='tmy2',
            losses=0.13, lat=40, lon=-105)
        self.assert_results(results)

    def test_pypvwatts_instance(self):
        """Test pypvwatts instance based searches"""
        p = PVWatts(api_key='DEMO_KEY')
        results = p.request(
            system_capacity=4, module_type=1, array_type=1,
            azimuth=190, tilt=30, dataset='tmy2',
            losses=0.13, lat=40, lon=-105)
        self.assert_results(results)

    def assert_results(self, results):
        self.assertEqual(results.ac_annual, 7263.046875)
        self.assertEqual(results.solrad_annual, 5.446694850921631)
        self.assertEqual(results.station_info['city'], 'BOULDER')
        self.assertIn(501.930908203125, results.dc_monthly)
        self.assertIn(183.11537170410156, results.poa_monthly)
        self.assertIn(6.103845596313477, results.solrad_monthly)


if __name__ == "__main__":
    unittest.main()
