import spotlight, os, glob, json

directories = ['DESIGN101','UD509']

for dir in directories:

    path = './data/subtitles-V3-by-topic/Design/'+dir
    os.chdir(path)

    map = {}

    for file in glob.glob('*.txt'):

        f = open(file,'r')
        text = f.read()
        f.close()

        print(file)

        try:
            annotations = spotlight.annotate('http://spotlight.sztaki.hu:2222/rest/annotate',text,confidence=0.5,support=20)
            i = 0
            while i<len(annotations):
                annotations[i] = {'sourfaceForm': annotations[i]['surfaceForm'], 'URI': annotations[i]['URI']}
                i = i+1
            map[file] = annotations
        except:
            map[file] = []

    file_path = 'dbpedia_spotlight/dbpedia_spotlight_design_'+dir+'.txt'
    os.chdir('../../../../outputfiles')
    f = open(file_path,'w')
    f.write(str(json.dumps(map)))
    f.close()
    os.chdir('../')

    print('Scrittura completata')