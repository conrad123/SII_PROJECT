from SPARQLWrapper import SPARQLWrapper, JSON
import json

directories = ['PS001']
sparql = SPARQLWrapper("http://dbpedia.org/sparql")

for directory in directories:

    final_result = {}

    f = open('./outputfiles/sparql/categories_psychology_'+directory+'.txt','r')
    obj = f.read()
    f.close()

    obj = json.loads(obj)

    articles = list(obj.keys())

    for article in articles:

        print(article)
        categories_of_article = obj[article]
        final_result[article] = {}

        if isinstance(categories_of_article[0],unicode):
            categories_of_article[0] = [categories_of_article[0]]

        for category in categories_of_article[0]:

            broader_of_article = []
            isbroaderof_of_article = []

            query = 'SELECT ?broaderConcept ?preferredLabel WHERE { <'+category+'> skos:broader ?broaderConcept . ?broaderConcept skos:prefLabel ?preferredLabel .}'

            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()

            #print category

            #print '*********** BROADER ************'
            #print '--- 1 STEP ---'
            for result in results["results"]["bindings"]:
                broader_of_article.append(result['broaderConcept']['value'])
                #print result['broaderConcept']['value']

            #print '2 STEPS'
            for result in results["results"]["bindings"]:
                query = 'SELECT ?broaderConcept ?preferredLabel WHERE { <' + result["broaderConcept"]["value"] + '> skos:broader ?broaderConcept . ?broaderConcept skos:prefLabel ?preferredLabel .}'
                sparql.setQuery(query)
                sparql.setReturnFormat(JSON)
                results_2_steps = sparql.query().convert()
                for result_2_steps in results_2_steps["results"]["bindings"]:
                    broader_of_article.append(result_2_steps["broaderConcept"]["value"])
                    #print result_2_steps["broaderConcept"]["value"]



            query = 'SELECT *  { values ?category { <'+category+'> } ?concept skos:broader ?category . }'

            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()

            #print '************* IS BROADER OF **************'
            #print '--- 1 STEP ---'
            for result in results["results"]["bindings"]:
                isbroaderof_of_article.append(result['concept']['value'])
                #print result['concept']['value']

            #print '--- 2 STEPS ---'
            for result in results["results"]["bindings"]:
                query = 'SELECT *  { values ?category { <' + result["concept"]["value"] + '> } ?concept skos:broader ?category . }'
                sparql.setQuery(query)
                sparql.setReturnFormat(JSON)
                results_2_steps = sparql.query().convert()
                for result_2_steps in results_2_steps["results"]["bindings"]:
                    isbroaderof_of_article.append(result_2_steps["concept"]["value"])
                    #print result_2_steps["concept"]["value"]

            final_result[article][category] = (broader_of_article, isbroaderof_of_article)

    f = open('./outputfiles/sparql/sparql_broaders/broaders_2steps_psychology_'+directory+'.txt','w')
    f.write(json.dumps(final_result))
    f.close()

    print('Scrittura completata')