from SPARQLWrapper import SPARQLWrapper, JSON
import json

directories = ['BIO110']
sparql = SPARQLWrapper("http://dbpedia.org/sparql")

final_result =  {}

for directory in directories:

    f = open('./outputfiles/sparql/categories_biology_'+directory+'.txt','r')
    obj = f.read()
    f.close()

    obj = json.loads(obj)

    articles = list(obj.keys())

    for article in articles:

        print(article)
        categories_of_article = obj[article]
        final_result[article] = {}

        for category in categories_of_article[0]:

            broader_of_article = []
            isbroaderof_of_article = []

            query = 'SELECT ?broaderConcept ?preferredLabel WHERE { <'+category+'> skos:broader ?broaderConcept . ?broaderConcept skos:prefLabel ?preferredLabel .}'

            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()

            for result in results["results"]["bindings"]:
                broader_of_article.append(result['broaderConcept']['value'])

            query = 'SELECT *  { values ?category { <'+category+'> } ?concept skos:broader ?category . }'

            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()


            for result in results["results"]["bindings"]:
                isbroaderof_of_article.append(result['concept']['value'])

            final_result[article][category] = (broader_of_article, isbroaderof_of_article)

    f = open('./outputfiles/sparql/broaders_biology_'+directory+'.txt','w')
    f.write(json.dumps(final_result))
    f.close()

    print('Scrittura completata')