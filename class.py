#!/usr/bin/python

# -*- coding: UTF-8 -*-

class Vin:
    def __init__(self, vincode):
        self.vincode = vincode
   
    @staticmethod
    def checkVin(vincode):
        if len(vincode) != 17:
            return False
        return True

    def printVin(self):
        print "VIN: %s" % self.vincode

    def getYear(self):
        return self.vincode[9]
     
    def getWmi(self):
        return self.vincode[0:3]

    def getVds(self):
        return self.vincode[3:8]

    def getChecksum(self):
        return self.vincode[8]


if __name__ == '__main__':
    vin = Vin("LVSHCAMB1CE054249")
    vin.printVin()
    print "year:", vin.getYear()
    print "wmi:", vin.getWmi()
    print "vds:", vin.getVds()
    print "checksum:", vin.getChecksum()
    print "valid vin:", Vin.checkVin("LVSHCAMB1CE054249")
    print "valid vin:", Vin.checkVin("LVSHCAMB1CE0542490")

