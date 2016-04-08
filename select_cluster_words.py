import json
import sys

diction = {}
words = []

data = {}
with open(sys.argv[1]) as data_file:    
    data = json.load(data_file)
    for word in data.keys():
        words.append(word)
    words = set(words)

print "finish loading source file"
print words
print len(words)


with open(sys.argv[2], "r") as ins:
    for line in ins:
        line = line[:-1]
        array = line.split(" ")
        if array[0] in words:
        	diction[array[0]] = array[1:]
        	if len(diction) % 100 == 0:
        		print len(diction)

non_exist_words = words - set(diction.keys())
non_exist_words_tup = []
for w in non_exist_words:
    tup = (w, data[w])
    non_exist_words_tup.append(tup)

non_exist_words_tup.sort(key=lambda tup: tup[1])

for w in non_exist_words_tup:
    print w

with open(sys.argv[3], 'w+') as outfile:
        json.dump(diction, outfile)