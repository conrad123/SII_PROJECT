import pandas
import numpy
from sklearn.preprocessing import MinMaxScaler
import json

data = "outputfiles/pos_tagging/pos_tagging_physics_PH100.txt"
names = ['TERMS', 'NN', 'NNS']

normalized = {}

df = pandas.read_json(str(data), typ='index')
keys = df.keys()
array = df.values
big_array = [None]*len(array)

i=0
for index in array:
    tmp = []
    NN = index['NN'][0]
    NNS = index['NNS'][0]
    terms = index['Terms']
    tmp.append(int(NN))
    tmp.append(int(NNS))
    tmp.append(int(terms))
    big_array[i] = tmp
    i = i+1

numpy.set_printoptions(precision=3)
scaler = MinMaxScaler(feature_range=(0, 1))
rescaled = scaler.fit_transform(big_array)
j=0

while j<len(keys):
    normalized[keys[j]] = {'NN': rescaled[j][0], 'NNS': rescaled[j][1], 'Terms': rescaled[j][0]}
    j = j+1

print(normalized)
printNormalize = json.dumps(normalized)

file_path = './outputfiles/normalization/normalization_physics_PH100.txt'
f = open(file_path, 'w')
f.write(printNormalize)
f.close()

print('Scrittura completata')
