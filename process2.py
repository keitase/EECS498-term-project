# I wrote this in like 20 minutes and it's really really ugly,
# but it only has one job and it does it pretty well
# so don't kill me please

import postdata
import math

thresh_above = {}
thresh_below = {}
threshold_score = 20

totalhourthresh = 1

# Must divide 24 evenly (valid values are 1, 2, 3, 4, 6, 8, 12.  also, 0.5 might work, but uh, good luck)
hour_bin_size = 2

hour_posts = {}
hour_sum = {}
hour_avg = {}
hour_thresh = {}
hour_threshscore = 20
for a in range(24 / hour_bin_size):
    hour_sum[a] = 0
    hour_posts[a] = {}
    hour_avg[a] = 0
    hour_thresh[a] = 0

for id,n in postdata.posts.items():
    if "title" not in n:
        continue
    # created
    hrnum = math.floor(n["created"].hour / hour_bin_size)
    hour_posts[hrnum][id] = n
    hour_sum[hrnum] += n["day"][1]
    if n["day"][1] >= threshold_score:
        thresh_above[id] = n
    else:
        thresh_below[id] = n
    if n["day"][1] >= hour_threshscore:
        hour_thresh[hrnum] += 1
        totalhourthresh += 1

totalwithtitle = len(thresh_above) + len(thresh_below)
print("{0:5d} posts total; {1:5d} posts ({2:7.4f}%) above threshold of {3:4d} upvotes ({4:5d} posts ({5:7.4f}%) below threshold)".format(totalwithtitle, len(thresh_above), (float(len(thresh_above)) / float(totalwithtitle)) * 100.0, threshold_score, len(thresh_below), (float(len(thresh_below)) / float(totalwithtitle) * 100.0)))

mergedposts = {}

assert(len(thresh_above) < len(thresh_below))

# add all posts above threshold
for id,n in thresh_above.items():
    mergedposts[id] = n
# add same number of posts from below the threshold
for id,n in thresh_below.items():
    mergedposts[id] = n
    if len(mergedposts) >= 2*len(thresh_above):
        break

f = file("balanced_postdata.py", "w")
f.write("import datetime\nposts = ")
f.write(repr(mergedposts))
f.write("\n")
f.close()

weightedposts = {}

for a in range(24 / hour_bin_size):
    hour_avg[a] = float(len(hour_posts[a])) / float(hour_sum[a])

    # how many times greater than the expected average value is this bin?
    threshratio = float(hour_thresh[a]) / totalhourthresh * (24.0 / hour_bin_size)

    print("Hour {0:2d}-{5:2d}: {1:5d} posts averaging {2:7.4f} upvotes; {3:5d} posts above threshold which is {4:7.4f} times the E.V.".format(a*hour_bin_size, len(hour_posts[a]), hour_avg[a], hour_thresh[a], threshratio, (a+1) * hour_bin_size - 1))

    # divide all the posts in that bin by the threshratio (bins with "more good posts" will have scores scaled down)
    for id,b in hour_posts[a].items():
        for r in ("hour", "6 hrs", "12 hrs", "day"):
            # can't modify tuples :(((
            b[r] = (b[r][0], float(b[r][1]) / threshratio, float(b[r][2]) / threshratio)
        b["num_comments"] = float(b["num_comments"]) / threshratio
        weightedposts[id] = b

f = file("timeweighted_postdata.py", "w")
f.write("import datetime\nposts = ")
f.write(repr(weightedposts))
f.write("\n")
f.close()

# these posts are shallow copies so they will be modified as well
f = file("balanced_timeweighted_postdata.py", "w")
f.write("import datetime\nposts = ")
f.write(repr(mergedposts))
f.write("\n")
f.close()

