import os
import numpy as np
import pickle

from gensim.utils import simple_preprocess
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

from src.logger import logging

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    try:
        tokens = simple_preprocess(text, deacc=True, min_len=3)
        
        clean_tokens = [
            lemmatizer.lemmatize(word) for word in tokens if word not in stop_words
        ]
        return clean_tokens
    except Exception as e:
        logging.error(e)

def save_numpy_array(file_path, arr):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        
        arr = arr.toarray()
        
        np.save(file_path, arr)
    except Exception as e:
        logging.error(e)

def save_object(file_path, obj):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
    except Exception as e:
        logging.error(e)

def load_numpy_array(file_path):
    try:
        if not os.path.exists(file_path):
            raise Exception("File does not exists")
        
        return np.load(file_path, allow_pickle=True)
    except Exception as e:
        logging.error(e)

def load_object(file_path):
    try:
        with open(file_path, "rb") as file:
            return pickle.load(file)
    except Exception as e:
        logging.error(e)
