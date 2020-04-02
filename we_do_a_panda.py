import pandas as pd
import csv

with open ("ottos.csv") as f:
    x = pd.read_csv(f)
    print(x)
