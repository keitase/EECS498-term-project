import datetime
import data

# assumes input coming from 'data.py'
# where the variable name is 'stale = '...
# data.py must "import datetime"

# generates postdata.py, with all the titles and everything

posts = {}

for p in data.stale:
    for n in p:
        assert(n['id'] not in posts)
        posts[str(n['id'])] = n
        #print(n)

import pprint
#pprint.pprint(posts)
#pprint.pprint(posts.keys())

import downloadtitles
titles = downloadtitles.getData(posts.keys())

for n in titles.keys():
    for c,d in titles[n].items():
        posts[n][c] = d
    print(posts[n])

for c in posts.keys():
    if c not in titles:
        print("NO DATA FOR {0}".format(c))

of = file('./postdata.py', 'w')
of.write('import datetime\n')
of.write('posts = ' + repr(posts))
of.close()

