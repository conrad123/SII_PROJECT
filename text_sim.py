import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
import os, glob, json

directories = ['CS046']

f = open('./outputfiles/common_cat/common_cat_computerscience_CS046.txt', 'r')
common_res = f.read()
common_res = json.loads(common_res)
f.close()

stem = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def stem_tokens(tokens):
    return [stem.stem(item) for item in tokens]

'''remove punctuation, lowercase, stem'''
def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

def cosine_sim(text1: object, text2: object) -> object:
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]

for dir in directories:

    path = './data/subtitles-V3-by-topic/Computer Science/'+dir
    os.chdir(path)

    files = []

    for file in glob.glob('*.txt'):
        files.append(file)

    i = 0
    map = {}

    while i<len(files):

        print(files[i])
        common_files = list(common_res[files[i]].keys())

        j=0
        file2similarity = {}


        while j<len(common_files):

            file_i = open(files[i], 'r')
            file_j = open(common_files[j], 'r')
            text_i = file_i.read()
            text_j = file_j.read()
            file_i.close()
            file_j.close()
            cos_sim = cosine_sim(text_i, text_j)

            file2similarity[common_files[j]] = cos_sim


            j = j+1

        map[files[i]] =file2similarity

        i=i+1

    map = json.dumps(map)

    file_path = 'text_sim/text_sim_computerscience_' + dir + '.txt'
    os.chdir('../../../../outputfiles')
    f = open(file_path, 'w')
    f.write(str(map))
    f.close()
    os.chdir('../')

    print('Scrittura completata')


