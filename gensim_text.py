import logging, os, glob, spotlight, wikipedia, json
from collections import defaultdict
from SPARQLWrapper import SPARQLWrapper, JSON
from gensim import corpora, models, similarities

#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)




sparql = SPARQLWrapper("http://dbpedia.org/sparql")

f = open('./outputfiles/sparql/sparql_broaders/broaders_2steps_biology_BIO110.txt')
broaders = f.read()
f.close()

broaders = json.loads(broaders)

path = './data/subtitles-V3-by-topic/Biology/BIO110/'
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










stoplist = set("a	about	above	after	again	against	all	am	an	and	any	are	aren't	as	at	be	because	been	before	being	below	between	both	but	by	can't	cannot	could	couldn't	did	didn't	do	does	doesn't	doing	don't	down	during	each	few	for	from	further	had	hadn't	has	hasn't	have	haven't	having	he	he'd	he'll	he's	her	here	here's	hers	herself	him	himself	his	how	how's	i	i'd	i'll	i'm	i've	if	in	into	is	isn't	it	it's	its	itself	let's	me	more	most	mustn't	my	myself	no	nor	not	of	off	on	once	only	or	other	ought	our	ours	ourselves	out	over	own	same	shan't	she	she'd	she'll	she's	should	shouldn't	so	some	such	than	that	that's	the	their	theirs	them	themselves	then	there	there's	these	they	they'd	they'll	they're	they've	this	those	through	to	too	under	until	up	very	was	wasn't	we	we'd	we'll	we're	we've	were	weren't	what	what's	when	when's	where	where's	which	while	who	who's	whom	why	why's	with	won't	would	wouldn't	you	you'd	you'll	you're	you've	your	yours	yourself	yourselves".split('\t'))

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






f = open('./data/subtitles-V3-by-topic/Computer Science/CS046/cs046 0104 Java.txt', 'r')
text = f.read()
f.close()

annotations = spotlight.annotate('http://model.dbpedia-spotlight.org/en/annotate/', text, confidence=0.5, support=20)

dict = defaultdict(int)

for annotation in annotations:
    dict[annotation['URI']] += 1

dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)

treshold = int((dict[0][1] + dict[len(dict)-1][1])/2)

dict = [x for x in dict if x[1] >= treshold]

print '--- Risorse ---'
print dict



all_categories = []

for r in dict:

    # *********** CATEGORIE ************
    query = 'PREFIX dcterms:<http://purl.org/dc/terms/> SELECT ?cat WHERE {<' + r[0] + '> dcterms:subject ?cat .}'

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    categories = []
    for result in results["results"]["bindings"]:
        categories.append(result["cat"]["value"])

    print 'Categorie fatte'

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

        print '1step'

        # --- 2 STEPS ---
        for result in results["results"]["bindings"]:
            query = 'SELECT ?broaderConcept ?preferredLabel WHERE { <' + result["broaderConcept"][
                "value"] + '> skos:broader ?broaderConcept . ?broaderConcept skos:prefLabel ?preferredLabel .}'
            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            results_2_steps = sparql.query().convert()
            for result_2_steps in results_2_steps["results"]["bindings"]:
                broader_of_categories.append(result_2_steps["broaderConcept"]["value"])

        print 'Broader fatti'

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
            query = 'SELECT * { values ?category { <' + result["concept"][
                "value"] + '> } ?concept skos:broader ?category . }'
            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            results_2_steps = sparql.query().convert()
            for result_2_steps in results_2_steps["results"]["bindings"]:
                isbroaderof_of_categories.append(result_2_steps["concept"]["value"])

        print 'is broader of fatti'

    all_categories += categories + broader_of_categories + isbroaderof_of_categories

all_categories = set(all_categories)





abstracts = []

for r in dict:

    try:
        page = wikipedia.page(r[0][28:])
    except:
        page = None

    abstracts.append((r[0], page.summary))

'''dict = defaultdict(int)'''

print '--- Abstarct ---'
print abstracts






semantic_avgs = {}

for a in abstracts:

    dict = defaultdict(int)
    query = ''
    annotations = spotlight.annotate('http://model.dbpedia-spotlight.org/en/annotate/', a[1], confidence=0.5, support=20)

    for annotation in annotations:
        dict[annotation['URI'][28:].replace('_', ' ')] += 1

    dict = sorted(dict.items(), key=lambda x: -x[1])

    treshold = int((dict[0][1]+dict[len(dict)-1][1])/2)

    dict = [x for x in dict if x[1] >= treshold]

    for r in dict:
        query += r[0]+' '

    terms = query.lower().split()

    print terms

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

for article in semantic_avgs:

    semantic_avgs[article] = sum(semantic_avgs[article])/len(semantic_avgs[article])

semantic_avgs = sorted(semantic_avgs.items(), key=lambda x: -x[1])



for x in semantic_avgs:

    cat = broaders[x[0]]

    for k in cat:
        if (len(all_categories.intersection(set(k)))>0) or (len(all_categories.intersection(set(cat[k][0]+cat[k][1])))>0):
            print x