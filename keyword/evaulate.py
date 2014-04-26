import datetime as dt
from Tokenizer import token
from collections import defaultdict

#Change this to use different datasets
import timeweighted_postdata as data
import numpy as np
import math
import operator
import cProfile

#Variable used for altering the threshold to be tested on
threshold = 200

#Old code, not actually used right now. Functionaly is contained in Run()
def main():
	significant_posts = defaultdict(int)
	for post in data.posts:
		try:
			if data.posts[post]["day"][1] - data.posts[post]["day"][2] >= threshold:
				significant_posts[data.posts[post]['title']] = data.posts[post]["day"][1] - data.posts[post]["day"][2]
		except KeyError:
			continue
			#print significant_posts[data.posts[post]['day']]

	print len(significant_posts)

	word_scores, weights = metrics()

	#query = raw_input("Please enter the query that you would like to rate: ")
	score = 0
	for key, value in significant_posts.iteritems():
		tokens = {}
		token.get_tokens(key, tokens, 0, 1)
		for t in tokens:
			score += np.log10(word_scores[t] * weights[t])
		print key
		print "Post Score: " + str(value) + " Score: " + str(score/len(tokens)) + "\n"
			
	#for word in query.split(' '):
	#	print word_scores[word]
	#	print weights[word]
	#	score += word_scores[word] * weights[word]

	#print score/len(query.split(' '))
	#print score

def metrics():
	word_scores = defaultdict(int)
	num_words = defaultdict(int)
	total_num_words = 0
	highest_post = 0
	title = ""

	for post in data.posts:
		tokens = {}
		try:
			#print post
			#print data.posts[post]['title']
			token.get_tokens(data.posts[post]['title'], tokens, 0, 1)
			for t in tokens:
				#Get upvotes
				word_scores[t] += data.posts[post]['day'][1]
				word_scores[t] -= data.posts[post]['day'][2]
				num_words[t] += 1
				total_num_words += 1
			if data.posts[post]["day"][1] > highest_post:
				title = post
				highest_post = data.posts[post]["day"][1]
		except KeyError:
			continue

	weights = defaultdict(float)

	for key, value in num_words.iteritems():
		#weights[key] = np.log10(total_num_words/float(value)+len(num_words));
		weights[key] = 1 - (float(value)/total_num_words)

	for key, value in word_scores.iteritems():
		word_scores[key] = value / num_words[key]

	print highest_post
	print title
	return word_scores, weights

def has_title(p):
    return "title" in p

def run():
	leave_one_out_evaluate()

def leave_one_out_evaluate():
	temp_data = dict(data.posts)
	for post in data.posts:
		try:
			temp = temp_data[post]['title']
		except KeyError:
			temp_data.pop(post)

	data.posts = dict(temp_data)

	average_correct = 0

	posts = {k: post for k,post in data.posts.iteritems() if has_title(post)}

	HOLDOUT = .20

	n = len(posts)
	n_test = int(n * HOLDOUT)
	n_train = n - n_test

	print "{} questions -- {} training -- {} test".format(n, n_train, n_test)

	ids = posts.keys()

	train_ids = ids[:n_train]
	test_ids = ids[n_train:]


	doc_categories = split_by_category(train_ids)
	category_probabilities = train(doc_categories)

	for post in test_ids:

		chosen_category = evaluate(category_probabilities, post)
		#BASELINE
		#chosen_category = "fail"
		if data.posts[post]["day"][1] - data.posts[post]["day"][2] >= threshold:
			if chosen_category is "successful":
				average_correct += 1
		else:
			if chosen_category is "fail":
				average_correct += 1

		#Debug Output
		if False:
			print chosen_category
			print list_of_documents[index]
			print average_correct
	print float(average_correct) / len(test_ids)

def vocabulary(posts):
	vocab = defaultdict(int)
	for post in posts:
		tokens = {}
		token.get_tokens(data.posts[post]['title'], tokens, 0, 1)

		for t in tokens:
			vocab[t] += 1

	return vocab

#Returns the list of probabilities for each word for a particular category
def category_probability(vocabulary, total_vocab):
	word_probabilities = defaultdict(int)
	total_words = 0
	for key, value in vocabulary.iteritems():
		total_words += value

	for key, value in vocabulary.iteritems():
		#TODO
		#Will need to come back to this as I am not entirely sure what n is
		#for now I just divide by vocabulary
		word_probabilities[key] = float((value + 1)) / (total_words)

	return word_probabilities

def train(doc_categories):
	category_probabilities = {}
	total_vocab = {}

	#Generate category probabilities
	for key, value in doc_categories.iteritems():
		total_vocab.update(vocabulary(value))

	for key, value in doc_categories.iteritems():
		category_probabilities[key] = category_probability(vocabulary(value), len(total_vocab))

	return category_probabilities

#Returns hash table contain a list of document by category
def split_by_category(posts):
	doc_categories = {}

	doc_categories["successful"] = []
	doc_categories["fail"] = []

	for post in posts:
		if data.posts[post]["day"][1] - data.posts[post]["day"][2] >= threshold:
			doc_categories["successful"].append(post)
		else:
			doc_categories["fail"].append(post)

	return doc_categories


def evaluate(category_probabilities, post):
	prob_per_category = defaultdict(float)

	total_value = 0
	for key, value in category_probabilities.iteritems():
		total_value += len(value)


	tokens = {}
	token.get_tokens(data.posts[post]['title'], tokens, 0, 0)

	for t in tokens:
		for key, value in category_probabilities.iteritems():
			if t in value:
				prob_per_category[key] += math.log(value[t])



	for key, value in prob_per_category.iteritems():
		print len(category_probabilities[key])/total_value
		value *= len(category_probabilities[key])/total_value

	#DEBUG OUTPUT
	if True:
		print "Probability of true:\t" + str(prob_per_category["successful"])
		print "Probability of lie:\t" + str(prob_per_category["fail"])

	return min(prob_per_category.iteritems(), key=operator.itemgetter(1))[0]


if __name__ == "__main__":
		#cProfile.run('run()')
		run()