'''
Nathaniel Price
Uniquename: nrprice
EECS 498
'''

import re
import operator
import os
#import cProfile
from optparse import OptionParser
from stemming.porter2 import stem

def main():
	parser = OptionParser()
	usage = "usage: %prog [options] arg1 arg2"

	parser.add_option("-p", "--porter", action="store_true", 
		help="Activates Porter Stemmer", dest="port", default=False)
	parser.add_option("-s", "--stop", action="store_true",
		help="Activates Stop Words", dest="stop", default=False)
	parser.add_option("-c", "--count", type="int", 
		dest="num_tokens", help="Number of Tokens to output")
	parser.add_option("-v", "--verbose", action="store_true", 
		help="Activates Verbose Mode, indicating when each document is being parsed",
		dest="verbose", default=False)

	options, arguments = parser.parse_args()

	num_tokens = 20
	if(options.num_tokens):
		num_tokens = options.num_tokens

	run(num_tokens, options.port, options.stop, options.verbose)


def run(num_tokens, port, stop, verbose):

	line_num = 1

	list_of_docs = []
	doc_contents = ""

	tokens = {}

	for fn in os.listdir('cranfieldDocs'):
		if verbose:
			print "Tokenizing Document: " + fn
		doc_contents = ''
		for line in open('cranfieldDocs/' + fn, 'r+'):
			doc_contents += remove_tags(line)
			line_num += 1

			doc_contents = pre_process_text(doc_contents)

			get_tokens(doc_contents, tokens, port, stop)

	print "Sorting..."
	sorted_x = sorted(tokens.iteritems(), key=operator.itemgetter(1))[::-1]

	#used for question 2
	total_num_words = 0
	current_num_tokens = 0

	for key, value in sorted_x:
		if(current_num_tokens < num_tokens):
			print key + " " + str(value)
		current_num_tokens += 1
		
		total_num_words += value

	return sorted_x

	print "Number of Unique Tokens:\t" + str(len(tokens))
	print "Total Number of Words:\t" + str(total_num_words)

def tokenize_doc(document, port, stop):
	doc_contents = ""
	tokens = {}

	for line in open(document, 'r+'):
		doc_contents += remove_tags(line)

		doc_contents = pre_process_text(doc_contents)

		get_tokens(doc_contents, tokens, port, stop)

	return tokens

def remove_tags(line):

	regex = re.compile(r'<.*?>')
	result = regex.sub('', line)
	return result

def pre_process_text(text):
	#make everything lowercase
	text.lower()
	#remove newlines
	text = re.sub('\n', ' ', text)
	text = re.sub('[\(/\)]', '', text)
	return text

def get_tokens(text, tokens, port, stop):
	#first just simply get all tokens as everything that is split appart
	list_of_tokens = text.split(' ')

	list_of_tokens = filter(None,list_of_tokens)

	skip_next = False

	#iterate over list of tokens
	for index, token in enumerate(list_of_tokens):
		if skip_next:
			skip_next = False
			continue

		token = remove_trailing_characters(token)

		#stem words
		if port:
			token = stem(token)

		
		if check_month(token):
			date = is_date(list_of_tokens, token, index)
			add_to_tokens(date, tokens)
			skip_next = True
			continue
		

		if possesive_check(token):
			add_to_tokens(token[:-2], tokens)
			add_to_tokens('is', tokens)
			continue


		add_to_tokens(token, tokens)

	#Empty strings were still being added to the dictionary
	if '' in tokens:
		del tokens['']
	if None in tokens:
		del tokens[None]


	if stop:
		for key, value in tokens.items():
		#Get rid of stop words			
			if stop_words(key):
				del tokens[key]


	list_of_tokens = []
	
	

def is_num(value):
	try:
		i = float(value)
		return True
	except ValueError, TypeError:
		return False

def add_to_tokens(token, tokens):
	if token in tokens:
		tokens[token] += 1
	else:
		tokens[token] = 1

def possesive_check(token):
	if token[-2:] == '\'s':
		return True

def is_date(list_of_tokens, token, index):
	a = 0
	try:
		return token + " " + list_of_tokens[index+1]
	except Exception:
		a = a

def remove_trailing_characters(value):
	#remove trailing periods
	if value[-1:] == '.':
		value = value[:-1]

	#remove trailing commas
	if value[-1:] == ',':
		value = value[:-1]

	if value[-1:] == '\'':
		value = value[:-1]

	return value

def check_month(string):
	#excluded 'may' because it occurs too often in other contexts to be regularly next to a year/date
	list_of_months = ['january', 'febuary', 'march', 'april', 'june', 'july',
	'august', 'september', 'october', 'november', 'december']
	if [e in string for e in list_of_months if e in string]:
		return True

	return False

def stop_words(string):
	list_of_stop_words = ['a', 'all', 'an', 'and', 'any', 'are', 'as', 'be', 
	'been', 'but', 'by', 'few', 'for', 'have', 'he', 'her', 'here', 'him', 
	'his', 'how', 'i', 'in', 'is', 'it', 'its', 'many', 'me', 'my', 'none', 
	'of', 'on', 'or', 'our', 'she', 'some', 'the', 'their', 'them', 'there', 
	'they', 'that', 'this', 'us', 'was', 'what', 'when', 'where', 'which', 
	'who', 'why', 'will', 'with', 'you', 'your']
	if any(e == string for e in list_of_stop_words):
		return True

	return False

if __name__ == "__main__":
    #cProfile.run('main()')
    main()