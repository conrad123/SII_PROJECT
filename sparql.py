from SPARQLWrapper import SPARQLWrapper, JSON
import os, glob, json

f = open('./outputfiles/dbpedia_spotlight/dbpedia_spotlight_biology_BIO110.txt','r')
map = f.read()
f.close()

map = json.loads(map)

os.chdir('./data/subtitles-V3-by-topic/Biology/BIO110')
titoli = []

for file in glob.glob('*.txt'):
    titoli.append(file)

for titolo in titoli:
    objs = map[titolo]
    uris = []
    for obj in objs:
        uris.append(obj['URI'])

    set_uris = list(set(uris))

    counts = []
    for set_uri in set_uris:
        counts.append((set_uri,uris.count(set_uri)))

    counts = sorted(counts, key=lambda x: x[1], reverse=True)

    i = 0
    while i<len(counts):
        counts[i] = list(counts[i])
        counts[i][0] = '<'+counts[i][0]+'> dcterms:subject ?cat .'
        counts[i] = tuple(counts[i])
        i = i+1

    final_result = []
    i = 0
    while i<len(counts):

        sparql = SPARQLWrapper("http://dbpedia.org/sparql")

        query = "PREFIX dcterms:<http://purl.org/dc/terms/> SELECT ?cat WHERE {"+counts[i][0]+"}"

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        for result in results["results"]["bindings"]:
            final_result.append(result["cat"]["value"])

        i = i+1

    set_final_result = list(set(final_result))

    category_counts = []
    for elem in set_final_result:
        category_counts.append((elem, final_result.count(elem)))

    max_count = max(category_counts, key=lambda x: x[1])[1]

    file_category = []
    for cat in category_counts:
        if cat[1] == max_count:
            file_category.append(cat[0])

    print(titolo)
    print('max'+str(max_count))
    print(file_category)