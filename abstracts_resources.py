import spotlight, json

directories = ['BIO110']

for directory in directories:

    f = open('./outputfiles/sparql/abstracts/abstracts_biology_' + directory + '.txt', 'r')
    abstracts = f.read()
    f.close()
    abstracts = json.loads(abstracts)

    result = {}

    for article in abstracts:

        print article

        print abstracts[article]

        annotations = spotlight.annotate('http://model.dbpedia-spotlight.org/en/annotate/',abstracts[article],confidence=0.5,support=20)

        resources = []

        for annotation in annotations:
            resources.append(annotation['URI'])

        result[article] = resources

    f = open('./outputfiles/sparql/abstracts/abstracts_resources_biology_' + directory + '.txt', 'w')
    f.write(json.dumps(result))
    f.close()

print 'Scrittura completata'