from SPARQLWrapper import SPARQLWrapper, JSON
import json

directories = ['PS001']

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

for directory in directories:

    f = open('./outputfiles/dbpedia_spotlight/top_resources_psychology_'+directory+'.txt')
    top_res = f.read()
    f.close()

    top_res = json.loads(top_res)

    final_result = {}

    for article in top_res:

        print article

        final_result[article] = {}

        if top_res[article] != []:

            treshold = int((top_res[article][0][1]+top_res[article][len(top_res[article]-1)][1])/2)

            res = [x for x in top_res[article] if x[1] >= treshold]

            for r in res:

                query = """
                        prefix ontology: <http://dbpedia.org/ontology/>
                
                        select ?abstract where {
                            <"""+r+"""> ontology:abstract ?abstract .
                            filter(langMatches(lang(?abstract),"en"))
                        }
                        """

                sparql.setQuery(query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    final_result[article][r] = result["abstract"]["value"]

            else:
                final_result[article][r] = ''

    f = open('./outputfiles/sparql/abstracts/abstracts_psychology_'+directory+'.txt','w')
    f.write(json.dumps(final_result))
    f.close()

print 'Scrittura completata'