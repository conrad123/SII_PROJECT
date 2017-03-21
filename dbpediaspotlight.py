import spotlight

f = open('./data/subtitles-V3-by-topic/Biology/BIO110/bio110 Amino Acids.txt','r')
text = f.read()
f.close()

annotations = spotlight.annotate('http://spotlight.sztaki.hu:2222/rest/annotate',text,confidence=0.5,support=20)

print(text)

for annotation in annotations:
    print(annotation)