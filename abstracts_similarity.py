import nltk, string, json
from sklearn.feature_extraction.text import TfidfVectorizer

directories = ['BIO110']

stem = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def stem_tokens(tokens):
    return [stem.stem(item) for item in tokens]

'''remove punctuation, lowercase, stem'''
def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]

'''------------------------------------------------------------------------------------------------'''

for directory in directories:

    f = open('./outputfiles/sparql/abstracts/abstracts_biology_' + directory + '.txt', 'r')
    abstracts = f.read()
    f.close()
    abstracts = json.loads(abstracts)

    result = {}

    for article in abstracts:

        print '--'+article

        abstract = abstracts[article]
        text_sims = []

        for x in abstracts:

            if x != article:

                print '----'+x

                f = open('./data/subtitles-V3-by-topic/Biology/'+directory+'/'+x,'r')
                comp = f.read()
                f.close()

                text_sims.append((comp,cosine_sim(abstract,comp)))

        text_sims.sort(key=lambda x: x[1],reverse=True)
        result[article] = text_sims

    f = open('./outputfiles/sparql/abstracts/abstracts_similarity_biology'+directory+'.txt','w')
    f.write(json.dumps(result))
    f.close()

print 'Scrittura completata'