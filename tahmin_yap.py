import pandas as pd
import joblib

ilce = input("İlçe : ").lower()

try:
    model = joblib.load(f"models/model_{ilce}.pkl")
except:
    print("Bu ilçe için model yok.")
    exit()

gross = float(input("Brüt m²: "))
net = float(input("Net m²: "))
age = int(input("Bina yaşı: "))
floors = int(input("Binadaki kat sayısı: "))
rooms = int(input("Oda sayısı (sayı): "))
floor_loc = int(input("Bulunduğu kat: "))
credit = int(input("Krediye uygun mu? (1 evet / 0 hayır): "))

# Bu 3 yeni kolon otomatik hesaplanacak
net_brut = net / gross
fiyat_m2_brut = 0
fiyat_m2_net  = 0

df_input = pd.DataFrame({
    "GrossSquareMeters":[gross],
    "BuildingAge":[age],
    "NumberFloorsofBuilding":[floors],
    "NumberOfRooms":[rooms],
    "FloorLocation":[floor_loc],
    "CreditEligibility":[credit],
    "NetSquareMeters":[net],
    "Net_Brut_Oran":[net_brut],
    "Fiyat_m2_Brut":[fiyat_m2_brut],
    "Fiyat_m2_Net":[fiyat_m2_net]
})

pred = model.predict(df_input)[0]
print(f"Tahmini fiyat: {pred:,.0f} TL")
