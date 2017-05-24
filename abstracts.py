from SPARQLWrapper import SPARQLWrapper, JSON
import json

directories = ['BIO110']

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

for directory in directories:

    f = open('./outputfiles/dbpedia_spotlight/top_resources_biology_'+directory+'.txt')
    top_res = f.read()
    f.close()

    top_res = json.loads(top_res)

    final_result = {}

    for article in top_res:

        print article

        if top_res[article] != []:
            res = top_res[article][0][0]

        query = """
                prefix dbpedia-owl: <http://dbpedia.org/ontology/>
        
                select ?abstract where {
                    <"""+res+"""> dbpedia-owl:abstract ?abstract .
                    filter(langMatches(lang(?abstract),"en"))
                }
                """

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        for result in results["results"]["bindings"]:
            final_result[article] = result["abstract"]["value"]

    f = open('./outputfiles/sparql/abstracts/abstracts_biology_'+directory+'.txt','w')
    f.write(json.dumps(final_result))
    f.close()

print 'Scrittura completata'