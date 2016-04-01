#@author: Ziyan Liu

import json
import string
#from nltk.stem import PorterStemmer

#stemmer=PorterStemmer()
word_dictionary = {}
posts = []
translator = str.maketrans({key: None for key in string.punctuation})
with open('dgaz.json', encoding="utf8") as f:
    for line in f:
        posts.append(json.loads(line))
for post in posts:
	mesg = post['body']
	for word in mesg.split(" "):
		#stemmed_word = stemmer.stem('word')
		if (len(word) > 0):
			if (word[0] != '$'):
				word = word.translate(translator)
				print(word)
				if(word not in word_dictionary.keys()):
					word_dictionary[word] = 0
				word_dictionary[word] = word_dictionary[word]+1
for key in word_dictionary:
	print ("key is "  + key + "		and value is", word_dictionary[key])