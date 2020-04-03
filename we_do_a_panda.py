import pandas as pd
import csv


def calculator(data):

    df = pd.read_csv(data, sep=";", names = ["Title", "Brand", "Kategorie", "ml", "Preis"])

    print(df)

    df["Preis"] = pd.to_numeric(df["Preis"])
    df["ml"] = pd.to_numeric(df["ml"])
    df["Preis pro 100 ml"] = df["Preis"] / df["ml"] * 100

    print(df)

    df.to_csv("ottos_meets_panda.csv", index=False)


with open ("ottos.csv") as df:
    calculator(df)