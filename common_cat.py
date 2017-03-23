import os, glob, json

directories = ['BIO110']

for dir in directories:

    path = './data/subtitles-V3-by-topic/Biology/'+dir
    os.chdir(path)

    files = []

    for file in glob.glob('*.txt'):
        files.append(file)

    os.chdir('../../../../outputfiles')

    file_path = 'sparql/categories_biology_'+dir+'.txt'
    f = open(file_path,'r')
    map = f.read()
    map = json.loads(map)
    f.close()

    common_cat = {}

    i = 0
    while i<len(files):

        j = 0
        print(files[i])
        ai = map[files[i]]

        common_cat[files[i]] = {}

        while j<len(files):

            if i == len(files)-1 and i == j:
                break

            if files[i] == files[j]:
                j = j+1

            cont = 0
            aj = map[files[j]]

            for c_i in ai[0]:
                for c_j in aj[0]:
                    if c_i == c_j:
                        cont = cont+1

            if cont>2:
                common_cat[files[i]][files[j]] = cont

            j = j+1

        i = i+1

    common_cat = json.dumps(common_cat)

    file_path = 'common_cat/common_cat_biology_'+dir+'.txt'
    f = open(file_path,'w')
    f.write(str(common_cat))
    f.close()
    os.chdir('../')

    print('Scrittura completata')
