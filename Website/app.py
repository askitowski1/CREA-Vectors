from flask import Flask, render_template, request
import csv
import numpy as np
from scipy.spatial.distance import cosine
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

fname = '/Users/al33856/Downloads/CREA/all_words_float.csv'  # Update the path to your CSV file

# Function to get the vector by word
def get_vec_by_word(word, columns):
    with open(fname, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['Word'] == word:
                if not columns:
                    columns = row.keys()
                vec = np.array([row[col] for col in columns if col != 'Word'], dtype=np.float64)
                print(f"Vector for {word}: {vec}")  # Debug line
                return vec
    return None

def calculate_similarity(vec1, vec2):
    vec1 = np.array(vec1).reshape(1, -1)
    vec2 = np.array(vec2).reshape(1, -1)
    return cosine_similarity(vec1, vec2)[0][0]

@app.route('/', methods=['GET', 'POST'])
def display_csv():
    data = []
    columns = []
    selected_columns = []

    # Read the CSV file and store the data
    with open(fname, mode='r') as file:
        csv_reader = csv.DictReader(file)
        columns = csv_reader.fieldnames
        data = [row for row in csv_reader]
    
    if request.method == 'POST':
        # Get selected columns from the form submission
        selected_columns = request.form.getlist('columns')  # Get selected columns as a list
    else:
        selected_columns = request.args.getlist('columns')
    # If no columns are selected, use all columns by default
    if not selected_columns:
        selected_columns = columns

    # allows it to be passed to the html file
    return render_template('index.html', data=data, columns=columns, selected_columns=selected_columns)

# points to the view_item.html file
@app.route('/item/<word>', methods=['GET', 'POST'])
def view_item(word):
# Get selected columns from checkbox parameters
    selected_columns = request.args.getlist('columns')  
    if not selected_columns:
        selected_columns = ['Vision', 'Bright', 'Dark']  
    # Get the vector for the word
    vec = get_vec_by_word(word, selected_columns)

    # Get the word details from the CSV file
    data = {}
    with open(fname, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['Word'].lower() == word.lower():
                data = row
                break

    if not data:
        return "Item not found", 404

    # Convert the vector to a list 
    vec_list = vec.tolist() if vec is not None else []

    #Find similar words
    similar_words = []
    similar_word_vecs = {}

    with open(fname, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['Word'].lower() != word.lower():
                other_word_vec = get_vec_by_word(row['Word'], selected_columns)
                if other_word_vec is not None:
                    similarity = calculate_similarity(vec, other_word_vec)
                    similar_words.append((row['Word'], similarity))
                    similar_word_vecs[row['Word']] = other_word_vec
    similar_words.sort(key=lambda x: x[1], reverse=True)
    top_similar_words = similar_words[:5]

    return render_template('view_item.html', data=data, vec=vec_list, selected_columns=selected_columns, similar_words=top_similar_words, similar_word_vecs=similar_word_vecs)

if __name__ == '__main__':
    app.run(debug=True)
