import indexer
import tokenizer

import postdata

# Can use by importing this file and using query.getScore("Some title of a post")

idx = indexer.indexer()

for i,p in postdata.posts.items():
    if "title" in p: # some posts don't have titles (means they were deleted/some other error happened to them)
        title = p["title"].encode('ascii','ignore')
        selftext = p["selftext"].encode('ascii','ignore')
        tokens = tokenizer.tokenize(title, True, True)
        idx.addDocument(p["id"], tokens)

idx.makeDocumentVectors()

def getScore(newtitle):
    query = tokenizer.tokenize(newtitle, True, True)
    res = idx.queryVector(query, 1)
    print("{0} results.".format(len(res)))
    
    # Take average of (upvotes-downvotes) weighted by similarity score ^ 2
    # but only for posts with simscore > max(simscore)/2
    totalweight = 0.0
    totalscore = 0.0
    for n in res:
        simscore = n[1] / res[0][1]
        simscore2 = simscore
        simscore *= simscore
        if simscore < 0.5:
            continue

        post = postdata.posts[n[0]]
        #score = post["day"][1] - post["day"][2]/2 # ups - downs/2
        score = post["day"][1]
        totalscore += float(score) * simscore
        totalweight += simscore

    if totalweight == 0:
        return 0.0 # couldn't make a score for this

    finalscore = (totalscore / totalweight) ** 2

    return finalscore

if __name__=="__main__":
    while True:
        print("")
        print("Enter query (or enter '+exit' to exit):")
        query = raw_input("")
        if query == "+exit":
            break
        else:
            print("Score: {0}".format(getScore(query)))

