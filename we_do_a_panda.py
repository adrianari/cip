import pandas as pd
import csv














with open ("ottos.csv") as x:
    df = pd.read_csv(x, header=None)

print(df[df.columns[3:5]])
