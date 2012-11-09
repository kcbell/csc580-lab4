'''
Pulls the knights and knaves puzzles from http://philosophy.hku.hk/think/logic/knight.php

Created on Nov 9, 2012

@author: Karl
'''
import re, nltk, urllib

URL = "http://philosophy.hku.hk/think/logic/knight.php"
PARAM = "qno=%d"
NUM_PUZZLES = 382
PATTERN = ".*<entry>([^<]*)</p>.*"

def getPuzzle(html):
    match = re.match(PATTERN, html, re.DOTALL)
    return match.group(1).strip().replace("`", "'")

def main():
    for i in xrange(1, NUM_PUZZLES):
        puz = getPuzzle(urllib.urlopen(URL, PARAM % i).read())
        print puz

if __name__ == '__main__':
    main()