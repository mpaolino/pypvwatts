# coding: utf-8
"""
Unit tests for pypvwatts.

"""
from pypvwatts import PVWatts, PVWattsResult
from pvwattserror import PVWattsValidationError

import unittest
import json

SAMPLE_RESPONSE = """
{
  "station_info": {
    "tz": -7,
    "location": "94018",
    "lon": -105.25,
    "file_name": "94018.tm2",
    "city": "BOULDER",
    "state": "CO",
    "lat": 40.01666641235352,
    "elev": 1634
  },
  "errors": [

  ],
  "version": "4.0.0",
  "inputs": {
    "system_size": "4",
    "lon": "-105",
    "derate": "0.77",
    "dataset": "tmy2",
    "lat": "40",
    "api_key": "DEMO_KEY"
  },
  "warnings": [

  ],
  "outputs": {
    "poa_monthly": [
      137.1923980712891,
      137.0316772460938,
      187.4732360839844,
      182.7943878173828,
      185.7599792480469,
      182.4970855712891,
      187.8779907226562,
      193.34228515625,
      187.3993988037109,
      175.8596649169922,
      137.8765869140625,
      132.9652557373047
    ],
    "dc_monthly": [
      468.0147399902344,
      457.9238891601562,
      616.0709228515625,
      581.62548828125,
      576.5953979492188,
      551.68603515625,
      553.3501586914062,
      569.5568237304688,
      564.85595703125,
      550.3904418945312,
      460.4128112792969,
      454.1395263671875
    ],
    "ac_annual": 5834.35107421875,
    "solrad_annual": 5.553147792816162,
    "ac_monthly": [
      426.7577514648438,
      417.6890869140625,
      563.779541015625,
      529.3705444335938,
      523.4755249023438,
      500.5887451171875,
      502.0051879882812,
      518.2822875976562,
      515.994140625,
      503.0267639160156,
      420.1042785644531,
      413.2771606445312
    ],
    "solrad_monthly": [
      4.425561428070068,
      4.893988609313965,
      6.047523975372314,
      6.093146324157715,
      5.992257595062256,
      6.083236217498779,
      6.060580253601074,
      6.236847877502441,
      6.246646404266357,
      5.672892570495605,
      4.59588623046875,
      4.289201736450195
    ]
  },
  "ssc_info": {
    "version": 27,
    "build": "Unix 64 bit GNU/C++ Jan 10 2013 20:00:07"
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
        self.assertEqual(result.solrad_annual, 5.553147792816162)
        self.assertEqual(result.station_info['city'], 'BOULDER')

    def test_pypvwatts_validation(self):
        """Test pypvwatts validations"""
        self.assertRaises(PVWattsValidationError, PVWatts.request,
                          system_size='a', dataset='tmy2', derate=0.77,
                          lat=40, lon=-105, azimuth=0)
        self.assertRaises(PVWattsValidationError, PVWatts.request,
                          system_size=4, dataset=1, derate=0.77,
                          lat=40, lon=-105, azimuth=0)
        self.assertRaises(PVWattsValidationError, PVWatts.request,
                          system_size=4, dataset='tmy2', derate=-400,
                          lat=40, lon=-105, azimuth=0)
        self.assertRaises(PVWattsValidationError, PVWatts.request,
                          system_size=4, dataset='tmy2', derate=0.77,
                          lat=-100, lon=-105, azimuth=0)
        self.assertRaises(PVWattsValidationError, PVWatts.request,
                          system_size=4, dataset='tmy2', derate=0.77,
                          lat=-10, lon=400, azimuth=0)
        self.assertRaises(PVWattsValidationError, PVWatts.request,
                          system_size=4, dataset='tmy2', derate=0.77,
                          lat=-10, lon=-100, azimuth=-10)
        self.assertRaises(PVWattsValidationError, PVWatts.request,
                          system_size=4, dataset='tmy2', derate=0.77,
                          lat=-10, lon=-100, azimuth=0, timeframe='notvalid')
        self.assertRaises(PVWattsValidationError, PVWatts.request,
                          system_size=4, dataset='tmy2', derate=0.77,
                          lat=-10, lon=-100, azimuth=0, tilt='a')
        self.assertRaises(PVWattsValidationError, PVWatts.request,
                          system_size=4, dataset='tmy2', derate=0.77,
                          lat=-10, lon=-100, azimuth=0, track_mode=6)
        self.assertRaises(PVWattsValidationError, PVWatts.request,
                          system_size=4, dataset='tmy2', derate=0.77,
                          lat=-10, lon=-100, azimuth=0, inoct=10)
        self.assertRaises(PVWattsValidationError, PVWatts.request,
                          system_size=4, dataset='tmy2', derate=0.77,
                          lat=-10, lon=-100, azimuth=0, gamma=-3)

    def test_pypvwatts(self):
        """Test pypvwatts"""
        PVWatts.api_key = 'DEMO_KEY'
        results = PVWatts.request(system_size=4, dataset='tmy2', derate=0.77,
                            lat=40, lon=-105)
        self.assert_results(results)

    def test_pypvwatts_instance(self):
        """Test pypvwatts instance based searches"""
        p = PVWatts(api_key='DEMO_KEY')
        results = p.request(system_size=4, dataset='tmy2', derate=0.77, lat=40,
                           lon=-105)
        self.assert_results(results)

    def assert_results(self, results):
        self.assertEqual(results.ac_annual, 7607.97607421875)
        self.assertEqual(results.solrad_annual, 7.110589504241943)
        self.assertEqual(results.station_info['city'], 'BOULDER')
        self.assertIn(784.6525268554688, results.dc_monthly)
        self.assertIn(252.2440948486328, results.poa_monthly)
        self.assertIn(8.341022491455078, results.solrad_monthly)


if __name__ == "__main__":
    unittest.main()
