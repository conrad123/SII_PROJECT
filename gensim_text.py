import logging, os, glob, spotlight
from collections import defaultdict
from SPARQLWrapper import SPARQLWrapper, JSON
from gensim import corpora, models, similarities

#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

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

f = open('./data/subtitles-V3-by-topic/Biology/BIO110/bio110 Mitosis.txt', 'r')
text = f.read()
f.close()

annotations = spotlight.annotate('http://model.dbpedia-spotlight.org/en/annotate/', text, confidence=0.5, support=20)

dict = defaultdict(int)

#--------------------------------------------------------------------------------------------------------------------
#CONFRONTARE LE RISORSE DEL TESTO IN ANALISI CON IL CORPUS
'''
for annotation in annotations:
    dict[annotation['URI'][28:].replace('_',' ')] += 1
'''

#--------------------------------------------------------------------------------------------------------------------
#CONFRONTARE LE RISORSE DEGLI ABSTRACT DEL TESTO IN ANALISI CON IL CORPUS
for annotation in annotations:
    dict[annotation['URI']] += 1

dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)

treshold = int((dict[0][1] + dict[len(dict)-1][1])/2)

dict = [x for x in dict if x[1] >= treshold]

abstracts = []

for r in dict:
    query = """
               prefix ontology: <http://dbpedia.org/ontology/>
               select ?abstract where {
                  <""" + r[0] + """> ontology:abstract ?abstract .
                  filter(langMatches(lang(?abstract),"en"))
               }
            """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        abstracts.append((r[0], result["abstract"]["value"]))

dict = defaultdict(int)

for a in abstracts:
    annotations = spotlight.annotate('http://model.dbpedia-spotlight.org/en/annotate/', a[1], confidence=0.5, support=20)
    for annotation in annotations:
        dict[annotation['URI'][28:].replace('_', ' ')] += 1

#--------------------------------------------------------------------------------------------------------------------

query = ''

for d in dict:
    query += d[0]+' '

vec_bow = dictionary.doc2bow(query.lower().split())
vec_lsi = lsi[vec_bow]

index = similarities.MatrixSimilarity(lsi[corpus])
index.save('./outputfiles/dictionary/redirect.index')

if os.path.exists("./outputfiles/dictionary/redirect.index"):
    index = similarities.MatrixSimilarity.load('./outputfiles/dictionary/redirect.index')

sims = index[vec_lsi]

sims = sorted(enumerate(sims), key=lambda item: -item[1])

for s in sims:
    print files_name[s[0]]+' --> '+str(s[1])