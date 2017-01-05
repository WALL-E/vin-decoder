#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
"""
Vin Class
"""

class Vin(object):
    """
    Vin Class
    """
    def __init__(self, vincode):
        self.vincode = vincode.upper()

    def is_valid(self):
        """
        checkout length and checksum
        """
        if len(self.vincode) != 17:
            return False
        if "I" in self.vincode or "O" in self.vincode or "Q" in self.vincode:
            return False
        return True

    def print_vin(self):
        """
        print vin
        """
        print "VIN: %s" % self.vincode

    def get_vin(self):
        """
        get vin
        """
        return self.vincode

    def get_year(self):
        """
        get year
        """
        return self.vincode[9]

    def get_wmi(self):
        """
        get wmi
        """
        return self.vincode[0:3]

    def get_vds(self):
        """
        get vds
        """
        return self.vincode[3:8]

    def get_checksum(self):
        """
        get chcksum
        """
        return self.vincode[8]


def main():
    """
    main function
    """
    vin = Vin("LVSHCAMB1CE054249")
    vin.print_vin()
    print "year:", vin.get_year()
    print "wmi:", vin.get_wmi()
    print "vds:", vin.get_vds()
    print "checksum:", vin.get_checksum()
    print "valid vin:", vin.is_valid()
    vin = Vin("LVSHCAMB1CE0542490")
    print "valid vin:", vin.is_valid()
    vin = Vin("lvshcamb1ce0542490")
    print "vin:", vin.get_vin()


if __name__ == '__main__':
    main()
