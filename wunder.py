#!/usr/bin/env python
'''
Wunderground API command line script.
'''

import sys
import requests

# todo: raise error if no config file
from config import WUAPI


class Wunder(object):
    ''' Wunderground API class. '''

    lookup_zip = 'http://api.wunderground.com/api/{}/geolookup/q/{}.json'
    us_city_current_conditions = ('http://api.wunderground.com/api/{}/'
                                  'conditions/q/{}/{}.json')

    @classmethod
    def check_call(cls, response):
        ''' Check that the call status is 200. '''

        # todo: raise error if missing certain dict keys
        if response.status_code != 200:
            print response.text
            raise Exception('Return status code is not 200.')

    @classmethod
    def conditions(cls, us_state, us_city):
        ''' Lookup weather given location. '''

        us_city = us_city.replace(' ', '_')

        call = cls.us_city_current_conditions.format(WUAPI, us_state, us_city)
        response = requests.get(call)
        cls.check_call(response)

        info = response.json()
        current_obs = info['current_observation']

        fields = ['station_id', 'observation_time',
                  'temp_f', 'relative_humidity']

        # todo: spruce-up output
        for field in fields:
            print current_obs[field]

    # todo: expand command line api to lookup and list locations
    @classmethod
    def lookup_zipcode(cls, zipcode):
        ''' Lookup location and then lookup weather with first find. '''

        call = cls.lookup_zip.format(WUAPI, zipcode)
        response = requests.get(call)
        cls.check_call(response)

        info = response.json()
        print info


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print 'usage: wunder.py [state] [city]'
    else:
        STATE, CITY = (sys.argv[1], sys.argv[2])
        Wunder.conditions(STATE, CITY)
