import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# OS handles system problems, and the extra lines silence Tensorflow Error Messages

import numpy as np
import pandas as pd
# Libraries that handles data

from keras.utils import pad_sequences
from keras.models import Model
from keras.layers import Input, Embedding, LSTM, Dense, TimeDistributed
# Importing the ML library

# Initializing vocabulary map from ID to Token
VOCABULARY_MAP = {
    1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10", 11: "11",
    12: "12", 13: "13", 14: "+", 15: "-", 16: "*", 17: "/", 18: "(", 19: ")", 20: "IMPOSSIBLE",
    21: "START", 22: "END"
}

# Reverse the formatting so we can access from token to id faster
# More efficient when scaling up the complexity, and we have a complex case here
# This is a Must-do
TOKEN_TO_ID = {token: id_val for id_val, token in VOCABULARY_MAP.items()}

PAD_ID = 0 # Adding the PAD_ID so the model can fill up the dummy slots
MAX_INPUT_LENGTH = 5 # The neural network takes in the four cards and one target
MAX_OUTPUT_LENGTH = 30 # The maximum length for expression output by the model
VOCAB_SIZE = len(VOCABULARY_MAP) + 1 # +1 is for PAD_ID

# load the data in with pandas dataframe
def load_data():
    file_path = os.path.join("24_NN", "24_game_data.csv")
    
    try: # dataframe below contains the dataset values, only use the input_numbers and solution_expression columns
        df = pd.read_csv(file_path, usecols=[0,2])
        print(f"Successfully loaded {len(df)} rows from {file_path}")
        return df
    except FileNotFoundError: # If file doesn't exist, output the error message
        print("Error: The file path is invalid.")
        return None
        

if __name__ == "__main__":
    print(TOKEN_TO_ID)