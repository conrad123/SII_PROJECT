import json

directories = ['BIO110']
for directory in directories:
    f = open('./outputfiles/normalization/normalization_commoncat/normalization_commoncat_biology_'+directory+'.txt','r')
    commoncat = f.read()
    f.close()
    commoncat = json.loads(commoncat)

    f = open('./outputfiles/normalization/normalization_commonres/normalization_commonres_biology_'+directory+'.txt','r')
    commonres = f.read()
    f.close()
    commonres = json.loads(commonres)

    f = open('./outputfiles/normalization/normalization_dbpediaspotlight/normalization_dbpediaspotlight_biology_'+directory+'.txt','r')
    dbpediaspotlight = f.read()
    f.close()
    dbpediaspotlight = json.loads(dbpediaspotlight)

    f = open('./outputfiles/normalization/normalization_postagging/normalization_postagging_biology_'+directory+'.txt','r')
    postagging = f.read()
    f.close()
    postagging = json.loads(postagging)

    f = open('./outputfiles/normalization/normalization_postagging/normalization_postagging_intersection/normalization_postagging_intersection_biology_'+directory+'.txt','r')
    postagging_intersection = f.read()
    f.close()
    postagging_intersection = json.loads(postagging_intersection)

    f = open('./outputfiles/normalization/normalization_postagging/normalization_postagging_union/normalization_postagging_union_biology_'+directory+'.txt','r')
    postagging_union = f.read()
    f.close()
    postagging_union = json.loads(postagging_union)

    for chiave in list(commoncat.keys()):
        if(not (chiave in list(commonres.keys()))):
            print chiave

    print(len(list(commoncat.keys())))
    print(len(list(commonres.keys())))
    print(len(list(dbpediaspotlight.keys())))
    print(len(list(postagging.keys())))
    print(len(list(postagging_intersection.keys())))
    print(len(list(postagging_union.keys())))


    keys = list(commoncat.keys())
    final_vectors = {}
    for key in keys:
        val_commoncat = commoncat[key]
        val_commonres = commonres[key]
        val_dbpediaspotlight = dbpediaspotlight[key]
        val_postagging = postagging[key]
        val_postagging_intersection = postagging_intersection[key]
        try:
            val_postagging_union = postagging_union[key]
        except:
            val_postagging_union = {}
        feature_vector = []
        feature_vector.append(val_commoncat['common_cat'])
        feature_vector.append(val_commonres['common_res'])
        feature_vector.append(val_dbpediaspotlight['resources'])
        feature_vector.append(val_postagging['NN'])
        feature_vector.append(val_postagging['Terms'])
        feature_vector.append(val_postagging_intersection['nn_tot'])
        try:
            feature_vector.append(val_postagging_union['nn_tot'])
        except:
            feature_vector.append(0.0)
        final_vectors[key] = feature_vector

    print json.dumps(final_vectors)




