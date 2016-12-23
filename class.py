#!/usr/bin/python

# -*- coding: UTF-8 -*-

class Vin:
   def __init__(self, name):
      self.name = name
   
   def printVin(self):
     print "VIN: %s" % self.name


if __name__ == '__main__':
    vin = Vin("LVSHCAMB1CE054249")
    vin.printVin()

