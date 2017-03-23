from SPARQLWrapper import SPARQLWrapper, JSON
import os, glob, json

directories = ['DESIGN101','UD509']

for dir in directories:

    path = './outputfiles/dbpedia_spotlight/dbpedia_spotlight_design_'+dir+'.txt'
    f = open(path,'r')
    map = f.read()
    f.close()

    map = json.loads(map)

    path = './data/subtitles-V3-by-topic/Design/'+dir
    os.chdir(path)
    titoli = []

    for file in glob.glob('*.txt'):
        titoli.append(file)

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

            sparql = SPARQLWrapper("http://dbpedia.org/sparql")

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

    os.chdir('../../../../outputfiles')
    f = open('sparql/categories_design_'+dir+'.txt','w')
    f.write(json.dumps(map_out))
    f.close()
    os.chdir('../')

    print('Scrittura completata')