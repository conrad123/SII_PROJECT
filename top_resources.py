from collections import defaultdict
import json

directories = ['BIO110']

for directory in directories:

    f = open('./outputfiles/dbpedia_spotlight/dbpedia_spotlight_biology_'+directory+'.txt','r')
    spotlight = f.read()
    f.close()

    spotlight = json.loads(spotlight)

    final_result = {}

    for article in spotlight:

        print article

        resources = []
        for obj in spotlight[article]:
            resources.append(obj['URI'])

        d = defaultdict(int)
        for resource in resources:
            d[resource] += 1

        top_resources = sorted(d.items(), key=lambda x: x[1], reverse=True)

        final_result[article] = top_resources

    f = open('./outputfiles/dbpedia_spotlight/top_resources_biology_'+directory+'.txt','w')
    f.write(json.dumps(final_result))
    f.close()

print 'Scrittura completata'