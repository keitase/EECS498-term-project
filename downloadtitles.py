import praw

def getData(ids):
    # gets data for all the ids in 'ids' list
    user_agent = "EECS 498 Term Project - contact noodle@umich.edu"
    reddit = praw.Reddit(user_agent)
    
    t3ids = []
    for n in ids:
        t3ids.append(str('t3_' + n))

    #if len(t3ids) > 10:
    #    t3ids = t3ids[:10]

    data = {}

    i = 0
    print("Downloading titles/etc. for {0} submissions".format(len(t3ids)))
    subs = reddit.get_submissions(t3ids)
    for sub in subs:
        i = i + 1
        print("Downloading: {0} / {1}".format(i, len(t3ids)))
        try:
            data[sub.id] = {
                 'title': sub.title,
                 'author': sub.author.name,
                 'selftext': sub.selftext,
                 'num_comments': sub.num_comments
                 }
            # print(str(sub.id), sub.title, sub.author.name, sub.selftext)
        except Exception:
            # post deleted?
            pass
    return data

