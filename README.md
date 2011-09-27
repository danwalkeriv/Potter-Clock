Potter Clock
============

The Potter Clock is a simple
[ambient information display](http://en.wikipedia.org/wiki/Ambient_device)
that provides a few bits of information about your location.  If you are
at home the display shows a blue light.  If you are at school/work the light is
red.  If you are out-and-about then the light is green, and the intensity of
the light increases as you near home.  The name "Potter Clock" refers to the
magical clocks in the Harry Potter novels that serve a similar function.

Overview
--------

The Potter Clock uses the [Google Latitude](https://www.google.com/latitude/b/0)
web service and API in order to keep track of your location.  The user updates
the service with his/her location in whatever way they prefer (most likely with
a GPS equipped mobile device).  The display consists of an Arduino embedded
device that controls the intensity of red, green, and blue LEDs based on
commands given by a python script that periodically polls Latitude for the
user's current location.

Use
---

To build your own Potter Clock, connect a red LED to analog output pin 9,
a green LED to pin 10 and a blue LED to pin 11.  Make sure to check the
data sheets for your LEDs and use appropriately rated resistors for each.
Use the Arduino IDE to upload the `display_firmware.pde` sketch to your
Arduino.

Next, copy `config.py.example` to `config.py` and edit the values there.
You need to tell the program which locations should trigger the home (blue),
and the work (red) LEDs.  The brightness of the green LED also depends on
where you are in relation to the home point.  You can the latitude and
longitude pairs using Google Maps by right-clicking on the right location
on the map and then clicking on the "What's here?" item on the context
menu when it appears.  The latitude and longitude will be in the search
bar at the top of the results screen.

The `client_id`, an `client_secret` settings are strings supplied by
the [Google APIs Console](https://code.google.com/apis/console/b/0/?pli=1#project:966405524).
Go there and start a new API project.  Make sure to set the type of the
project to a native application by using `urn:ietf:wg:oauth:2.0:oob`
and `http://localhost` for your redirect URLS.

Once you have `config.py` setup correctly generate the OAuth token by
running `python authenticate.py`.  The program will display a URL that you
should copy and paste into your browser.  You will then follow a few simple
instructions to complete the OAuth authentication flow to retrieve a token that
the application will use to authenticate in order to request your location.
After that, you should have a file named latitude.dat in the Potter Clock
directory.

Finally, run `python potter_clock.py` to start the "clock".  For best results,
run this command in screen so that it will continue to run should you log out.

Copyright 2011, Daniel Walker
