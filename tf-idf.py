import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
import os, glob, json

directories = ['CS046']

file = './outputfiles/hierarchies/hierarchies__CS046.txt'

f = open(file,'r')

obj = f.read()
f.close()

obj = json.loads(obj)

file_list = []
text_list = []
result = {}

for i in obj:
    print (i)
    result[i] = []
    file_list = obj[i]['broaders']
    file_list.append(i)
    file_list = file_list + obj[i]['is_broder_of']

    for y in file_list:
        f = open('./data/subtitles-V3-by-topic/Computer Science/CS046/'+ y)
        text = f.read()
        f.close()
        text_list.append(text)

    tf = TfidfVectorizer(min_df=1)
    x = tf.fit_transform(text_list)
    idf = tf.idf_
    dictionary = dict(zip(tf.get_feature_names(), idf))
    dictionary = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)

    result[i] = dictionary

print(result)