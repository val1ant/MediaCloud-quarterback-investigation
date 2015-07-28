import nltk, logging
import string
import os
import math,operator,json,unicodecsv

logging.basicConfig(level=logging.DEBUG	)

try:
	from sklearn.feature_extraction.text import TfidfVectorizer
	scikit = True
except ImportError:
	scikit = False
	
from nltk.stem.porter import PorterStemmer

### NOTE: scikit will only yield a corpus for each run (player, race). Alternate TF-IDF will yield a corpus *and* individual files. ###
### Additionally, scikit tokenizes words, while my tf-idf does not. ###

token_dict = {}
stemmer = PorterStemmer()

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems
		
#############################################

def tf_idf(collection): #computes tf-idf for each word in each document in the corpus (passed in as dictionary -- {"qb name":[word,word,word], ...})
	logging.info('Computing tfidf for all %ss' % collection)
	path = os.path.join('data','json','words',collection)
	if not os.path.exists(path):
		os.makedirs(path)
	token_dict = {}
	for subdir, dirs, files in os.walk(path):
		for file in files:
			file_path = subdir + os.path.sep + file
			shakes = open(file_path, 'r')
			text = shakes.read()
			lowers = text.lower()
			no_punctuation = lowers.translate(None, string.punctuation)
			token_dict[file] = no_punctuation
	corpus = token_dict
	num_docs = len(corpus)
	corp_results = {}
	for item in corpus:
		filename = item[:-4]
		doc = corpus[item].split(' ')
		results = {}
		for word in doc:
			if word not in results:
				word_tf  = tf(word,doc)
				word_idf = idf(word,corpus)
				results[word] = word_tf*word_idf
		sorted_results = sorted(results.items(), key=operator.itemgetter(1), reverse=True)
		corp_results[filename] = sorted_results
		directory = os.path.join('data','json','tfidf',collection)
		if not os.path.exists(directory):
			os.makedirs(directory)
		with open( os.path.join(directory,filename+'.json'), "w") as outfile: 
			json.dump(sorted_results,outfile)
		directory = os.path.join('data','csv','tfidf',collection)
		if not os.path.exists(directory):
			os.makedirs(directory)
		with open( os.path.join(directory,filename+'.csv'), "wb") as outfile: 
			try:
				w = unicodecsv.writer(outfile)
				w.writerow( ('WORD', 'TF-IDF') )
				for i in results:
					w.writerow( (i, results[i]) )
			finally:
				outfile.close()
	with open( os.path.join('data','json','tfidf','###'+collection.upper()+'CORPUS###.txt'), "w") as outfile:  
		json.dump(corp_results,outfile)
	
def tf(word,doc):
	doc_count = doc.count(word)
	return float(doc_count)/float(len(doc))

def idf(word,corpus):
	num_docs = len(corpus) #possible -1 due to csv header inclusion-- fix this later?
	num_docs_with_word = 0 #do I count the doc in question?
	for doc in corpus:
		if word in corpus[doc]: 	
			num_docs_with_word += 1
	return math.log(float(num_docs)/float(num_docs_with_word))
        
#############################################	

if __name__ == "__main__":
	if scikit:
		logging.info('(using scikit)')
		for x in ['player','race']:
			path = os.path.join('quarterback','data','json','words',x)
			for subdir, dirs, files in os.walk(path):
				for file in files:
					file_path = subdir + os.path.sep + file
					shakes = open(file_path, 'r')
					text = shakes.read()
					lowers = text.lower()
					no_punctuation = lowers.translate(None, string.punctuation)
					token_dict[file] = no_punctuation
			tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
			tfs = tfidf.fit_transform(token_dict.values())
			with open(os.path.join('data','json','tfidf',x+'###CORPUS###.txt'), "w") as outfile: 
				json.dump(tfs,outfile)
	else:
		tf_idf('player')
		tf_idf('race')
