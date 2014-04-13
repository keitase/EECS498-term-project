#!/usr/bin/env python

# David Purser (dpurser)
# EECS 498 Information Retrieval
# Assignment 2 - Part 1/2/3
# Indexer / Query Processor

# For logarithm, etc.
import math

# For dicts that default to 0
from collections import defaultdict

import tokenizer

class indexer(object):
    def __init__(self):
        self.docs = {}
        self.docMags = None
        self.idfs = None
        self.globalTokenDocs = {}
        self.invertedIndex = {}

    def addDocument(self, name, tokens):
        if len(tokens) == 0:
            return

        # Count the tokens for this document
        tokenFreq = defaultdict(int)
        for t in tokens:
            tokenFreq[t] += 1

        for t,v in tokenFreq.items():
            if t in self.globalTokenDocs:
                self.globalTokenDocs[t] += 1
            else:
                self.invertedIndex[t] = set()
                self.globalTokenDocs[t] = 1
            self.invertedIndex[t].add(name)

        self.docs[name] = tokenFreq
    
    def makeDocumentVectors(self):
        print("Calculating document vector magnitudes...")
        self.docMags = {}
        idfs = {}
        numTokens = len(self.globalTokenDocs)
        N = float(len(self.docs))

        for t,df in self.globalTokenDocs.items():
            idfs[t] = math.log10(N / float(df))

        for docid,tokens in self.docs.items():
            vecmag = 0
            for t,tf in tokens.items():
                val = tf*idfs[t]
                vecmag += val * val
            self.docMags[docid] = math.sqrt(vecmag)
        self.idfs = idfs

    # scheme = 0: unnormalized tf-idf
    # scheme = 1: tfc-nfx from the paper
    def queryVector(self, queryTokens, scheme):
        docScores = []
        N = float(len(self.docs))

        queryTokenFreqs = {}

        if self.docMags is None:
            print("Tried to query, but document vectors haven't been calculated yet! Doing it now...")
            self.makeDocumentVectors()

        for t in queryTokens:
            if t not in self.invertedIndex:
                continue # no documents have this term
            if t in queryTokenFreqs:
                queryTokenFreqs[t] += 1.0
            else:
                queryTokenFreqs[t] = 1.0
        
        if len(queryTokenFreqs) == 0: # no documents have any of the query terms
            return []

        possibleDocs = set()
        for t in queryTokenFreqs:
            possibleDocs.update(self.invertedIndex[t])

        #print("{0} out of {1} docs are possible matches".format(len(possibleDocs), len(self.docs)))

        docNums = {}
        for docid in possibleDocs:
            docNums[docid] = 0

        maxqrytf = float(max(queryTokenFreqs.values()))

        querymag = 0

        for t, qrytf in queryTokenFreqs.items():
            idf = self.idfs[t] #math.log10(N / float(self.globalTokenDocs[t]))
            if scheme == 0:
                queryVal = qrytf*idf
                for docid in possibleDocs:
                    tf = float(self.docs[docid].get(t, 0))
                    docNums[docid] += (tf * idf) * queryVal
            else:
                nterm = 0.5 + (0.5 * qrytf) / (maxqrytf)
                queryVal = nterm * idf
                for docid in possibleDocs:
                    tf = float(self.docs[docid].get(t, 0))
                    docNums[docid] += (tf * idf / self.docMags[docid]) * queryVal
            querymag += queryVal * queryVal
        querymag = math.sqrt(querymag)

        # Calculate similarities
        for docid, docNum in docNums.items():
            docVectorMag = self.docMags[docid] if scheme == 0 else 1.0
            sim = docNum / (querymag * docVectorMag)
            if sim > 0:
                docScores.append((docid, sim))

        docScores.sort(key = lambda x: -x[1])

        return docScores

    def printQueryResults(self, query, scheme):
        res = self.queryVector(query, scheme)
        print("{0} results.".format(len(res)))
        print("{0:5s} {1:100s} {2:10s}".format("Rank", "Document", "Similarity"))
        i = 0
        for n in res:
            i += 1
            docid = n[0].ljust(100) # this way it won't get cut off
            print("{0:5d} {1} {2:10.5f}".format(i, docid, n[1]))

    def interactive(self):
        scheme = 1

        while True:
            #if scheme == 0:
            #    print("Using tf-idf non-normalized weighting scheme (implements problem 1.1)")
            #else:
            #    print("Using tf-idf normalized weighting scheme ('tfc-nfx' from Salton & Buckley 1988) (implements problem 1.2)")

            #print("Enter query (or enter '+exit' to exit, '+scheme' to change weighting scheme):")
            print("Enter query (or enter '+exit' to exit):")
            query = raw_input("")
            if query == "+exit":
                break
            #elif query == "+scheme":
            #    if scheme == 0:
            #        scheme = 1
            #    else:
            #        scheme = 0
            else:
                self.printQueryResults(tokenizer.tokenize(query), scheme)



