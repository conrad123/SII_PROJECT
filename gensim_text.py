import os, sys, glob, spotlight, wikipedia, json, nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
from SPARQLWrapper import SPARQLWrapper, JSON
from gensim import corpora, models, similarities


# COSENO SIMILARITA' ------------------------------------------------------------------------------------------------
stem = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def stem_tokens(tokens):
    return [stem.stem(item) for item in tokens]

# si applica lo stemming, il lowercase e la rimozione della punteggiatura
def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

# coseno similarita' tra due testi
def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]

# wrapper per sparql
sparql = SPARQLWrapper("http://dbpedia.org/sparql")

f = open(sys.argv[1])
broaders = f.read()
f.close()
broaders = json.loads(broaders)


# collezionamento di tutti i testi del corpus
path = sys.argv[2]
os.chdir(path)
documents = []
files_name = []

for file in glob.glob('*.txt'):
    files_name.append(file)
    f = open(file, 'r')
    text = f.read()
    f.close()
    documents.append(text)

os.chdir('../../../../')


# addestramento di gensim
stoplist = set("for a of the and to in".split())

texts = [[word for word in document.lower().split() if word not in stoplist]for document in documents]

frequency = defaultdict(int)

for text in texts:
    for token in text:
        frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1] for text in texts]

dictionary = corpora.Dictionary(texts)

dictionary.save('./outputfiles/dictionary/redirect.dict')

corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('./outputfiles/dictionary/redirect.mm', corpus)

if (os.path.exists("./outputfiles/dictionary/redirect.dict") and os.path.exists("./outputfiles/dictionary/redirect.mm")):
    dictionary = corpora.Dictionary.load("./outputfiles/dictionary/redirect.dict")
    corpus = corpora.MmCorpus("./outputfiles/dictionary/redirect.mm")

tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=300)
corpus_lsi = lsi[corpus_tfidf]

lsi.save('./outputfiles/dictionary/redirect.lsi')

if os.path.exists("./outpufiles/dictionary/redirect.lsi"):
    lsi = models.LsiModel.load('./outputfiles/dictionary/redirect.lsi')

lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=300)


# analisi del testo da verificare
f = open(sys.argv[3], 'r')
text = f.read()
f.close()

# reperimento risorse da dbpedia
annotations = spotlight.annotate('http://model.dbpedia-spotlight.org/en/annotate/', text, confidence=0.5, support=20)

dict = defaultdict(int)

for annotation in annotations:
    dict[annotation['URI']] += 1

dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)

treshold = int((dict[0][1] + dict[len(dict)-1][1])/2)

# selezione delle risorse più occorrenti
dict = [x for x in dict if x[1] >= treshold]


# reperimento delle categorie a 2 step del testo da verificare
all_categories = []

for r in dict:

    # *********** CATEGORIES ************
    query = 'PREFIX dcterms:<http://purl.org/dc/terms/> SELECT ?cat WHERE {<' + r[0] + '> dcterms:subject ?cat .}'

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    categories = []
    for result in results["results"]["bindings"]:
        categories.append(result["cat"]["value"])


    broader_of_categories = []
    isbroaderof_of_categories = []

    for category in categories:

        # *********** BROADER ************
        query = 'SELECT ?broaderConcept ?preferredLabel WHERE { <' + category + '> skos:broader ?broaderConcept . ?broaderConcept skos:prefLabel ?preferredLabel .}'

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        # --- 1 STEP ---
        for result in results["results"]["bindings"]:
            broader_of_categories.append(result['broaderConcept']['value'])

        # --- 2 STEPS ---
        for result in results["results"]["bindings"]:
            query = 'SELECT ?broaderConcept ?preferredLabel WHERE { <' + result["broaderConcept"]["value"] + '> skos:broader ?broaderConcept . ?broaderConcept skos:prefLabel ?preferredLabel .}'
            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            results_2_steps = sparql.query().convert()
            for result_2_steps in results_2_steps["results"]["bindings"]:
                broader_of_categories.append(result_2_steps["broaderConcept"]["value"])


        # print '************* IS BROADER OF **************'
        query = 'SELECT * { values ?category { <' + category + '> } ?concept skos:broader ?category . }'

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        # --- 1 STEP ---
        for result in results["results"]["bindings"]:
            isbroaderof_of_categories.append(result['concept']['value'])

        # --- 2 STEPS ---
        for result in results["results"]["bindings"]:
            query = 'SELECT * { values ?category { <' + result["concept"]["value"] + '> } ?concept skos:broader ?category . }'
            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            results_2_steps = sparql.query().convert()
            for result_2_steps in results_2_steps["results"]["bindings"]:
                isbroaderof_of_categories.append(result_2_steps["concept"]["value"])

    all_categories += categories + broader_of_categories + isbroaderof_of_categories

all_categories = set(all_categories)


# reperimento degli abstract di wikipedia delle risorse principali del testo da verificare
abstracts = []

for r in dict:

    try:
        page = wikipedia.page(r[0][28:])
    except:
        page = None

    abstracts.append((r[0], page.summary))


# similiratia' semantica tra gli abstract e i testi del corpus
semantic_avgs = {}

for a in abstracts:

    query = a[1]
    terms = list(set(query.lower().split()))

    vec_bow = dictionary.doc2bow(terms)
    vec_lsi = lsi[vec_bow]

    index = similarities.MatrixSimilarity(lsi[corpus])
    index.save('./outputfiles/dictionary/redirect.index')

    if os.path.exists("./outputfiles/dictionary/redirect.index"):
        index = similarities.MatrixSimilarity.load('./outputfiles/dictionary/redirect.index')

    sims = index[vec_lsi]

    sims = sorted(enumerate(sims), key=lambda item: -item[1])

    for s in sims:
        if files_name[s[0]] in semantic_avgs:
            semantic_avgs[files_name[s[0]]].append(s[1])
        else:
            semantic_avgs[files_name[s[0]]] = [s[1]]

# similarita' semantica media per ogni testo del corpus
for article in semantic_avgs:

    semantic_avgs[article] = sum(semantic_avgs[article])/len(semantic_avgs[article])

semantic_avgs = sorted(semantic_avgs.items(), key=lambda x: -x[1])


# generamento dell'output
final_result = []
for x in semantic_avgs:

    cat = broaders[x[0]]

    for k in cat:

        # verifica di intersezione tra le categorie a 2 step del testo da verificare e del corpus
        if (len(all_categories.intersection(set(k)))>0) or (len(all_categories.intersection(set(cat[k][0]+cat[k][1])))>0):

            f = open(sys.argv[2]+x[0], 'r')
            text = f.read()
            f.close()

            # similarita' sintattica tra gli abstract e i testi del corpus
            cos_sims = []
            for a in abstracts:
                cos_sims.append(cosine_sim(text, a[1]))

            max_cos_sim = max(cos_sims)
            min_cos_sim = min(cos_sims)

            # eliminazione dei falsi positivi di gensim
            if max_cos_sim >= 0.1:
                final_result.append((x[0], x[1]+max_cos_sim-min_cos_sim))
            else:
                final_result.append((x[0], 0))

final_result.sort(key=lambda x: -x[1])

for x in final_result:
    if x[1] != 0:
        print x