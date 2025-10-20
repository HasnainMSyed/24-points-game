#import numpy as np
#import pandas as pd
#import os
#from tensorflow.keras.preprocessing.sequence import pad_sequences


VOCABULARY_MAP = {
    1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10", 11: "11",
    12: "12", 13: "13", 14: "+", 15: "-", 16: "*", 17: "/", 18: "(", 19: ")", 20: "IMPOSSIBLE",
    21: "START", 22: "END"
}

TOKEN_TO_ID = {token: id_val for id_val, token in VOCABULARY_MAP.items()}

