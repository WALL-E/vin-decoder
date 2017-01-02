#!/usr/bin/env python


def checkSum(vincode):
    """
    checkout length and checksum
    """
    if len(vincode) != 17:
        return False
    if "I" in vincode or "O" in vincode or "Q" in vincode:
        return False

    table = {
        "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
        "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8,
        "J": 1, "K": 2, "L": 3, "M": 4, "N": 5, "P": 7, "R": 9,
        "S": 2, "T": 3, "U": 4, "V": 5, "W": 6, "X": 7, "Y": 8, "Z": 9,
    }

    weight = [
        8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2
    ]

    sum = 0
    for i,v in enumerate(vincode):
        try:
            tmp = table[v] * weight[i]
        except KeyError:
            break
        sum = sum + tmp

    remainder = sum%11
    if remainder == 10:
        remainder = "X"

    return str(remainder) == vincode[8]
        

def main():
    assert checkSum("LHGRC3838F8043791")
    assert checkSum("WP0AA2987FK162906")

    assert not checkSum("AHGRC3838F8043791")
    assert not checkSum("AP0AA2987FK162906")

    assert not checkSum("aP0AA2987FK162906")

    print "Unit test [ok]"

if __name__ == "__main__":
    main()
