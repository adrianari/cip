import pandas as pd
import csv


def calculator(data):
    #setting up dataframe
    df = pd.read_csv(data, sep=";", names = ["Title", "Brand", "Kategorie", "ml", "Preis"])

    #Calculating price for 100ml
    df["Preis"] = pd.to_numeric(df["Preis"])
    df["ml"] = pd.to_numeric(df["ml"])
    df["Preis pro 100 ml"] = df["Preis"] / df["ml"] * 100

    #filling missing values for title (only happend for one specific parfum)
    df["Title"].fillna("Naomi Campbell", inplace=True)

    #export
    df.to_csv("ottos_meets_panda.csv", index=False, header = True, sep=";")

with open ("ottos.csv") as df:
    calculator(df)