import nltk, glob, os

os.chdir('./data/subtitles-V3-by-topic/Biology/BIO110')

for file in glob.glob('*.txt'):

    f = file
    f = open(f,'r')
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

    print(tags)
    print('Terms: '+str(len(split)))
    print('NN: '+str(contnn)+'\tNNS: '+str(contnns))