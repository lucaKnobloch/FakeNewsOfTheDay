import re
import pandas as pd
from keras.engine.saving import model_from_json
import numpy as np
from tensorboard.compat import tf

# read the dataset 
dataset = pd.read_csv('./data_files/data.csv')

# prints the shape of the dataset which also represents that the reading process worked
print(dataset.shape)

# saves the text and label from the loaded dataset
texts=dataset['text']
label=dataset['label']

# preprocessing steps to clean up the content of the article
def striphtml(html):
    p = re.compile(r'<.*?>')
    return p.sub('', html)

def clean(s):
    return re.sub(r'[^\x00-\x7f]', r'', s)

# Hyperparameter
MAX_SENT_LENGTH = 300
MAX_SENTS = 20
docs_test = []
txt=''

# clean the sentences before feeding in the model
for statement in (texts):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', clean(striphtml(statement)))
    sentences = [sent.lower() for sent in sentences]
    docs_test.append(sentences)


X_test = np.ones((len(docs_test), MAX_SENTS, MAX_SENT_LENGTH), dtype=np.int64) * -1
for doc in docs_test:
    for s in doc:
        txt += s

chars = set(txt)
print('total chars:', len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

for i, doc in enumerate(docs_test):
    for j, sentence in enumerate(doc):
        if j < MAX_SENTS:
            for t, char in enumerate(sentence[-MAX_SENT_LENGTH:]):
                if char not in char_indices.keys():
                   continue
                X_test[i, j, (MAX_SENT_LENGTH-1-t)] = char_indices[char]

x_test=X_test

# opens the model which is saved as in a json file before
json_file = open('./trained_model/model.json', 'r')

# reads the file to read it 
loaded_model_json = json_file.read()

# closes the json file again that the space is not unnecessary beeing used 
json_file.close()

# loads the model from the json loaded json file
loaded_model = model_from_json(loaded_model_json, custom_objects={'tf': tf})
print("loaded model from disk")

# load weights 
loaded_model.load_weights("./trained_model/model.h5")
print("loaded weights of the model from disk")


# compile loaded model on test data
loaded_model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['acc'])
print("model is compiled")

# makes the prediction of the new given data 
y_pred = loaded_model.predict(x_test)

y2=[]
# sets the prediction to a binary classification
for q in y_pred:
    # either it is higher or smaller than 0.5 
	if(q[0]>0.5):
		y2.append(True)
	else:
		y2.append(False)

# adds a label colum to the dataset 
dataset['label'] = y2
print('data is labeled')

# writes the dataset back to the csv file 
dataset.to_csv('./data_files/labeled_data.csv', index=False)
print('data is saved to labeled_data.csv')
