import pandas as pd
import numpy as np
import string
import re
import nltk
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords  
import pickle

class Manipulate:

    def __init__(self,text):
        self.text=text

    def transform_data(self):
        tf = pickle.load(open('scaler.pkl', 'rb'))
        wnl = WordNetLemmatizer()
        stopwords_list=stopwords.words('english')
        for x in ["hadn't",'hasn',"hasn't",'haven',"haven't",'isn',"isn't",'no',"nor",'not']:
            stopwords_list.remove(x)
        text_new=[]
        for x in self.text:
            x=x.lower()
            x=re.sub(r'[^\w\s]', '', x)
            x=' '.join(wnl.lemmatize(t) for t in x.split() if t not in stopwords_list)
            text_new.append(x)
        return text_new
