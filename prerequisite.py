from collections import defaultdict
from SPARQLWrapper import SPARQLWrapper, JSON
from sklearn.feature_extraction.text import TfidfVectorizer
import spotlight, nltk, string

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

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

def prerequisite(text1, text2):
    try:
        annotations = spotlight.annotate('http://model.dbpedia-spotlight.org/en/annotate/', text2, confidence=0.5, support=20)

        dict = defaultdict(int)

        for annotation in annotations:
            dict[annotation['URI']] += 1

        dict = sorted(dict.items(),key=lambda x: x[1], reverse = True)

        treshold = int((dict[0][1] + dict[len(dict)-1][1])/2)

        dict = [x for x in dict if x[1]>=treshold]

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

        prereq_candidates = []
        for abstract in abstracts:
            similarity = cosine_sim(text1, abstract[1])
            if (similarity>0.1):
                prereq_candidates.append((abstract[0], similarity))

        if prereq_candidates != []:
            prereq = max(prereq_candidates, key=lambda x: x[1])
            sem_fields = set(semantic_fields(prereq[0]))
            cat = set(categories(text1))
            print(sem_fields)
            print(len(sem_fields))
            print ("-----")
            print (cat)
            print(len(cat))
            if len(list(sem_fields.intersection(cat))) > 0:
                print(prereq)
    except:
        print("No resources")









def categories(text):

    annotations = spotlight.annotate('http://model.dbpedia-spotlight.org/en/annotate/', text, confidence=0.5, support=20)

    for annotation in annotations:
        query = 'PREFIX dcterms:<http://purl.org/dc/terms/> SELECT ?cat WHERE {<' + annotation['URI'] + '> dcterms:subject ?cat .}'

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        categories = []
        for result in results["results"]["bindings"]:
            categories.append(result["cat"]["value"])

        dict = defaultdict(int)

        for category in categories:
            dict[category] += 1

        dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)

        max = dict[0][1]
        dict = [x for x in dict if x[1]==max]

        categories = []
        for d in dict:
            categories.append(d[0])

        return categories










def semantic_fields(resource):

    query = 'PREFIX dcterms:<http://purl.org/dc/terms/> SELECT ?cat WHERE {<'+resource+'> dcterms:subject ?cat .}'

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    fields = []
    for result in results["results"]["bindings"]:
        fields.append(result["cat"]["value"])

    broader_of_category = []
    isbroaderof_of_category = []

    for category in fields:

        query = 'SELECT ?broaderConcept ?preferredLabel WHERE { <' + category + '> skos:broader ?broaderConcept . ?broaderConcept skos:prefLabel ?preferredLabel .}'

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        # print category

        # print '*********** BROADER ************'
        # print '--- 1 STEP ---'
        for result in results["results"]["bindings"]:
            broader_of_category.append(result['broaderConcept']['value'])
            # print result['broaderConcept']['value']

        # print '2 STEPS'
        for result in results["results"]["bindings"]:
            query = 'SELECT ?broaderConcept ?preferredLabel WHERE { <' + result["broaderConcept"]["value"] + '> skos:broader ?broaderConcept . ?broaderConcept skos:prefLabel ?preferredLabel .}'
            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            results_2_steps = sparql.query().convert()
            for result_2_steps in results_2_steps["results"]["bindings"]:
                broader_of_category.append(result_2_steps["broaderConcept"]["value"])
                # print result_2_steps["broaderConcept"]["value"]


        query = 'SELECT *  { values ?category { <' + category + '> } ?concept skos:broader ?category . }'

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        # print '************* IS BROADER OF **************'
        # print '--- 1 STEP ---'
        for result in results["results"]["bindings"]:
            isbroaderof_of_category.append(result['concept']['value'])
            # print result['concept']['value']

        # print '--- 2 STEPS ---'
        for result in results["results"]["bindings"]:
            query = 'SELECT *  { values ?category { <' + result["concept"]["value"] + '> } ?concept skos:broader ?category . }'
            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            results_2_steps = sparql.query().convert()
            for result_2_steps in results_2_steps["results"]["bindings"]:
                isbroaderof_of_category.append(result_2_steps["concept"]["value"])
                # print result_2_steps["concept"]["value"]

    fields = fields + broader_of_category + isbroaderof_of_category
    return fields







b = "To declare an array of strings with space for ten values, we would make the variable, and give it a type of string array, and an initial value of a new string array with space for ten items. To declare an array of strings that contains two values, yes and no, we'll use the curly brace notation. The type is the same as before, but now we put the strings, yes and no, in the curly braces separated by commas. "
a = "Now you've done a lot of work with numbers and most people think that numbers are what computers are really good at. But truth be told many programmers work more with text than numbers. In Java the technical term for text is a string. Why a string? You can think of text being a sequence of individual letters that are strung together. You have already seen strings. In Java, their enclosed in quotes and there's some text inside. You've seen string variables, here is one, it's called name and it's type is string. You've seen a bunch of string methods and here are a few more. In the interest of learn by doing, go ahead, fire up BlueJ. And tell me what happens when you call each of these methods, or in the last case, when you execute this piece of code. "
prerequisite(a, b)