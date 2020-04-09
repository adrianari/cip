import pandas as pd
import csv

data = "ottos.csv"
#setting up dataframe
df = pd.read_csv(data, sep=";", names = ["Title", "Brand", "Kategorie", "ml", "Preis"])

df.iloc[58] = df.iloc[58].replace(to_replace = 10, value=60)


#Calculating price for 100ml
df["Preis"] = pd.to_numeric(df["Preis"])
df["ml"] = pd.to_numeric(df["ml"])
df["Preis pro 100 ml"] = df["Preis"] / df["ml"] * 100

#filling missing values for title (only happend for one specific parfum)
df["Title"].fillna("Naomi Campbell", inplace=True)

#correcting
print(df.iloc[58])

