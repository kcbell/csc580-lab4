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

def getPuzzlePart(html):
    match = re.match(PATTERN, html, re.DOTALL)
    return match.group(1).strip().replace("`", "'")

def getPuzzle(html):
    strPuzzle = ""
    title = "<title>Knights and Knaves</title>"
    bigTag = "<p>"
    endTag = "</p>"
    entTag = "<entry>"
    numParas = 0
    idx = html.find(title)
    if idx > -1:
        html = html[idx+len(title):]
    while numParas < 3 and len(html) > 0:
        idx1 = html.find(bigTag)
        if idx1 < 0:
            break
        if numParas == 1:
            idx1 = html.find(entTag) + len(entTag)
        else:
            idx1 = idx1 + len(bigTag)
        idx2 = html.find(endTag)
        if idx2 < 0:
            break
        strPuzzle += html[idx1:idx2]
        html = html[idx2 + len(endTag):]
        numParas += 1
    return strPuzzle.strip().replace("`", "'")

def getPuzzleParts(nums):
    r = []
    for i in nums:
        r.append(getPuzzlePart(urllib.urlopen(URL, PARAM % i).read()))
    return r

def getPuzzles(nums):
    r = []
    for i in nums:
        r.append(getPuzzle(urllib.urlopen(URL, PARAM % i).read()))
    return r

def main():
    for puz in getPuzzleParts(xrange(1, NUM_PUZZLES)):
        print puz

if __name__ == '__main__':
    main()