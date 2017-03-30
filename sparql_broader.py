from SPARQLWrapper import SPARQLWrapper, JSON
import os, glob, json

final_result =  []

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

query = 'PREFIX cat: <http://dbpedia.org/resource/Category:> SELECT ?broaderConcept ?preferredLabel WHERE {cat:20th-century_American_male_actors skos:broader ?broaderConcept . ?broaderConcept skos:prefLabel ?preferredLabel .}'

sparql.setQuery(query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result["broaderConcept"]["value"])

print('FINE DEI SKOS:BROADER\nINIZIO DEI IS SKOS:BROADER OF')

query = 'PREFIX cat: <http://dbpedia.org/resource/Category:> SELECT * { values ?category { <cat:20th-century_American_male_actors> } ?concept skos:broader ?category . }'

sparql.setQuery(query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result["category"]["value"])