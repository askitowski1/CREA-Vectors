class CREA_library:
    def __init__(self, word_vectors):
        self.word_vectors = word_vectors

    def get_vector(self, word):
        return self.word_vectors.get(word)
    
    def get_vectors(self, words):
        selected_vecs = {}
        for word in words:
            vec = self.get_vector(word)
            if vec is not None:
                selected_vecs[word] = vec
        return selected_vecs
    
    def select_cols(self, words, columns):
        selected_vecs = {}
        for word in words:
            vec = self.get_vector(word)
            if vec is not None:
                selected_vecs[word] = [vec[col] for col in columns]
        return selected_vecs
    
    def cosine_similarity(self, vec1, vec2):
        vec1 = self.get_vector(vec1)
        vec2 = self.get_vector(vec2)

        if vec1 is None or vec2 is None:
            return ValueError("Words not found")
    
        vec1 = np.array(vec1).reshape(1, -1)
        vec2 = np.array(vec2).reshape(1, -1)
        return cosine_similarity(vec1, vec2)[0][0]
    

