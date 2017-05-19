
import wikipedia
import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from sklearn.externals import joblib
from string import digits
import string

#read training data
df = pd.read_csv('/home/nilesh/Downloads/TrainActors.txt', sep='\t', names = ['label', 'name'])
df['data'] = pd.Series('default' , index=df.index)
digits = string.maketrans('', '')
#print(df)
#update summary for each actor in training data
def strip_non_ascii(string):
        stripped = (c for c in string if 0 < ord(c) < 127)
        return ''.join(stripped)
        
for index, row in df.iterrows():
    ag = wikipedia.search(row['name'])
    x=wikipedia.summary(ag[0])
    info= strip_non_ascii(x)
    df.loc[index, 'data'] = str(info).translate(digits)

# print(df['data'])

#make a TFIDF vertor for model building     
df_x = df["data"]
df_y = df["label"]
cv = TfidfVectorizer(min_df=1, stop_words='english')
x_traincv = cv.fit_transform(df_x)
#print(x_traincv[0])
# a = x_traincv.toarray()
# print(len(cv.inverse_transform(a)))
 
 #get test instance from text file and convert to TFIDF vertor
#df1 = pd.read_csv('/Users/devendralad/Desktop/testActors.txt', sep='\t', names = ['data'])
#print(df1)
#df1_test = df1['data']
# x_testcv = cv.transform(df1_test)
 
#model building and store
mnb = MultinomialNB()
df_y = df_y.astype('int')
mnb.fit(x_traincv, df_y)
joblib.dump(mnb, '/home/nilesh/Downloads/NB.pkl')
joblib.dump(cv, '/home/nilesh/Downloads/vectorizer.pkl')
print("done")