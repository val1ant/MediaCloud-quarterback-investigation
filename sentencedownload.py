import datetime, json, csv, sys, math, string, operator, nltk, stopwords, mediacloud
from nltk.tokenize import wordpunct_tokenize
from collections import Counter

###CONFIG###
from ConfigParser import SafeConfigParser
parser = SafeConfigParser()
parser.read('config.txt')
MY_API_KEY = parser.get('API','MY_API_KEY')
mc = mediacloud.api.AdminMediaCloud(MY_API_KEY) #AdminMediaCloud, rather than MediaCloud

f = open('qb-table.csv')
qb_table = csv.reader(f)

m = open('sources.csv') ###should I include sources that haven't gleaned sentences in the past year?
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


def sortnsave(): #assembles corpus, dumps qb words in buckets based on race, calls wordcount_save, tfidf_save for each bucket
	corpus = {}
	count_corpus = {}
	white_doc = []
	black_doc = []
	other_doc = []
	hispanic_doc = []
	for row in qb_table:
		team = row[0]
		qb = row[1]
		race = row[2]
		file_label = str(qb+' ('+team+')')
		qb_words = wordsearch(team,qb)
		json_save('words/player/',file_label,qb_words)
		corpus[qb] = qb_words
		counted_doc = dict((x,qb_words.count(x)) for x in set(qb_words)) 
		sorted_doc = sorted(counted_doc.items(), key=operator.itemgetter(1), reverse = True) 
		count_corpus[qb] = counted_doc
		json_save('counts/player/',file_label,sorted_doc)
		print team, qb, len(qb_words)
		if race == 'white':
			white_doc += qb_words
		elif race == 'black':
			black_doc += qb_words
		elif race == 'other':
			other_doc += qb_words
		elif race == 'hispanic':
			hispanic_doc += qb_words
		else:
			print "Race sorting error!", team, qb, race
	json_save('words','###CORPUS###',corpus)
	json_save('counts','###CORPUS###',count_corpus)
	json_save('words/white_words','white_words',white_doc)
	json_save('words/black_words','black_words',black_doc)
	json_save('words/other_words','other_words',other_doc)
	json_save('words/hispanic_words','hispanic_words',hispanic_doc)
	white_counts = dict((x,white_doc.count(x)) for x in set(white_doc)) 
	json_save('counts/white_wordcount','white_counts',white_counts)
	black_counts = dict((x,black_doc.count(x)) for x in set(black_doc)) 
	json_save('counts/black_wordcount','black_counts',black_counts)
	other_counts = dict((x,other_doc.count(x)) for x in set(other_doc)) 
	json_save('counts/other_wordcount','other_counts',other_counts)
	hispanic_counts = dict((x,hispanic_doc.count(x)) for x in set(hispanic_doc)) 
	json_save('counts/hispanic_wordcount','hispanic_counts'hispanic_counts)

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
	with open ('../quarterback/data/'+file+'/'+label+'.txt', "w") as outfile:
		json.dump(content,outfile)
		
if __name__ == "__main__":
	sortnsave()
	
	
#########################################################################################################################

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
