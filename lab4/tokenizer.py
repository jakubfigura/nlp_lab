import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import Counter

class BasicTokenizer:
    
    #TODO 
    def train(self, text, vocab_size, verbose = False):
        pass


    #TODO
    def encode(self, text):
        pass
        
    #TODO 
    def deode(self, ids):
        
        pass


def pair_comparison(numbers):

    counts = {}
    
    pass


with open("taylorswift.txt") as file:
    text = file.read()

characters_dictionary = set([i for i in text])
# print(sorted(characters_dictionary))

characters_distributions = dict(Counter([i for i in text]))
# print(characters_distributions)


filtered_dict = {k: v for k, v in characters_distributions.items() if v > 100}
keys = list(filtered_dict.keys())
values = list(filtered_dict.values())

sorted_value_index = np.argsort(values)
sorted_dict = {keys[i]: values[i] for i in reversed(sorted_value_index)}

print(sorted_dict)

plt.barh(sorted_dict.keys(), sorted_dict.values())
plt.show()







