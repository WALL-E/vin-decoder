#!/usr/bin/python

# -*- coding: UTF-8 -*-

class Vin:
    def __init__(self, name):
        self.name = name
   
    @classmethod
    def checkVin(cls, name):
        if len(name) != 17:
            return False
        return True

    def printVin(self):
        print "VIN: %s" % self.name

    def getYear(self):
        return self.name[9]
     
    def getWmi(self):
        return self.name[0:3]

    def getVds(self):
        return self.name[3:8]

    def getChecksum(self):
        return self.name[8]


if __name__ == '__main__':
    vin = Vin("LVSHCAMB1CE054249")
    vin.printVin()
    print "year:", vin.getYear()
    print "wmi:", vin.getWmi()
    print "vds:", vin.getVds()
    print "checksum:", vin.getChecksum()
    print "valid vin:", Vin.checkVin("LVSHCAMB1CE054249")
    print "valid vin:", Vin.checkVin("LVSHCAMB1CE0542490")

