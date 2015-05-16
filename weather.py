#!/usr/bin/env python2.7 -tt
""" regex fun with weather.gov """

import sys
import re
import urllib


class Weather:
    """ weather.gov html scrubber """

    _location = re.compile(r'<b>Current conditions at</b>[\t\n\r ]+' \
       r'<h2 class="panel-title">[\t\n\r ]+([\w() ]+)[\t\n\r ]+</h2>') 
    _current = re.compile(r'<p class="myforecast-current-lrg">(\d+&deg;F)</p>' \
       r'[\t\n\r ]+<p class="myforecast-current-sm">(\d+&deg;C)</p>')

    _day = re.compile(r'<li class="forecast-tombstone"><div>' \
       r'<p class="txt-ctr-caps">(\w+)[<br>]+(\w+)?</p>', re.I)
    _condition = re.compile( r'<p><img src="[\w/.]+" alt="[\w ]+" title="([\w ]+)"' \
       r' class="forecast-icon"></p>', re.I)
    _temp = re.compile(r'<p>[\w</>]+<br></p>' \
       r'<p class="point-forecast-icons-[\w]+">(\w+: \d+) &deg;F</p></div></li>', re.I)

    def __init__(self, zipcode = 94110):
        self.zipcode = zipcode
        url = "http://forecast.weather.gov/zipcity.php?inputstring=" + str(self.zipcode)
        try:
            webpage = urllib.urlopen(url)
        except IOError: 
            sys.stderr.write("Couldn't connect to {}\n".format(url))
            return 
        except ValueError as ValueMsg:
            sys.stderr.write("Value Error: {}\n".format(ValueMsg))
            return
        contents = str(webpage.read())
        webpage.close()

        location = self.__class__._location.findall(contents)
        current = self.__class__._current.findall(contents)
        days = self.__class__._day.findall(contents)
        conditions = self.__class__._condition.findall(contents)
        temps = self.__class__._temp.findall(contents)

        if len(location) == 0:
            raise Exception('regex fail: location')
        else:
            location = location[0]

        if len(current) == 0:
            raise Exception('regex fail: current temp')
        else: 
            current = [re.sub(r"&deg;", r"\u00b0", temp).decode("unicode-escape")
                       for temp in current[0]]

        if len(days) == 0:
            raise Exception('regex fail: 7-day title')
        else:
            days = [' '.join(day).strip() for day in days]

        if len(conditions) == 0:
            raise Exception('regex fail: 7-day conditions')

        if len(temps) == 0:
            raise Exception('regex fail: 7-day temperatures')

        if len(days) != len(conditions) != len(temps):
            raise Exception('regex issue: days != conditions != temps')

        self.location = location
        self.F, self.C = current
        self.forecast = zip(days, temps, conditions)

    def __unicode__(self):
        forecast_str = u"\n{self.zipcode}: {self.location}\n".format(self=self)
        forecast_str += u"Current Temperature: {self.F}, {self.C}\n".format(self=self)
        for forecast in self.forecast:
            forecast_str += "{:>15}  {:>8}  {:<15}\n".format(*forecast)
        return forecast_str

    def __str__(self):
        return unicode(self).encode("utf-8")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        zipcode = int(sys.argv[1])
    else:
        zipcode = 94110

    print(Weather(zipcode))
