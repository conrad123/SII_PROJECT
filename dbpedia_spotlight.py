import spotlight, os, glob

os.chdir('./data/subtitles-V3-by-topic/Biology/BIO110')

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

os.chdir('../../../../outputfiles')
f = open('dbpediaspotlight_biology.txt','w')
f.write(str(map))
f.close()

print('Scrittura completata')