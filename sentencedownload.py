import datetime, json, csv, sys, math, string, operator, nltk, stopwords, mediacloud
from nltk.tokenize import wordpunct_tokenize
from collections import Counter

###CONFIG###
from ConfigParser import SafeConfigParser
parser = SafeConfigParser()
parser.read('qb-config.txt')
MY_API_KEY = parser.get('API','MY_API_KEY')
mc = mediacloud.api.AdminMediaCloud(MY_API_KEY) #AdminMediaCloud, rather than MediaCloud

f = open('qb-table.csv')
qb_table = csv.reader(f)

m = open('potentialsources.csv') ###should I include sources that haven't gleaned sentences in the past year?
media_reader = csv.reader(m)
media = [x[1] for x in media_reader]	[1:]

stopwords = stopwords.getStopWords()

############################################
	
def wordsearch(team,qb): #MC query, returns list of words 
	words = []
	qb_split = qb.split()
	exclude = list(string.punctuation)+qb_split+team.split()+byteify(stopwords)+['1','2','3','4','5','6','7','8','9','0']
	exclude = [x.lower() for x in exclude]
	for source in media:
		sentences = mc.sentenceList(solr_query=str('"'+qb+'"'), solr_filter=[mc.publish_date_query(datetime.date(2014,9,4), datetime.date(2015,2,1)), '+media_id:'+str(source)], rows = 10000, sort = 'publish_date_desc')
		response = sentences['response']
		docs = response['docs']
		for doc in docs:  
			some_words = byteify(wordpunct_tokenize(doc['sentence']))
			some_words = [x.lower() for x in some_words]
			words += [x for x in some_words if x not in exclude]
	return words
	
def qb_sort(): #reads qb csv, assembles and saves corpus, qb words, qb counted words
	corpus = {}
	#tfidf_dict = {}
	for row in qb_table: #add all qb:words to dictionary (corpus)
		team = row[0]
		qb = row[1]
		file_label = str(qb+' ('+team+')')
		qb_words = wordsearch(team,qb)
		corpus[qb] = qb_words
		qb_words_counted = Counter(qb_words)
		g = open('../quarterback/word-count/'+file_label+'.csv', 'wb')
		try:
			writer = csv.writer(g)
			writer.writerow( ('word', 'count') )
			for i in qb_words_counted:
				writer.writerow((i[0] , i[1]))
		finally:
			g.close()
		json_save('qb-sentences',qb+' ('+team+')',qb_words)
	json_save('qb-sentences','###CORPUS###',corpus)
	# for item in corpus:
		# sorted_dict = wordcount_save(str(item),corpus[item],corpus)
		# tfidf_dict[item] = sorted_dict
		# json_save('sorted-tfidf',str(item),sorted_dict)
	return tfidf_dict

def race_sort(): #assembles corpus, dumps qb words in buckets based on race, calls wordcount_save, tfidf_save for each bucket
	corpus = {}
	white_doc = []
	black_doc = []
	other_doc = []
	hispanic_doc = []
	for row in qb_table:
		team = row[0]
		qb = row[1]
		race = row[2]
		words = wordsearch(team,qb)
		corpus[qb] = words
		print team, qb, len(words)
		if race == 'white':
			white_doc += words
		elif race == 'black':
			black_doc += words
		elif race == 'other':
			other_doc += words
		elif race == 'hispanic':
			hispanic_doc += words
		else:
			print "Race sorting error!", team, qb, race
	white_wordcount_dict = wordcount_save('white_wordcount',white_doc,corpus)
	black_wordcount_dict = wordcount_save('black_wordcount',black_doc,corpus)
	other_wordcount_dict = wordcount_save('other_wordcount',other_doc,corpus)
	hispanic_wordcount_dict = wordcount_save('hispanic_wordcount',hispanic_doc,corpus)
	# white_tfidf_dict = tfidf_save('white_tfidf',white_doc,corpus)
	# black_tfidf_dict = tfidf_save('black_tfidf',black_doc,corpus)
	# other_tfidf_dict = tfidf_save('other_tfidf',other_doc,corpus)
	# hispanic_tfidf_dict = tfidf_save('hispanic_t',hispanic_doc,corpus)

def wordcount_save(label,doc,corpus): #sorts and saves wordcount as JSON and CSV
	counted_doc = dict((x,doc.count(x)) for x in set(doc))
	sorted_doc = sorted(counted_doc.items(), key=operator.itemgetter(1), reverse = True)
	json_save('word-count',label,sorted_doc)
	f = open('../quarterback/word-count/'+label+'.csv', 'wb')
	try:
		writer = csv.writer(f)
		writer.writerow( ('word', 'count') )
		for i in sorted_doc:
			writer.writerow((i[0] , i[1]))
	finally:
		f.close()
		
# def tfidf_save(label,doc,corpus): 
	# tfidf_dict = tf_idf(doc,corpus)
	# sorted_dict = sorted(tfidf_dict.items(), key=operator.itemgetter(1), reverse=True)
	# json_save('sorted-tfidf',label,sorted_dict)
	# f = open('../quarterback/sorted-tfidf/'+label+'.csv', 'wb')
	# try:
		# writer = csv.writer(f)
		# writer.writerow( ('word', 'tf-idf') )
		# for i in sorted_dict:
			# writer.writerow((i[0] , i[1]))
	# finally:
		# f.close()

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input
		
def json_save(file, label, content):
	with open ('../quarterback/'+file+'/'+label+'.txt', "w") as outfile:
		json.dump(content,outfile)
		
if __name__ == "__main__":
	qb_sort()
	race_sort()

# def tf_idf(doc,corpus): #computes tf-idf for each word in each document in the corpus (passed in as dictionary -- {"qb name":[word,word,word], ...})
	# print "START TF-IDF"
	# corpus = byteify(corpus)
	# num_docs = len(corpus)
	# doc = byteify(doc)
	# results = {}
	# corpus_words = []
	# for item in corpus:    
		# corpus_words += corpus[item] 	#builds list (corpus_words) of all words in corpus
	# for word in doc:
		# if word not in results:
			# word_tf  = tf(word,doc)
			# word_idf = idf(word,corpus)
			# results[word] = word_tf*word_idf
	# print 'END TF-IDF'
	# return results
	
# def tf(word,doc):
	# doc_count = doc.count(word)
	# return float(doc_count)/float(len(doc))

# def idf(word,corpus):
	# num_docs = len(corpus) #possible -1 due to csv header inclusion-- fix this later?
	# num_docs_with_word = 0 #do I count the doc in question?
	# for doc in corpus:
		# if word in corpus[doc]: 	
			# num_docs_with_word += 1
	# return math.log(float(num_docs)/float(num_docs_with_word))
