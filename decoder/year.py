#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-

class YearDecoder:
    data = {
        "N":"1992",
        "P":"1993",
        "R":"1994",
        "S":"1995",
        "T":"1996",
        "V":"1997",
        "W":"1998",
        "X":"1999",
        "Y":"2000",
        "1":"2001",
        "2":"2002",
        "3":"2003",
        "4":"2004",
        "5":"2005",
        "6":"2006",
        "7":"2007",
        "8":"2008",
        "9":"2009",
        "A":"2010",
        "B":"2011",
        "C":"2012",
        "D":"2013",
        "E":"2014",
        "F":"2015",
        "G":"2016",
        "H":"2017",
        "J":"2018",
        "K":"2019",
        "L":"2020",
        "M":"2021",
    }

    @classmethod
    def decode(cls, code):
        if cls.data.has_key(code):
            return cls.data[code]
        return None


if __name__ == '__main__':
    print YearDecoder.decode("C") == "2012"
    print YearDecoder.decode("5") == "2005"
