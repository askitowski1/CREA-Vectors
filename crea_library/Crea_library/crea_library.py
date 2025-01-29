import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class CREA_library:
    """
    A class for selecting and comparing word vectors from the CREA dataset

    :param word_vectors: A dictionary of word vectors
    :type word_vectors: dict
    """

    def __init__(self, word_vectors):
        self.word_vectors = word_vectors

    def get_all_vectors(self):
        """
        Get the vectors for all words in the dataset
        """
        return self.word_vectors
    
    def get_vector(self, word):
        """
        Get the vector for a single word
        :param word: The target word to get the vector for
        :type word: str
        """
        return self.word_vectors.get(word)

    def get_vectors(self, words):
        """
        Get the vectors for a list of words
        :param words: A list of target words to get the vectors for
        :type words: list
        """
        return {word: self.word_vectors.get(word) for word in words if word in self.word_vectors}

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
    
    def cosine_similarity(self, vec1, vec2):
        """
        Calculate the cosine similarity between two words
        :param vec1: The first word
        :type vec1: str
        :param vec2: The second word
        :type vec2: str
        """
        if isinstance(vec1, str):
            vec1 = self.get_vector(vec1)
        if isinstance(vec2, str):
            vec2 = self.get_vector(vec2)

        if vec1 is None or vec2 is None:
            raise ValueError("Words not found")
    
        vec1 = np.array(vec1).reshape(1, -1)
        vec2 = np.array(vec2).reshape(1, -1)
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
            raise ValueError("Word not found")
        
        similarities = {}
        for other_word, vec in self.word_vectors.items():
            if other_word != word:
                similarity = self.cosine_similarity(target_vec, vec)
                similarities[other_word] = similarity
        
        sorted_similarities = sorted(similarities.items(), key=lambda item: item[1], reverse=True)
        return sorted_similarities[:n]

    @staticmethod
    def load_word_from_json(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)