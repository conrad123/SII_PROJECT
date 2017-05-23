from sematch.semantic.similarity import EntitySimilarity
import json

sim = EntitySimilarity()

print sim.similarity('http://dbpedia.org/resource/Stop_codon','http://dbpedia.org/resource/Protein')

'''
directories = ['BIO110']

for directory in directories:

    f = open('./outputfiles/dbpedia_spotlight/dbpedia_spotlight_biology_'+directory+'.txt','r')
    dbpedia = f.read()
    f.close()

    f = open('./outputfiles/hierarchies/hierarchies_biology_'+directory+'.txt','r')
    hierarchies = f.read()
    f.close()

    hierarchies = json.loads(hierarchies)

    dbpedia = json.loads(dbpedia)

    result = {}

    for article in hierarchies:

        print article

        result[article] = {'broaders': [], 'is_broader_of': []}

        if article in dbpedia:
            res_article_tmp = dbpedia[article] #array di dizionari
            res_article = []

        for x in res_article_tmp:
            res_article.append(x['URI'])

        res_article = list(set(res_article))

        for broader in hierarchies[article]['broaders']:

            res_broader_tmp = dbpedia[broader] #array di dizionari
            res_broader = []

            for x in res_broader_tmp:
                res_broader.append(x['URI'])

            res_broader = list(set(res_broader))

            sum = 0
            for x in res_article:
                max = 0
                cont = 0
                for y in res_broader:
                    if x != y:
                        cont += 1
                        print cont
                        print x
                        print y
                        rel = sim.relatedness(x,y)
                        if rel > max:
                            max = rel
                sum += max

            result[article]['broaders'].append((broader,(sum/len(res_article))))

print str(result)
'''