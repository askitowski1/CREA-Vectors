# import json
# import bson
# import numpy as np
# import os
# import csv
# from sklearn.metrics.pairwise import cosine_similarity

# PACKAGE_DIR = os.path.dirname(__file__)
# DATA_PATH = os.path.join(PACKAGE_DIR, "data", "word_vectors.json")

# class crea:
#     """
#     A class for selecting and comparing word vectors from the CREA dataset

#     :param word_vectors: A dictionary of word vectors
#     :type word_vectors: dict
#     """

#     def __init__(self, word_vectors):
#         self.word_vectors = word_vectors

#     def get_all_vectors(self):
#         """
#         Get the vectors for all words in the dataset
#         """
#         return self.word_vectors
    
#     def get_vector(self, word):
#         """
#         Get the vector for a single word
#         :param word: The target word to get the vector for
#         :type word: str
#         """
#         return self.word_vectors.get(word)

#     def get_vectors(self, words):
#         """
#         Get the vectors for a list of words
#         :param words: A list of target words to get the vectors for
#         :type words: list
#         """
#         return {word: self.word_vectors.get(word) for word in words if word in self.word_vectors}

#     def select_cols(self, words, columns):
#         """
#         Create a vector of specific columns of specific words in the dataset
#         :param words: A list of target words
#         :type words: list
#         :param columns: A list of target columns
#         :type columns: list
#         """
#         selected_vecs = {}
#         for word in words:
#             vec = self.get_vector(word)
#             if vec is not None:
#                 selected_vecs[word] = [vec[col] for col in columns]
#         return selected_vecs
    
#     def cosine_similarity(self, vec1, vec2):
#         """
#         Calculate the cosine similarity between two words
#         :param vec1: The first word
#         :type vec1: str
#         :param vec2: The second word
#         :type vec2: str
#         """
#         if isinstance(vec1, str):
#             vec1 = self.get_vector(vec1)
#         if isinstance(vec2, str):
#             vec2 = self.get_vector(vec2)

#         if vec1 is None or vec2 is None:
#             raise ValueError("Words not found")
    
#         vec1 = np.array(vec1).reshape(1, -1)
#         vec2 = np.array(vec2).reshape(1, -1)
#         return cosine_similarity(vec1, vec2)[0][0]
    
#     def top_n_similar(self, word, n=5):
#         """
#         Get the top N most similar words to a target word by cosine similarity
#         :param word: The target word
#         :type word: str
#         :param n: The number of similar words to return (default is 5)
#         :type n: int
#         """
#         target_vec = self.get_vector(word)
#         if target_vec is None:
#             raise ValueError("Word not found")
        
#         similarities = {}
#         for other_word, vec in self.word_vectors.items():
#             if other_word != word:
#                 similarity = self.cosine_similarity(target_vec, vec)
#                 similarities[other_word] = similarity
        
#         sorted_similarities = sorted(similarities.items(), key=lambda item: item[1], reverse=True)
#         return sorted_similarities[:n]

#     def strip(file_name):
#         """
#         Remove columns from dictionary. Returns 'word': [list of values as floats]
#         :param file_name: The file name of the json data
#         :type file_name: str
#         """
#         with open(file_name) as f:
#             data = json.load(f)

#         lib  = crea(data)
#         all_vectors = lib.get_all_vectors()
#         vector_floats  = {}

#         for word, vector in all_vectors.items():
#             vector_floats[word] = [value for key, value in vector.items() if isinstance(value, float)]
#         return vector_floats 
    
#     def get_raw(file_name):
#         """
#         Get the raw data from the CREA dataset into a csv
#         :param file_name: The file name of the json data
#         :type file_name: str
#         """
#         with open(file_name) as f:
#             data = json.load(f)

#         header = [
#             "Word", "Vision", "Bright", "Dark", "Color", "Pattern", "Large", "Small", "Motion", 
#             "Biomotion", "Fast", "Slow", "Shape", "Complexity", "Face", "Body", "Touch", 
#             "Hot", "Cold", "Smooth", "Rough", "Light", "Heavy", "Pain", "Audition", 
#             "Loud", "Low", "High", "Sound", "Music", "Speech", "Taste", "Smell", "Head", 
#             "UpperLimb", "LowerLimb", "Manipulation", "Landmark", "Path", "Scene", "Near", 
#             "Toward", "Away", "Number", "Time", "Duration", "Long", "Short", "Caused", 
#             "Consequential", "Social", "Human", "Communication", "Self", "Cognition", 
#             "Benefit", "Harm", "Pleasant", "Unpleasant", "Happy", "Sad", "Angry", 
#             "Disgusted", "Fearful", "Surprised", "Drive", "Needs", "Attention", "Arousal"
#         ]

#         # Extract rows from the values of each dictionary
#         rows = []
        
#         #word is the key, attributes are the values
#         for word, attributes in data.items():
#             row = [word] + [attributes.get(attr, None) for attr in header[1:]]
#             rows.append(row)
        

#         file_exists = os.path.isfile('results.csv')
#         with open('results.csv', 'a', newline='') as file:
#             csv_writer = csv.writer(file)
#             if not file_exists:
#                 csv_writer.writerow(header) 
#             csv_writer.writerows(rows)

#     def calculate_averages(fname):
#         """
#         Calculate the averages of the CREA dataset
#         :param fname: The file name of the csv data
#         :type fname: str
#         """
#         with(open(fname)) as f:
#             data = pd.read_csv(f)
#         averages = data.groupby('Word').mean()
#         return averages

#     @staticmethod
#     def load_word_from_json(file_path):
#         with open(file_path, 'r') as f:
#             return json.load(f)
        
# __all__ = ['crea']

import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
import urllib.request

PACKAGE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(PACKAGE_DIR, "data", "data.json")

class CREA:
    def __init__(self, data_path=None):
        # Load the JSON file when an instance is created
        if data_path is None:
            # If no data_path is provided, use the default URL
            default_url = 'https://raw.githubusercontent.com/askitowski1/CREA-Vectors/refs/heads/main/WordVecs/updated_vecs.json'
            self.word_vectors = self._load_json_from_url(default_url)
        else:
            # If a custom path is provided, load from the file
            self.word_vectors = self._load_json_from_file(data_path)

    @staticmethod
    def _load_json_from_file(file_path):
        """Load JSON from a local file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Error: The file '{file_path}' is not found in current directory")
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            raise ValueError(f"Error: the file '{file_path}' is not a valid JSON file")
        

    @staticmethod
    def _load_json_from_url(url):
        """Load JSON from a URL."""
        with urllib.request.urlopen(url) as response:
            return json.load(response)

    def get_all_vectors(self):
        """Return all word vectors."""
        return self.word_vectors

    def get_vector(self, word):
        """
        Get the vector for a single word
        :param word: The target word to get the vector for
        :type word: str
        """
        vector = self.word_vectors.get(word)
        if vector is None:
            raise KeyError(f"Error: the word '{word}' is not found in word vector set")
        return vector

    def get_vectors(self, words):
        """
        Get the vectors for a list of words
        :param words: A list of target words to get the vectors for
        :type words: list
        """
        if not isinstance(words, list):
            raise TypeError("Error: 'words' must be a list of word strings")
        vectors = {}
        for word in words: 
            vec = self.word_vectors.get(word)
            if vec is not None:
                vectors[word] = vec
            else:
                print(f'Warning: the word "{word}" is not found in word vector set')
        return vectors
    
    def select_cols(self, words, columns):
        """
        Create a vector of specific columns of specific words in the dataset
        :param words: A list of target words
        :type words: list
        :param columns: A list of target columns
        :type columns: list
        """
        selected_vecs = {}
        for word in words:
            vec = self.get_vector(word)
            if vec is not None:
                selected_vecs[word] = [vec[col] for col in columns]
        return selected_vecs

    def cosine_similarity(self, word1, word2):
        """
        Calculate the cosine similarity between two words
        :param vec1: The first word
        :type vec1: str
        :param vec2: The second word
        :type vec2: str
        """

        vec1, vec2 = self.get_vector(word1), self.get_vector(word2)

        vec1, vec2 = np.array(vec1).reshape(1, -1), np.array(vec2).reshape(1, -1)
        return cosine_similarity(vec1, vec2)[0][0]

    def top_n_similar(self, word, n=5):
        """
        Get the top N most similar words to a target word by cosine similarity
        :param word: The target word
        :type word: str
        :param n: The number of similar words to return (default is 5)
        :type n: int
        """
        target_vec = self.get_vector(word)
        if target_vec is None:
            raise ValueError("Vector is empty")
        
        similarities = {}
        for other_word, vec in self.word_vectors.items():
            if other_word != word:
                similarity = self.cosine_similarity(word, other_word)
                similarities[other_word] = similarity
        
        sorted_similarities = sorted(similarities.items(), key=lambda item: item[1], reverse=True)
        return sorted_similarities[:n]