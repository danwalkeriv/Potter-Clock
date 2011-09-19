from math import radians, sin, cos, asin, sqrt, pi
import numpy as np

import serial
import sys
import argparse
import time
import httplib2
import json
from lxml import etree

from apiclient.discovery import build
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
from oauth2client.file import Storage

import display_driver
import config

# Determines when a location is considered "at" another
at_epsilon = 0.07

# Another constant, used in calculating the distance in miles between two points
earth_radius_miles = 3956.0


def get_distance(p1, p2):
    """Calculate miles between two points specified in (lat,lon)"""
    dlat = np.radians(p1[0]) - np.radians(p2[0])
    dlon = np.radians(p1[1]) - np.radians(p2[1])
    a = np.square(np.sin(dlat/2.0)) + (cos(radians(p2[0])) * 
            np.cos(np.radians(p1[0])) * np.square(np.sin(dlon/2.0)))
    great_circle_distance = 2 * np.arcsin(np.minimum(np.sqrt(a), 1))
    d = earth_radius_miles * great_circle_distance
    return d


def location_generator():
    """The default location generator that uses the Google Latitude API to
    query the user's current location."""
    storage = Storage('latitude.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid == True:
        auth_discovery = build("latitude", "v1").auth_discovery()
        flow = OAuth2WebServerFlow(
                    client_id=config.client_id,
                    client_secret=config.client_secret,
                    scope='https://www.googleapis.com/auth/latitude.current.best',
                    user_agent=client.user_agent,
                    location='current',
                    granularity='best')

        credentials = run(flow, storage)
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build("latitude", "v1", http=http)
    body = {}
    while True:
	try:
        	location = service.currentLocation().get(granularity='best').execute()
        	# print(location)
        	current_location = (location['latitude'], location['longitude'])
        	yield current_location
        except:
		pass
	time.sleep(30)


def kml_loc_gen(kml_filename):
  """Generate a stream of place names from a kml file like one that can be
  downloaded from the Latitude location history application."""
  ns = {'kml': 'http://www.opengis.net/kml/2.2'}
  ptree = etree.parse(kml_filename)
  placemarks = ptree.xpath('//kml:Placemark', namespaces=ns)
  placemarks.reverse()
  for placemark in placemarks:
    name = placemark.xpath('./kml:name', namespaces=ns)[0].text
    lon,lat,throwaway = placemark.xpath('./kml:Point/kml:coordinates', namespaces=ns)[0].text.split(',')
    print('\nPoint from {0}'.format(name))
    yield (float(lat),float(lon))
    time.sleep(1)


def dist_to_intensity(distance, max_dist=3.0, eps=0.06):
    """Maps a distance from home to a value on the interval (0,1.0), such that
    distances close to home have a high intensity (values close to 1.0, and
    distances 'far' from home, as defined by max_dist have a low intensity.)"""
    adjusted_distance = distance - eps
    return min(1.0, (1.0 / np.exp(adjusted_distance)))


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(description=('Keeps tabs on latitude user.'))
    parser.add_argument('--test_kml_file', help=('Instead of latitude, get '
                        'points from a KML file (generated by latitude history '
                        'application)'))
    options = parser.parse_args(argv)

    try:
        arduino = serial.Serial('/dev/ttyUSB0', 9600)
    except:
        print "Failed to connect on /dev/ttyUSB0"
	sys.exit(1)
    if options.test_kml_file:
        loc_gen = kml_loc_gen(options.test_kml_file)
    else:
        loc_gen = location_generator()
    for current_location in loc_gen:
        at_home = False
        at_work = False
        green_val = 0

        if get_distance(current_location, config.home_point) < at_epsilon:
            print("At home")
            at_home = True
	    display_driver.write_colors(['R', 'G', 'B'], [0,0,255], arduino)
        elif get_distance(current_location, config.work_point) < at_epsilon:
            print("At work")
            at_work = True
	    display_driver.write_colors(['R', 'G', 'B'], [255,0,0], arduino)
        else:
            distance_to_home = get_distance(current_location, config.home_point)
            if distance_to_home <= 1.5:
                green_val = dist_to_intensity(distance_to_home)
            elif distance_to_home < 100:
                green_val = dist_to_intensity(distance_to_home)
	    print("Green value: {0}".format(int(255 * green_val)))
	    display_driver.write_colors(['R','G','B'], [0,int(255 * green_val),0],arduino)
        print("Current location: {0}".format(current_location))
        print("{0} miles from home.".format(get_distance(config.home_point, current_location)))
        

if __name__ == "__main__":
    main()
