import query
import sys

if __name__=="__main__":
    f = open(sys.argv[1], "r")
    for l in f:
        q = l.strip()
        print("{0}".format(query.getScore(q)))
    f.close()

