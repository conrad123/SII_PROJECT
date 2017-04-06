import nltk, glob, os, json

directories = ['BIO110']

for dir in directories:

    path = './data/subtitles-V3-by-topic/Biology/'+dir
    os.chdir(path)

    map = {}

    for file in glob.glob('*.txt'):

        print(file)

        f = open(file,'r')
        text = f.read()
        f.close()

        split = text.split()
        try:
            text = nltk.word_tokenize(text)
            tags = nltk.pos_tag(text)

            nn = []
            nns = []
            contnn = 0
            contnns = 0

            for tag in tags:
                if tag[1] == 'NN':
                    contnn += 1
                    nn.append(tag[0])
                if tag[1] == 'NNS':
                    contnns += 1
                    nns.append(tag[0])

            map[file] = {'Terms': len(split), 'NN': (contnn,nn), 'NNS': (contnns,nns)}

        except:
            map[file] = 'Decoding Error'

    map = json.dumps(map)

    file_path = 'pos_tagging/pos_tagging_biology_'+dir+'.txt'
    os.chdir('../../../../outputfiles')
    f = open(file_path, 'w')
    f.write(map)
    f.close()
    os.chdir('../')

    print('Scrittura completata')