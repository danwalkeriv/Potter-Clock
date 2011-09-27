Potter Clock
============

The Potter Clock is a simple
[ambient information display](http://en.wikipedia.org/wiki/Ambient_device)
that provides a few bits of information about your location.  If you are
at home the display shows a blue light.  If you are at school/work the light is
red.  If you are out-and-about then the light is green, and the intensity of
the light increases as you near home.

The name "Potter Clock" was inspired by a magical artifact found in J.K Rowlings
Harryp Potter novels that functions in a similar manner:
>Mrs. Weasley glanced at the grandfather clock in the corner. Harry liked this clock. It was completely useless if you wanted to know the time, but otherwise very informative. It had nine golden hands, and each of them was engraved with one of the Weasley family’s names. There were no numerals around the face, but descriptions of where each family member might be. “Home,” “school,” and “work” were there, but there was also “traveling,” “lost,” “hospital,” “prison,” and, in the position where the number twelve would be on a normal clock, “mortal peril.” 


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
Set the home and work locations appropriately.  You can find the latitude and
longitude coordinates of a location by using Google Maps by right-clicking on
the right location on the map and then clicking on the "What's here?" item on
the context menu when it appears.  The latitude and longitude will be in the
search bar at the top of the results screen.

The `client_id`, and `client_secret` settings are strings supplied by
the [Google APIs Console](https://code.google.com/apis/console/b/0/?pli=1#project:966405524).
Go to that site and start a new API project.  Make sure to set the type of the
project to a native application by using `urn:ietf:wg:oauth:2.0:oob` and
`http://localhost` for your redirect URLS.

Once you have `config.py` setup correctly generate the OAuth token by running
`python authenticate.py`.  The program will display a URL that you should copy
and paste into your browser.  You will then follow a few simple instructions to
complete the OAuth authentication flow to retrieve a token that the application
will use to authenticate in order to request your location.  After that, you
should have a file named latitude.dat in the Potter Clock directory.

Finally, run `python potter_clock.py` to start the "clock".  For best results,
run this command in screen so that it will continue to run should you log out.

Copyright 2011, Daniel Walker
