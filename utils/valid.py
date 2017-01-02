#!/usr/bin/env python
"""
vin: checksum
"""


def valid(vincode):
    """
    checkout length, word and checksum
    """
    maps = "0123456789X"
    weights = [
        8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2
    ]
    table = {
        "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
        "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8,
        "J": 1, "K": 2, "L": 3, "M": 4, "N": 5, "P": 7, "R": 9,
        "S": 2, "T": 3, "U": 4, "V": 5, "W": 6, "X": 7, "Y": 8, "Z": 9,
    }

    if not isinstance(vincode, str) and not isinstance(vincode, unicode):
        return False

    if len(vincode) != 17:
        return False

    vincode = vincode.upper()
    if "I" in vincode or "O" in vincode or "Q" in vincode:
        return False

    total = 0
    for index, value in enumerate(vincode):
        try:
            products = table[value] * weights[index]
        except KeyError:
            break
        total = total + products

    index = total%11

    return maps[index] == vincode[8]


def main():
    """
    main function
    """
    import sys

    if len(sys.argv) > 1:
        for vincode in sys.argv[1:]:
            print "%s: %s" %(vincode, valid(vincode))
    else:
        assert valid(u"LHGRC3838F8043791")
        assert valid("LhGRC3838F8043791")

        assert valid("WP0AA2987FK162906")
        assert valid("wP0AA2987FK162906")

        assert not valid("AHGRC3838F8043791")
        assert not valid("AP0AA2987FK162906")

        assert not valid("LHGRC3838F804379I")
        assert not valid("LHGRC3838F804379O")
        assert not valid("LHGRC3838F804379Q")


        assert not valid("WP0AA2987FK16290")
        assert not valid("WP0AA2987FK1629066")

        assert not valid([])
        assert not valid({})

        print "Unit test [ok]"

if __name__ == "__main__":
    main()
