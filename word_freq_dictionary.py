#@author: Ziyan Liu

import json
import string
#from nltk.stem import PorterStemmer

#stemmer=PorterStemmer()
big_dictionary = {}
filenames = ['dgaz','dust','dwti','jdst','jnug','nugt','ugaz','uso','uwti']
translator = str.maketrans({key: None for key in string.punctuation})
for filename in filenames:
	word_dictionary = {}
	posts = []
	with open(filename + '.json', encoding="utf8") as f:
	    for line in f:
	        posts.append(json.loads(line))
	for post in posts:
		mesg = post['body']
		for word in mesg.split(" "):
			#stemmed_word = stemmer.stem('word')
			if (len(word) > 0):
				if (word[0] != '$'):
					word = word.translate(translator)
					if (len(word) > 0):
						if(word not in word_dictionary.keys()):
							word_dictionary[word] = 0
						word_dictionary[word] = word_dictionary[word]+1


						if(word not in big_dictionary.keys()):
							big_dictionary[word] = 0
						big_dictionary[word] = big_dictionary[word]+1
	with open('output_' + filename + '.json', 'w') as fp:
		json.dump(word_dictionary, fp)
with open('bigoutput.json', 'w') as fp:
		json.dump(big_dictionary, fp)
#for key in word_dictionary:
#	print ("key is "  + key + "		and value is", word_dictionary[key])


