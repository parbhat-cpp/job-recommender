import pandas as pd
import numpy as np
import os
import yaml
from dotenv import load_dotenv

from src.logger import logging
from src.utils import load_object,preprocess_text,load_numpy_array
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

class Prediction:
    def __init__(self) -> None:
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        self.vectorizer_path = config['vectorizer']['path']
        self.train_vector_path = config['vector']['path']
        self.dataset_path = config['dataset']['path']
        self.vectorizer = load_object(os.path.join(self.vectorizer_path))
    
    def predict(self, text: str):
        try:
            processed_text = preprocess_text(text)
            processed_text = " ".join(processed_text)
            input_vector = self.vectorizer.transform([processed_text])
            
            trained_vector = load_numpy_array(os.path.join(self.train_vector_path))
            df = pd.read_csv(os.path.join(self.dataset_path))

            similarity_score = cosine_similarity(input_vector, trained_vector).flatten()
            top_indices = similarity_score.argsort()[-5:][::-1]
            
            output_list = []

            for i in top_indices:
                output_list.append(df.iloc[i])

            output_df = pd.DataFrame(output_list, columns=['company', 'rating', 'location', 'positionName', 'description', 'salary', 'url', 'job_type', 'externalApplyLink'])
            return output_df
        except Exception as e:
            logging.error(e)
