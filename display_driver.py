#!/usr/bin/env python

# Copyright 2011
# This small library manages communication over the USB/Serial link to the
# arduino.
import sys
import argparse
import serial
import time

colors = ['R', 'G', 'B']
increments = [0,0,0]

def write_colors(colors, intensities, arduino):
  """Sets the specified colors to the specified colors on the device
  represented by the arduino parameter.

  Inputs:
    colors: an array of color specifier strings, each of which can take on one
            of the values 'R', 'G', or 'B'.
    intensities: an array of intensities that the LEDs specified in colors
                 should be set to.  For example, if colors is ['R','B'] and
                 intensities is [128, 255], then the red LED will be set to
                 128 and the blue LED will be set to 255.
    arduino: an instance of serial.Serial that corresponds to an arduino
             controller connected to the computer."""
  cmd = ''
  for i in range(len(colors)):
    cmd = cmd + colors[i].upper() + chr(intensities[i])
  print(cmd)
  try:
    arduino.write(cmd)
    time.sleep(.2)
  except:
    print "Failed to send!"

def main(argv=None):
  """A test that makes sure that you are able to communicate with the arduino
  and that the LEDs have been wired correctly."""
  if argv is None:
    argv = sys.argv[1:]

  parser = argparse.ArgumentParser(description=(
      "Communicate with an arduino board to give commands."))
  options = parser.parse_args(argv)
  
  try:  
    arduino = serial.Serial('/dev/ttyUSB0', 9600)  
  except:  
    print "Failed to connect on /dev/ttyUSB0"

  print(arduino.readline())
  intensities = [0,0,0]
  try:
    while True:
      for i in range(len(colors)):
        intensities[i] = (intensities[i] + increments[i]) % 256
      write_colors(colors, intensities, arduino)
        
  except(EOFError):  
    print("All done then!")

  arduino.close()


if __name__ == '__main__':
  sys.exit(main())
