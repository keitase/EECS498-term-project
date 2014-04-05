import praw
import bmemcached
import os
import datetime as dt

from pprint import pprint as pp

def reddit_login():
    user_agent = "EECS 498 Term Project - contact noodle@umich.edu"
    reddit = praw.Reddit(user_agent)

    username = "answer-bot"
    password = os.environ.get('ANSWER_BOT_PASSWORD')
    reddit.login(username, password)

    return reddit

def memcached_login():
    servers = os.environ.get('MEMCACHEDCLOUD_SERVERS')
    username = os.environ.get('MEMCACHEDCLOUD_USERNAME')
    password = os.environ.get('MEMCACHEDCLOUD_PASSWORD')
    
    if servers: # running on Heroku
        return bmemcached.Client(servers.split(','), username, password)
    else: # localhost
        return bmemcached.Client(['127.0.0.1:11211'])

def is_question(post):
    question = r'^.*\?$'
    if re.match(question, post.body):
        return True
    else:
        return False

def single_word(post):
    return not re.match(r'^.* .*$', post.body)

def says_reference(post):
    reference = r'^.*reference.*$'
    if re.match(reference, post.body):
        return True
    else:
        return False

def comments():
    reddit = reddit_login()

    for post in praw.helpers.comment_stream(reddit, 'all', verbosity=0):
        if is_question(post):
            p = post
            chain = []
            while type(p) == praw.objects.Comment:
                chain.append(p)
                p = reddit.get_info(thing_id=p.parent_id)
            print
            for i,p in enumerate(reversed(chain)):
                print "\t"*i + p.body
        else:
            print '.',

def askreddit():
    reddit = reddit_login()
    ask_reddit = reddit.get_subreddit('askreddit')
    for question in praw.helpers.submission_stream(reddit, ask_reddit, verbosity=0):
        print
        print question

def ask_cron():
    reddit = reddit_login()
    mc = memcached_login()

    unow = dt.datetime.utcnow()

    old_titles = mc.get('question_titles') or []
    old_ids = mc.get('question_ids') or set()

    ask_reddit = reddit.get_subreddit('askreddit')
    newest = [s for s in ask_reddit.get_new() if s.id not in old_ids]
    
    # [{"id": id, "created": created, "scores": [(time, ups, downs)..]}..]
    new_scores = [{
        "id": s.id,
        "created": dt.datetime.utcfromtimestamp(s.created_utc), 
        "scores": []
        } for s in newest]

    pending = mc.get('question_scores') or []
    stored = mc.get('question_scores_done') or []

    still_scores = [s for s in pending if (unow - s["created"]).days < 1]
    new_stores = [s for s in pending if (unow - s["created"]).days > 0]

    for s in still_scores:
        s_id = s["id"]
        current = r.get_submission(submission_id=s_id)
        s["scores"].append((unow, current.ups, current.downs))

    new_titles = [n.title for n in newest]
    new_ids = set([n.id for n in newest])

    mc.set('question_titles', new_titles + old_titles)
    mc.set('question_ids', new_ids.union(old_ids))

    mc.set('question_scores', new_scores + still_scoring)
    mc.set('question_scores_done', new_stores + stored)

if __name__ == "__main__":
    ask_cron()