import os, glob, json

directories = ['PS001']

for dir in directories:

    path = './data/subtitles-V3-by-topic/Psychology/'+dir
    os.chdir(path)

    files = []

    for file in glob.glob('*.txt'):
        files.append(file)

    os.chdir('../../../../outputfiles')

    file_path = 'dbpedia_spotlight/dbpedia_spotlight_psychology_'+dir+'.txt'
    f = open(file_path,'r')
    map = f.read()
    map = json.loads(map)
    f.close()

    common_res = {}

    i = 0
    while i<len(files):

        j = 0
        print(files[i])
        ai = map[files[i]]
        common_res[files[i]] = {}
        uri_i = []

        for obj in ai:
            uri_i.append(obj['URI'])

        uri_i = list(set(uri_i))

        while j<len(files):

            if i == len(files)-1 and i == j:
                break

            if files[i] == files[j]:
                j = j+1

            cont = 0
            aj = map[files[j]]
            uri_j = []

            for obj in aj:
                uri_j.append(obj['URI'])

            for res_i in uri_i:
                for res_j in uri_j:
                    if res_i == res_j:
                        cont = cont+1

            if cont>4:
                common_res[files[i]][files[j]] = cont

            j = j+1

        i = i+1

    common_res = json.dumps(common_res)

    file_path = 'common_res/common_res_psychology_'+dir+'.txt'
    f = open(file_path,'w')
    f.write(str(common_res))
    f.close()
    os.chdir('../')

    print('Scrittura completata')