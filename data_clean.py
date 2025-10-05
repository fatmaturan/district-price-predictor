# data_clean.py

import pandas as pd
import numpy as np

# Mapping: sayıdan isme
district_map = {
    0: "adalar",
    1: "arnavutkoy",
    2: "atasehir",
    3: "avcilar",
    4: "bagcilar",
    5: "bahcelievler",
    6: "bakirkoy",
    7: "basaksehir",
    8: "bayrampasa",
    9: "besiktas",
    10: "beykoz",
    11: "beylikduzu",
    12: "beyoglu",
    13: "buyukcekmece",
    14: "catalca",
    15: "cekmekoy",
    16: "esenler",
    17: "esenyurt",
    18: "eyupsultan",
    19: "fatih",
    20: "gaziosmanpasa",
    21: "gungoren",
    22: "kadikoy",
    23: "kagithane",
    24: "kartal",
    25: "kucukcekmece",
    26: "maltepe",
    27: "pendik",
    28: "sancaktepe",
    29: "sariyer",
    30: "sile",
    31: "silivri",
    32: "sisli",
    33: "sultanbeyli",
    34: "sultangazi",
    35: "tuzla",
    36: "umraniye",
    37: "uskudar",
    38: "zeytinburnu"
}

# 1) Veriyi oku (district sayısal hali)
df = pd.read_csv("veri_daire_temiz.csv")

# 2) District'i string hale çevir
df["district"] = df["district"].map(district_map)

# 3) Aykırı fiyat filtrele
df = df[(df["price"] > 100_000) & (df["price"] < 50_000_000)]

# 4) Yeni featurelar
df["Net_Brut_Oran"] = df["NetSquareMeters"] / df["GrossSquareMeters"]
df["Fiyat_m2_Brut"] = df["price"] / df["GrossSquareMeters"]
df["Fiyat_m2_Net"] = df["price"] / df["NetSquareMeters"]

df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(inplace=True)

# 5) Kaydet
df.to_csv("clean_apartments.csv", index=False)
print("Temiz veri kaydedildi 'clean_apartments.csv'")
