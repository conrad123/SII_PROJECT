import json

directories = ['BIO110']

for directory in directories:

    f = open('./outputfiles/pos_tagging/pos_tagging_biology_' + directory + '.txt', 'r')
    map_pos = f.read()
    f.close()
    map_pos = json.loads(map_pos)

    f = open('./outputfiles/common_cat/common_cat_biology_' + directory + '.txt', 'r')
    map_com_cat = f.read()
    f.close()
    map_com_cat = json.loads(map_com_cat)

    map_out = {}
    files = list(map_pos.keys())

    for file in files:

        print(file)
        commons = {}

        try:
            nn_comp = list(set(map_pos[file]['NN'][1]))
            nns_comp = list(set(map_pos[file]['NNS'][1]))

            common_files = list(map_com_cat[file].keys())
            for com in common_files:

                try:
                    nn_curr = list(set(map_pos[com]['NN'][1]))
                    nns_curr = list(set(map_pos[com]['NNS'][1]))

                    nn_union = list(set(nn_comp+nn_curr))
                    nns_union = list(set(nns_comp+nns_curr))

                    commons[com] = {'NN': nn_union, 'NNS': nns_union}

                except:
                    continue

                map_out[file] = commons

        except:
            map_out[file] = 'Decoding Error'

    map_out = json.dumps(map_out)

    file_path = './outputfiles/pos_tagging/pos_tagging_union/pos_tagging_union_biology_' + directory + '.txt'
    f = open(file_path, 'w')
    f.write(map_out)
    f.close()

    print('Scrittura completata')