#!/usr/bin/python3
# *-* coding: utf-8 *-*
# Python 3

import argparse
import logging
import os
import sys
import datetime
import csv
import random

def main(args):
    p = argparse.ArgumentParser(description="Credit Cards generator")
    p.add_argument("--iin", default="./res/inn.txt", help="file containing inn info")
    p.add_argument("-i", "--issuer", default="random", help="issuer name, if none, random one")
    p.add_argument("-n", "--number", default="1", help="number of cards to generate")
    p.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    a = p.parse_args(args)

    logging.basicConfig(level=logging.ERROR, format='%(asctime)s::%(levelname)s - [%(filename)s - %(funcName)s():%(lineno)s ] %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
    l = logging.getLogger()

    if a.verbose:
        l.setLevel(logging.DEBUG)
        l.debug("Verbose enabled")

    if os.path.isfile(os.path.abspath(a.iin)):
        vendors = []
        with open(os.path.abspath(a.iin)) as r:
            csvfile = csv.DictReader(r)
            for l in csvfile:
                vendors.append(l["Issuer"])
        issuers = list(set(vendors))
    else:
        l.critical("IIN file not found! Current path is: %s.\nPlease check again before restarting." %(str(os.path.abspath(a.iin))))
        exit(10)
    if a.issuer == "random":
        issuer = random.choice(issuers)
    if a.issuer not in issuers:
        print("Your issuer (%s) is not in the known list yet. If you'd like to choose another one, pick from the following list:" %(a.issuer))
        for t in issuers:
            print("    - %s" %(t))
        issuer = ""
        while issuer not in issuers:
            issuer = input("Issuer: ")
    else:
        issuer = a.issuer

    # getting options
    options = []
    with open(os.path.abspath(a.iin)) as r:
        csvfile = csv.DictReader(r)
        for l in csvfile:
            if l["Issuer"] == issuer:
                options.append([l["StartsWith"], l["Length"]])

    # generation
    cards = []
    for x in range(int (a.number)):
        combi = random.choice(options)
        cards.append(createCard(combi[0], combi[1]))

    #export cards
    exportCards(cards, "stdout")

def exportCards(cards, method):
    if method == "stdout":
        for x in cards:
            print(x)

def createCard(beg, totalL):
    l = int(totalL) - len(beg)
    cardnumber = beg
    for i in range(l-1):
        cardnumber = cardnumber + str(random.choice(range(0, 10)))
    rev = []
    rev.extend(cardnumber)
    rev.reverse()
    s = 0
    p = 0
    while p < int(totalL) - 1:
        odd = int(rev[p]) * 2
        if odd > 9:
            odd = odd - 9
        s = s + odd
        if p < int(totalL) - 2:
            p = p + 1
            s = s + int(rev[p])
        p = p + 1
    if s%10 > 0:
        c = 10-(s%10)
    else:
        c = 0
    cardnumber = cardnumber + str(c)
    return(cardnumber)

if __name__ == '__main__':
    if sys.version_info < (3, 0):
        pyBirth = datetime.datetime.strptime('20 Feb 1991', '%d %b %Y')
        py3Birth = datetime.datetime.strptime('3 Dec 2008', '%d %b %Y')
        print("Come on man, it's %s! Use Python3 already!\nIf you didn't know, Python is now %s old.\nBut Python3 is only %s old! So use to knew one ;)"  %(str(datetime.datetime.now().year), str(datetime.datetime.now() - pyBirth), str(datetime.datetime.now() - py3Birth)))
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
