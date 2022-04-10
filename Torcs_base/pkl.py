import os
import pickle

with open("elites.pkl", "rb") as handle:
        top = pickle.load(handle)

print(top)
