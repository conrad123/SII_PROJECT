from collections import defaultdict
from SPARQLWrapper import SPARQLWrapper, JSON
from sklearn.feature_extraction.text import TfidfVectorizer
import spotlight, nltk, string, glob, os


sparql = SPARQLWrapper("http://dbpedia.org/sparql")


# COSENO SIMILARITA' ------------------------------------------------------------------------------------------------
stem = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)


def stem_tokens(tokens):
    return [stem.stem(item) for item in tokens]


#si applica lo stemming, il lowercase e la rimozione della punteggiatura
def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))


vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')


#coseno similarita' tra due testi
def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]


# PREREQUISITI ------------------------------------------------------------------------------------------------------
#verifica se il testo1 e' prerequisito del testo2
def prerequisite(text1, text2):

    try:
        #si annotano tutte le risorse dbpedia presenti nel testo2
        print('Ottenimento risorse del testo principale')
        annotations = spotlight.annotate('http://model.dbpedia-spotlight.org/en/annotate/', text2, confidence=0.5, support=20)

        #si contano le occorrenze delle risorse dbpedia nel testo2
        dict = defaultdict(int)

        for annotation in annotations:
            dict[annotation['URI']] += 1

        dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)

        #si mantengono solo le risorse che hanno un'occorrenza uguale o superiore alla media tra massima e minima occorrenza
        treshold = int((dict[0][1] + dict[len(dict)-1][1])/2)

        dict = [x for x in dict if x[1]>=treshold]

        #per ogni risorsa rimasta si collezionano gli abstract presenti in dbpedia
        print('Ottenimento degli abstract delle risorse principali')
        abstracts = []

        for r in dict:
            query = """prefix ontology: <http://dbpedia.org/ontology/>
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

        # si calcola la coseno similarita' tra gli abstract e il testo1 e si filtrano solo le risorse associate a similarita' superiore a 0.1
        print('Calcolo delle coseno similarita tra gli abstract e il testo da verificare')
        prereq_candidates = []
        for abstract in abstracts:
            similarity = cosine_sim(text1, abstract[1])
            if (similarity>0.1):
                prereq_candidates.append((abstract[0], similarity))

        # se ci sono risorse candidate, si prende quella con similarita' maggiore
        # prima di confermare la presenza di prerequisito si verifica prima se esiste almeno un'intersezione tra i campi semantici della risorsa e del testo1
        # per campi semantici si intendono le categorie e i 'broader' e gli 'is broader of' a due livelli di esse
        if prereq_candidates != []:
            prereq = max(prereq_candidates, key=lambda x: x[1])
            #print (prereq)
            print('Ottenimento dei campi semantici del testo principale')
            sem_fields = set(semantic_fields(prereq[0]))
            print('Ottenimento dei campi semantici del testo da verificare')
            cat = categories(text1)
            #print(len(cat))
            print (list(sem_fields.intersection(cat)))
            if len(list(sem_fields.intersection(cat)))>0:
                print(prereq)
                return "Relazione di prerequisito"
    except:

        return "No resources"


# CATEGORIE ---------------------------------------------------------------------------------------------------------
# si estraggono i campi semantici da un testo
def categories(text):

    annotations = spotlight.annotate('http://model.dbpedia-spotlight.org/en/annotate/', text, confidence=0.5, support=20)

    dict = defaultdict(int)

    for annotation in annotations:
        dict[annotation['URI']] += 1

    dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)

    max = dict[0][1]
    dict = [x for x in dict if x[1]==max]

    sem_fields = []

    for d in dict:
        sem_fields = sem_fields + semantic_fields(d[0])

    return set(sem_fields)


# CAMPI SEMANTICI ---------------------------------------------------------------------------------------------------
# si estraggono i campi semtnatici da una risorsa dbpedia
def semantic_fields(resource):

    # *********** CATEGORIE ************
    query = 'PREFIX dcterms:<http://purl.org/dc/terms/> SELECT ?cat WHERE {<'+resource+'> dcterms:subject ?cat .}'

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    fields = []
    for result in results["results"]["bindings"]:
        fields.append(result["cat"]["value"])

    broader_of_categories = []
    isbroaderof_of_categories = []

    for category in fields:

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

    fields = fields + broader_of_categories + isbroaderof_of_categories

    return fields


# MAIN --------------------------------------------------------------------------------------------------------------
path = './data/subtitles-V3-by-topic/Biology/BIO110/'
os.chdir(path)

text2 = "As long as the cell doubles its DNA before dividing, then each daughter cell will have the same amount of DNA information as the parent cell did. >> Sounds like a pretty important step, that all the genetic information stays intact for every division. >> Exactly. We call this kind of division, mitosis. Mitosis is a kind of division where the same amount of information is maintained over many cell divisions. So it's important to keep two copies of the chromosome in every cell. >> Right. This is how a heterozygous cell, where one copy of the chromosome has one allele and the other copy of the chromosome has another allele, when they divide and have daughter cells, both the daughter cells will also be heterozygous. "
files = len(glob.glob('*.txt'))
cont = 1
prerequisites = []

for file in glob.glob('*.txt'):

    if file != 'bio110 Mitosis.txt':
        print('--- '+file+' ('+str(cont)+'/'+str(files)+') ---')
        f = open(file, 'r')
        text1 = f.read()
        f.close()

        response = prerequisite(text1, text2)

        if response=='Relazione di prerequisito':
            prerequisites.append(file)

    cont += 1

print('*** Prerequisiti individuati ***')
print(prerequisites)