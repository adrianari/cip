import pandas as pd
import csv


def calculator(data):
    #setting up dataframe
    df = pd.read_csv(data, sep=";", names = ["Title", "Brand", "Kategorie", "ml", "Preis"])

    #Cleaning
    df.iloc[58] = df.iloc[58].replace(to_replace = 10, value=60)
    df.iloc[58] = df.iloc[58].replace(to_replace = "The Only One  50 ml & Mini", value="The Only One Set")

    #Delete multiple's (first 24 parfums due to setting up of pages crawling)
    df = df.drop([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23])

    #Calculating price for 100ml
    df["Preis"] = pd.to_numeric(df["Preis"])
    df["ml"] = pd.to_numeric(df["ml"])
    df["Preis pro 100 ml"] = df["Preis"] / df["ml"] * 100

    #filling missing values for title (only happend for one specific parfum)
    df["Title"].fillna("Naomi Campbell", inplace=True)

    #export
    df.to_csv("ottos_meets_panda.csv", encoding="utf-8", index=False, header = True, sep=";")

with open ("ottos.csv") as df:
    calculator(df)