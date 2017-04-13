import sys
import os
import re
import operator
from stemmer import *

# Uniquename: mamolina

# Dictionary of all possible expansions
expands = {"i'll": ['i', 'will'], "'twas": ['it', 'was'], "she'll": ['she', 'will'], "why'd": ['why', 'did'], "don't": ['do', 'not'], "should've": ['should', 'have'], "didn't": ['did', 'not'], "they've": ['they', 'have'], "who'll": ['who', 'will'], "won't": ['would', 'not'], "we'd": ['we', 'would'], "couldn't": ['could', 'not'], "how'll": ['how', 'will'], "why's": ['why', 'is'], "you'd": ['you', 'would'], "doesn't": ['does', 'not'], "might've": ['might', 'have'], "how's": ['how', 'is'], "he's": ['he', 'is'], "when's": ['when', 'is'], "where'd": ['where', 'did'], "what'd": ['what', 'did'], "he'd": ['he', 'would'], "can't": ['can', 'not'], "how'd": ['how', 'did'], "there's": ['there', 'is'], "shouldn't": ['should', 'not'], "they'll": ['they', 'will'], "when'll": ['when', 'will'], "where'll": ['where', 'will'], "you're": ['you', 'are'], "we're": ['we', 'are'], "mightn't": ['might', 'not'], "i've": ['i', 'have'], "'tis": ['it', 'is'], "what's": ['what', 'is'], "who's": ['who', 'is'], "where's": ['where', 'is'], "they'd": ['they', 'would'], "ain't": ['is', 'not'], "you've": ['you', 'have'], "would've": ['would', 'have'], "that'll": ['that', 'will'], "aren't": ['are', 'not'], "who'd": ['who', 'would'], "he'll": ['he', 'will'], "must've": ['must', 'have'], "they're": ['they', 'are'], "we'll": ['we', 'will'], "why'll": ['why', 'will'], "weren't": ['were', 'not'], "wasn't": ['was', 'not'], "wouldn't": ['would', 'not'], "hasn't": ['has', 'not'], "she'd": ['she', 'would'], "you'll": ['you', 'will'], "i'd": ['i', 'would'], "could've": ['could', 'have'], "she's": ['she', 'is'], "i'm": ['i', 'am'], "when'd": ['when', 'did'], "mustn't": ['must', 'not'], "isn't": ['is', 'not'], "that's": ['that', 'is']}

# List of stopwords
stopWords = ['a', 'all', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'been', 'but', 'by', 'few', 'from', 'for', 'have', 'he', 'her', 'here', 'him', 'his', 'how', 'i', 'in', 'is', 'it', 'its', 'many', 'me', 'my', 'none', 'of', 'on', 'or', 'our', 'she', 'some', 'the', 'their', 'them', 'there', 'they', 'that', 'this', 'to', 'us', 'was', 'what', 'when', 'where', 'which', 'who', 'why', 'will', 'with', 'you', 'your']

months = ['january', 'jan.', 'feb.', 'february', 'march', 'mar.', 'april', 'apr.', 'may', 'june', 'july', 'august', 'aug.', 'sept.', 'september', 'oct.', 'october', 'nov.', 'november', 'dec.', 'december']

special_chars = ["", "+", "-", "=", "&", "%", ",", ".", "'"]

# Removes any SGML tags present
def removeSGML(text):
	if '</' in text:
		text = text.replace('</','')
	if '<' in text:
		text = text.replace('<','')
	if '>' in text:
		text = text.replace('>', '')
	return text

# Returns true if the token has a number
def has_number(token):
	return any(char.isdigit() for char in token)

# Returns true if the token is a number
def is_number(token):
	return all(char.isdigit() for char in token)

# Removes parenthesis and slashes from the token
def remove_parenthesis_slash(token):
	if "(" in token:
		token = token.replace("(", "")
	if ")" in token:
		token = token.replace(")", "")
	if "/" in token:
		toekn = token.replace("/", "")
	return token

# Tokenizes the contents of the document
def tokenizeText(text):
	tokens = []
	split_text = text.split()
	is_date = False
	month = ''
	for item in split_text:
		if item in expands:
			for word in expands[item]:
				tokens.append(word)
		elif "'" in item:
			h_pos = item.find("'")
			tokens.append(item[:h_pos])
			tokens.append(item[h_pos:])
		elif "," in item and not has_number(item):
			for each in item.split(","):
				if (item[len(item) - 1] == "." and item.count(".") == 1 and len(each) > 1):
					tokens.append(item[:len(item) - 1])
				elif each != "." and each != "":
					tokens.append(each)
		elif item[len(item) - 1] == "," or (item[len(item) - 1] == "." and item.count(".") == 1) or item[len(item) - 1] == "?" or item[len(item) - 1] == "!":
			tokens.append(item[:len(item) - 1])
		elif item in months:
			is_date = True
			month = item
		elif is_date and is_number(item):
			tokens.append(month + ' ' + item)
			is_date = False
		elif item != "":
			tokens.append(item)

	tokens = filter(lambda x: x not in special_chars, tokens)

	return tokens

def removeStopwords(tokens):
	new_list = []
	for item in tokens:
		if item not in stopWords:
			new_list.append(item)
	return new_list

def stemWords(tokens):
	stemmed_tokens = []
	for index, elem in enumerate(tokens):
		if all(each.isalpha() for each in elem):
			each = PorterStemmer()
			stemmed_tokens.append(each.stem(elem, 0, len(elem) - 1))
		else:
			stemmed_tokens.append(elem)

	return stemmed_tokens

if __name__ == '__main__':
	dirname = sys.argv[1]
	words = {}
	total = 0

	for filename in os.listdir(dirname):
		f = open(dirname + filename, 'r')
		content = f.read().replace('\n', ' ')

		content = content.lower()
		content = removeSGML(content)
		content = remove_parenthesis_slash(content)
		tokens = tokenizeText(content)
		tokens = removeStopwords(tokens)
		stemmed_tokens = stemWords(tokens)

		for token in stemmed_tokens:
			if token not in words:
				words[token] = 0
			words[token] += 1
			total += 1

	print 'Words ' + str(total)
	print 'Vocabulary ' + str(len(words))

	sorted_words = sorted(words.items(), key=operator.itemgetter(1), reverse=True)

	count = 0
	for word in sorted_words:
		if count == 50:
			break
		print word[0] + ' ' + str(word[1])
		count += 1
