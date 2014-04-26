import datetime as dt
from Tokenizer import token
from collections import defaultdict
import postdata as data

def main():
	word_scores()

def word_scores():
	scores = defaultdict(int)
	num_words = defaultdict(int)
	for post in data.posts:
		tokens = {}
		print data.posts[post]['title']
		token.get_tokens(data.posts[post]['title'], tokens, 0, 0)
		for t in tokens:
			print t
		break


if __name__ == "__main__":
    main()