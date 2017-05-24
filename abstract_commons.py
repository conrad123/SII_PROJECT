import json

directories = ['BIO110']

for directory in directories:

    f = open('./outputfiles/sparql/abstracts/abstracts_resources_biology_' + directory + '.txt', 'r')
    abstracts = f.read()
    f.close()
    abstracts = json.loads(abstracts)

    f = open('./outputfiles/dbpedia_spotlight/dbpedia_spotlight_biology_' + directory + '.txt', 'r')
    dbpedia = f.read()
    f.close()
    dbpedia = json.loads(dbpedia)

    result = {}

    for article in abstracts:

        print article

        abstract_resources = set(abstracts[article])

        result[article] = []

        for x in dbpedia:

            if x != article:

                article_resources = []
                for y in dbpedia[x]:
                    article_resources.append(y['URI'])

                article_resources = set(article_resources)

                intersection = abstract_resources.intersection(article_resources)

                if len(intersection) > 1:
                    result[article].append(x)

        result[article].sort(key=lambda x: x[1], reverse=True)

    print json.dumps(result)

print 'Finito'