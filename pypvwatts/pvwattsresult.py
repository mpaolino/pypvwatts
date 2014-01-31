# coding: utf-8

class PVWattsResult(object):
    """
    Result class for PVWatts request
    """
    # Result's output fields to be accesed as properties of PVWattsResult
    shortcut_fields = ('poa_monthly', 'dc_monthly', 'ac_annual',
                       'solrad_annual', 'solrad_monthly', 'ac_monthly',
                       'ac', 'poa', 'dn', 'dc', 'df', 'tamb', 'tcell', 'wspd')

    def __init__(self, result):
        """
        Creates instance of PVWattsResult from the JSON API response
        """
        self.result = result

    @property
    def raw(self):
        return self.result

    def __getattr__(self, name):
        """
        Access outputs results as properties
        """
        result = None
        if name in PVWattsResult.shortcut_fields and 'outputs' in self.result:
            return self.result['outputs'][name]
        if name is not None:
            return self.result[name]
        return result

    def __unicode__(self):
        return unicode(self.result)

    def __str__(self):
        return self.__unicode__().encode('utf8')
