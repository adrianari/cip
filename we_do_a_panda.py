import pandas as pd
import csv


def calculator(df):

    data = pd.read_csv(df, sep=";")
    df = pd.DataFrame(data, columns=["Title", "Brand", "Kategorie", "ml", "Preis"])
    spalte = []

    for line in df:
        df["Preis"] = pd.to_numeric(df["Preis"])
        df["ml"] = pd.to_numeric(df["ml"])
        df["Preis pro 100 ml"] = df["Preis"] / df["ml"] * 100

    print(spalte)












with open ("ottos.csv") as df:
    calculator(df)