# CREA-Vectors
Website
- In order to run the website locally, download the website folder. 
- Activate an environment with flask, scipy, and scikit-learn installed 
- Navigate to the directory with your files to run "python app.py"
- Copy and paste http://127.0.0.1:5000 in your browser to view the webpage locally
- The original data on this page comes from all_words.csv
- Be sure to click "Update Table" after selecting your desired columns but before clicking desired words

Crea Library
- Use the Crea library on a dictionary of words with "pip install Crea-library==0.3"
- import library via "from Crea_library.crea_library import *"
  
[crea_methods.docx](https://github.com/user-attachments/files/18711458/crea_methods.docx)

PsychoPy Data Collection
- Results are saved as a JSON file named "results.json"
- Currently it is overwritten each time
- JSON file has the structure {"target_word": {"Rating Category 1": rating_1, ... "Rating Category n": rating_n}}
