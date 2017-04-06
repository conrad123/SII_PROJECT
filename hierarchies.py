import json

f = open('./outputfiles/sparql/broaders_biology_BIO110.txt','r')
obj = f.read()
f.close()
obj = json.loads(obj)

articles = list(obj.keys())
final_result = {}

for article in articles:

    print(article)
    categories = list(obj[article].keys())
    broader_article = []
    is_broader_of_article = []

    if len(categories)<2 and len(categories)>0:

        for category in categories:

            for article_comp in articles:
                if article != article_comp:
                    categories_comp = list(obj[article_comp].keys())
                    if len(categories_comp)<2 and len(categories)>0:
                        for category_comp in categories_comp:
                            broaders = obj[article_comp][category_comp][0]
                            is_broaders_of = obj[article_comp][category_comp][1]
                            if category in broaders:
                                is_broader_of_article.append(article_comp)
                            if category in is_broaders_of:
                                broader_article.append(article_comp)

        final_result[article] = {'broaders': list(set(broader_article)), 'is_broder_of': list(set(is_broader_of_article))}

print(json.dumps(final_result))