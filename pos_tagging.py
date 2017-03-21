import nltk, glob, os, json

os.chdir('./data/subtitles-V3-by-topic/Biology/BIO110')

map = {}

for file in glob.glob('*.txt'):

    print(file)

    f = open(file,'r')
    text = f.read()
    f.close()

    split = text.split()
    text = nltk.word_tokenize(text)
    tags = nltk.pos_tag(text)

    contnn = 0
    contnns = 0
    for tag in tags:
        if tag[1] == 'NN':
            contnn += 1
        if tag[1] == 'NNS':
            contnns += 1

    map[file] = {'Terms': len(split), 'NN': contnn, 'NNS': contnns}

map = json.dumps(map)

os.chdir('../../../../outputfiles')
f = open('pos_tagging/pos_tagging_biology.txt', 'w')
f.write(str(map))
f.close()

print('Scrittura completata')