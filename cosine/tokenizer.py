#!/usr/bin/env python

# David Purser - dpurser
# EECS 498 - Information Retrieval

# Import regular expressions library
import re

# Import Porter stemmer
import porter
stemmer = porter.PorterStemmer()

# Token matching is done with a regular expression
# An explanation of the regular expression used follows:
#  1. General word match:  [A-Za-z\-]+  This matches words (which may contain hyphens).
#   1a.  It can also match abbreviations if the word has single alphabetic characters
#        separated by periods: ((\.[A-Za-z]+\.)?  It will not, however, match 't.e.s.t'
#        (without a final period) as that is not a valid abbreviation.
#  2. Number/date match:  [0-9]+([,./-]?[0-9]+)+  This matches sequences of digits, followed by
#      any separator characters (like commas, decimals, slashes, dashes) with more digits after.
#  3. Apostrophe/contraction match:  '(re|ve|s|t|d|ll|m)  This matches the endings of
#      contractions.

#tokenregexpattern = r"(([A-Za-z\-]+((\.[A-Za-z])+\.)?)|([0-9]+([,./-]?[0-9]+)+)|('[A-Za-z]+))" # version 1
#tokenregexpattern = r"(([A-Za-z\-]+((\.[A-Za-z])+\.)?)|([0-9]+([,./-]?[0-9]+)+)|('[A-Za-z]+[^A-Za-z'.,/\-\s]))" # version 2
tokenregexpattern = r"(([A-Za-z\-]+((\.[A-Za-z])+\.)?)|([0-9]+([,./-]?[0-9]+)+)|('(re|ve|s|t|d|ll|m)))" # version 3

tokenregex = re.compile(tokenregexpattern)

def isStopToken(token):
    return (token in ('a', 'all', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'been', 'but', 'by', 'few', 'for', 'from', 'has', 'have', 'he', 'her', 'here', 'him', 'his', 'how', 'i', 'in', 'is', 'it', 'its', 'many', 'me', 'my', 'none', 'of', 'on', 'or', 'our', 'she', 'that', 'the', 'their', 'them', 'there', 'they', 'that', 'this', 'to', 'was', 'were', 'what', 'when', 'where', 'which', 'who', 'why', 'will', 'with', 'you', 'your'))

def get_stem(word):
    return stemmer.stem(word, 0, len(word)-1)

def tokenize(instr, eliminateStopwords = True, usePorter = True):
    if usePorter:
        stemmedwords = [get_stem(x[0]) for x in tokenregex.findall(instr.lower()) if ((not eliminateStopwords) or (not isStopToken(x[0])))]
        return stemmedwords
    else:
        return [x[0] for x in tokenregex.findall(instr.lower()) if ((not eliminateStopwords) or (not isStopToken(x[0])))]

def tokenizetest(instr, expected):
    res = tokenize(instr)
    if res != expected:
        print("Incorrect tokenization:")
        print(instr, tokenize(instr), expected)

if __name__ == "__main__":
    tokenizetest("nasa", ['nasa'])
    tokenizetest("a.b.c.", ['a.b.c.'])
    tokenizetest("The end .", ['the', 'end'])
    tokenizetest("never-before-seen stuff", ['never-before-seen', 'stuff'])
    tokenizetest("annoying 'quotations' for 'emphasis'", ['annoying', 'quotations', 'for', 'emphasis'])
    tokenizetest("the boys' swords and shields", ['the', 'boys', 'swords', 'and', 'shields'])
    tokenizetest("slumbered 10,000 years", ['slumbered', '10,000', 'years'])
    tokenizetest("dated 12/12/2012", ['dated', '12/12/2012'])
    tokenizetest("his/her pencil", ['his', 'her', 'pencil'])
    tokenizetest("(a)", ['a'])
    tokenizetest("(who was a bit of a jerk)", ['who', 'was', 'a', 'bit', 'of', 'a', 'jerk'])
    print("Test complete")

