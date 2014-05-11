#!/usr/bin/env python2.7 -tt
"""fun with weather.gov"""

import sys
import re
import urllib

class Weather:
    """weather.gov html scrubber"""

    _locationpat = re.compile(r'<p class="current-conditions-location">([\w() ]+)</p>') 
    _temppattern = re.compile(r'<p class="myforecast-current-lrg">(\d+&deg;F)</p>' \
       r'<p><span class="myforecast-current-sm">(\d+&deg;C)</span></p>')
    _forecastpat = re.compile(r'<div class="one-ninth-first">[\t\n\r ]+' \
       r'<p class="txt-ctr-caps">(\w+)[<br>]+(\w+)?</p>[\t\n\r ]+' \
       r'<p><img src="[\w/.]+" width="\d+" height="\d+" alt="[\w ]+" ' \
       r'title="([\w ]+)" /></p>[\t\n\r ]+' \
       r'<p>[\w</>]+</p>[\t\n\r ]+' \
       r'<p class="point-forecast-icons-\w+">(\w+: \d+) &deg;F</p>[\t\n\r ]+</div>', re.I)

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
        temp = self.__class__._temppattern.findall(contents)
        fore = self.__class__._forecastpat.findall(contents)
        loc  = self.__class__._locationpat.findall(contents)[0]
    
        self.temps = [re.sub(r"&deg;", r"\u00b0", tstr).decode("unicode-escape") for tstr in temp[0]]
        self.forecast = fore
        self.loc = loc

    def __unicode__(self):
        forecast_str = u"{self.zipcode}: {self.loc}\n".format(self=self)
        forecast_str += u"Current Temperature: {}, {}\n".format(self.temps[0], self.temps[1])
        for forecast in self.forecast:
            forelist = list(forecast)
            if "" in forelist:
                forelist.remove("")
            else:
                forelist[0] = " ".join(forelist[0:2])
                forelist.remove(forelist[1])
            forelist[0] = forelist[0].ljust(15)
            forecast_str += " ".join(forelist) + "\n"
        return forecast_str

    def __str__(self):
        return unicode(self).encode("utf-8")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        zipcode = int(sys.argv[1])
    else:
        zipcode = 94110

    print(Weather(zipcode))
