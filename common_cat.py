import json

directories = ['PS001']

for dir in directories:

    file_path = './outputfiles/sparql/categories_psychology_'+dir+'.txt'
    f = open(file_path,'r')
    map = f.read()
    map = json.loads(map)
    f.close()

    files = list(map.keys())

    common_cat = {}

    i = 0

    while i<len(files):

        j = 0
        print(files[i])
        ai = map[files[i]]

        common_cat[files[i]] = {}

        while j<len(files):

            if files[i] != files[j]:

                cont = 0
                aj = map[files[j]]

                for c_i in ai[0]:
                    for c_j in aj[0]:
                        if c_i == c_j:
                            cont = cont+1

                if cont>0:
                    common_cat[files[i]][files[j]] = cont

            j = j+1

        i = i+1

    common_cat = json.dumps(common_cat)

    file_path = './outputfiles/common_cat/common_cat_psychology_'+dir+'.txt'
    f = open(file_path,'w')
    f.write(common_cat)
    f.close()

    print('Scrittura completata')
