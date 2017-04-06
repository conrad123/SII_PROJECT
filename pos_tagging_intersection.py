import json

directories = ['BIO110']

for dir in directories:

    f = open('./outputfiles/pos_tagging/pos_tagging_biology_'+dir+'.txt','r')
    map = f.read()
    f.close()

    map = json.loads(map)

    map_out = {}
    files = list(map.keys())

    for file in files:

        print(file)

        try:
            nn_comp = set(map[file]['NN'][1])
            nns_comp = set(map[file]['NNS'][1])

            i = 0
            commons = {}

            while i<len(files):

                if files[i] != file:
                    try:
                        nn_curr = set(map[files[i]]['NN'][1])
                        nns_curr = set(map[files[i]]['NNS'][1])

                        nn_intersect = list(nn_comp.intersection(nn_curr))
                        nns_intersect = list(nns_comp.intersection(nns_curr))

                        if len(nn_intersect)>4 or len(nns_intersect)>4:
                            commons[files[i]] = {'NN': nn_intersect, 'NNS': nns_intersect}
                    except:
                        i = i+1
                        continue

                    i = i+1

            map_out[file] = commons

        except:
            map_out[file] = 'Decoding Error'

    map_out = json.dumps(map_out)

    file_path = './outputfiles/pos_tagging/pos_tagging_intersection_biology_'+dir+'.txt'
    f = open(file_path, 'w')
    f.write(map_out)
    f.close()

    print('Scrittura completata')