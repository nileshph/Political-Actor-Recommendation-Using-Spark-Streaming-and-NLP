
import wikipedia
import random
import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from sklearn.externals import joblib
from string import digits
import string

class wikidata:
    
    def strip_non_ascii(self,string):
        stripped = (c for c in string if 0 < ord(c) < 127)
        return ''.join(stripped)

    def getProbability(self,actor):
        #read training data
        # df = pd.read_csv('/Users/devendralad/Desktop/TrainActors.txt', sep='\t', names = ['label', 'name'])
        # df['data'] = pd.Series('default' , index=df.index)
        # digits = str.maketrans('', '', digits)
        #print(df)
        #update summary for each actor in training data
        # for index, row in df.iterrows():
        #     ag = wikipedia.search(row['name'])
        #     df.loc[index, 'data'] = str(wikipedia.summary(ag[0])).translate(digits)
        
        # print(df['data'])
     
        #make a TFIDF vertor for model building     
        # df_x = df["data"]
        # df_y = df["label"]
        # cv = TfidfVectorizer(min_df=1, stop_words='english')
        # x_traincv = cv.fit_transform(df_x)
        #print(x_traincv[0])
        # a = x_traincv.toarray()
        # print(len(cv.inverse_transform(a)))
         
         #get test instance from text file and convert to TFIDF vertor
        #df1 = pd.read_csv('/Users/devendralad/Desktop/testActors.txt', sep='\t', names = ['data'])
        #print(df1)
        #df1_test = df1['data']
        # x_testcv = cv.transform(df1_test)
         
        #model building and store
        # mnb = MultinomialNB()
        # df_y = df_y.astype('int')
        # mnb.fit(x_traincv, df_y)
        # joblib.dump(mnb, '/Users/devendralad/Desktop/NB.pkl')
        # joblib.dump(cv, '/Users/devendralad/Desktop/vectorizer.pkl')
        
        #get actors wiki and convert to dataframe ->> actor from function call
        try:
            results = wikipedia.search(actor)
            if(len(results) != 0):
                info = self.strip_non_ascii(wikipedia.summary(results[0]))
                actor_wiki= (info).translate(digits)
                d = {'data' : pd.Series(actor_wiki)}
                df2 = pd.DataFrame(d)
                df2_test = df2['data']
                print(df2_test)
                #fetch
                loaded_model = joblib.load('/Users/nikitakothari/Downloads/NB.pkl')
                loaded_vc = joblib.load('/Users/nikitakothari/Downloads/vectorizer.pkl')
                x_testcv = loaded_vc.transform(df2_test);
                pred = loaded_model.predict_proba(x_testcv)
              
                return pred[0][1] * 100;
            else:
                return 0;
        except:
            print ("exception in wiki check")
            return random.uniform(0,1) * 100;
    
    # function call
    #val = getProbability(actor=str('amitabh bacchan'))
    #print(val)