import nltk, glob, os, json

directories = ['PS001']

for dir in directories:

    f = open('./outputfiles/pos_tagging/pos_tagging_psychology_'+dir+'.txt','r')
    map_pos = f.read()
    f.close()
    map_pos = json.loads(map_pos)

    f = open('./outputfiles/common_cat/common_cat_psychology_'+dir+'.txt','r')
    map_com_cat = f.read()
    f.close()
    map_com_cat = json.loads(map_com_cat)

    path = './data/subtitles-V3-by-topic/Psychology/'+dir
    os.chdir(path)

    map_out = {}
    files = []
    for file in glob.glob('*.txt'):
        files.append(file)

    for file in files:
        print(file)
        commons = {}
        try:
            nn_comp = list(set(map_pos[file]['NN'][1]))
            nns_comp = list(set(map_pos[file]['NNS'][1]))

            common_files = map_com_cat[file].keys()
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

    file_path = 'pos_tagging/pos_tagging_union_psychology_'+dir+'.txt'
    os.chdir('../../../../outputfiles')
    f = open(file_path, 'w')
    f.write(str(map_out))
    f.close()
    os.chdir('../')

    print('Scrittura completata')