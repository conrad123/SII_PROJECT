from SPARQLWrapper import SPARQLWrapper, JSON
import json

directories = ['BIO110']
sparql = SPARQLWrapper("http://dbpedia.org/sparql")

for dir in directories:

    path = './outputfiles/dbpedia_spotlight/dbpedia_spotlight_biology_'+dir+'.txt'
    f = open(path,'r')
    map = f.read()
    f.close()

    map = json.loads(map)

    titoli = list(map.keys())

    map_out = {}

    for titolo in titoli:

        objs = map[titolo]
        uris = []

        for obj in objs:
            uris.append(obj['URI'])

        uris = list(set(uris))

        i = 0
        while i<len(uris):
            uris[i] = '<'+uris[i]+'> dcterms:subject ?cat .'
            i = i+1

        final_result = []
        i = 0

        while i<len(uris):

            query = "PREFIX dcterms:<http://purl.org/dc/terms/> SELECT ?cat WHERE {"+uris[i]+"}"

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

        try:
            max_count = max(category_counts, key=lambda x: x[1])[1]
        except:
            max_count = 0

        file_category = []
        for cat in category_counts:
            if cat[1] == max_count:
                file_category.append(cat[0])

        print(titolo)
        map_out[titolo] = (file_category,max_count)

    f = open('./outputfiles/sparql/categories_biology_'+dir+'.txt','w')
    f.write(json.dumps(map_out))
    f.close()

    print('Scrittura completata')