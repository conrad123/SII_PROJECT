import nltk, glob, os, json, string
from sklearn.feature_extraction.text import TfidfVectorizer
from difflib import SequenceMatcher




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

def word_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


#directories = ['CS212-01', 'CS212-02', 'CS212-02ps', 'CS212-02x', 'CS212-03', 'CS212-03ps', 'CS212-03x', 'CS212-04', 'CS212-05', 'CS212-05ps', 'CS212-06', 'CS212-06ps', 'CS212-06x', 'CS212-07']

f = open( './outputfiles/sparql/abstracts/abstracts_computerscience_CS253.txt' ,'r')
spotlight = f.read()
f.close()



spotlight = json.loads(spotlight)

spotlightKeys = spotlight.keys()

#mitosis = spotlight["bio110 DNA.txt"]


max = 0
sum = 0

text_array = []
avg_Array = []
best_twenty = []

for title in spotlight:
    print(title)
   # print (abstract)
   # print (mitosis[abstract])
    for article in spotlight:
        if article != title:
            #print('\t' +article)
           # print(spotlight[title])
           # print(spotlight[article])
           # print('--------')
            for x in spotlight[title]:
                #print(spotlight[title][x])
                f = open('./data/subtitles-V3-by-topic/Computer Science/CS253/'+article, 'r')
                text = f.read()
                f.close()
                sim = cosine_sim(spotlight[title][x], text)
                text_array.append((article, sim))

    text_array=list(set(text_array))
    text_array.sort(key=lambda x: x[1], reverse = True)

    best_twenty = text_array[:20]
    avg_Array = avg_Array + best_twenty
    print(avg_Array)
    print(len(avg_Array))
    print('-----')


for i in avg_Array:
    sum = sum + i[1]

avg = sum/len(avg_Array)

print(avg)
