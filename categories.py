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

f = open('./outputfiles/sparql/categories_biology_BIO110.txt','r')
obj = f.read()
f.close()
obj = json.loads(obj)

articles = list(obj.keys())
one_category_articles = []
more_category_articles = []

for article in articles:
    if len(obj[article][0]) == 1:
        one_category_articles.append(article)
    else:
        more_category_articles.append(article)

for more_category_article in more_category_articles:

    print(more_category_article)
    text_sims = []
    f = open('./data/subtitles-V3-by-topic/Biology/BIO110/'+more_category_article,'r')
    text = f.read()
    f.close()

    for one_category_article in one_category_articles:
        f = open('./data/subtitles-V3-by-topic/Biology/BIO110/'+one_category_article,'r')
        text_comp = f.read()
        f.close()
        text_sims.append((one_category_article,cosine_sim(text,text_comp)))

    max_sim = max(text_sims, key=lambda x: x[1])

    for text_sim in text_sims:
        if max_sim[1] == text_sim[1]:
            category = obj[text_sim[0]][0][0]
            obj[more_category_article][0] = [category]

f = open('./outputfiles/sparql/categories_biology_BIO110.txt','w')
f.write(json.dumps(obj))
f.close()

print('Scrittura completata')