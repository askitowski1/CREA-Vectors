# CREA-Vectors

This is a package to access CREA vectors. Various data collection methods are also include.
Future updates will all users to add their collected vectors to the main set

## How to run the code
1. Clone the repository
2. Navigate to the repository and run python crea.py
3. In python import the file
   - from crea import CREA
   - crea_initialize = CREA() #this will automatically pull from the main dictionary, or you can pass your own json file
   - use get_all_vectors, get_vector, get_vectors, select_cols, cosine_similarity, get_n_similar

## PsychoPy Data Collection
- Results are saved as a JSON file named "results.json"
- Currently it is overwritten each time
- JSON file has the structure {"target_word": {"Rating Category 1": rating_1, ... "Rating Category n": rating_n}}


