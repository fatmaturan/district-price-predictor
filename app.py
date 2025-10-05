import streamlit as st
import pandas as pd
import joblib

st.title("Emlak Fiyat Tahmini (İlçe Bazlı)")

districts = ["adalar","arnavutkoy","atasehir","avcilar","bagcilar",
"bahcelievler","bakirkoy","basaksehir","bayrampasa","besiktas",
"beykoz","beylikduzu","beyoglu","buyukcekmece","catalca",
"cekmekoy","esenler","esenyurt","eyupsultan","fatih",
"gaziosmanpasa","gungoren","kadikoy","kagithane","kartal",
"kucukcekmece","maltepe","pendik","sancaktepe","sariyer",
"sile","silivri","sisli","sultanbeyli","sultangazi",
"tuzla","umraniye","uskudar","zeytinburnu"]

ilce = st.selectbox("İlçe seçiniz:", districts)

gross = st.number_input("Brüt m²", min_value=20, value=100)
net   = st.number_input("Net m²", min_value=10, value=80)
age   = st.number_input("Bina yaşı", min_value=0, value=10)
floors = st.number_input("Binadaki kat sayısı", min_value=1, value=5)
rooms  = st.number_input("Oda sayısı (sayı)", min_value=1, value=3)
floor_loc = st.number_input("Bulunduğu kat", min_value=0, value=2)
credit = st.selectbox("Krediye uygun mu?", [1, 0])

if st.button("Tahmin Et"):
    try:
        model = joblib.load(f"rf_models_optimized/model_{ilce}.pkl")
    except:
        st.error("Model bulunamadı. Önce main.py ile model eğit.")
    else:
        # EK Feature'ları hesapla
        net_bru_ratio = net / gross
        fiyat_m2_brut = 0
        fiyat_m2_net = 0

        df_input = pd.DataFrame({
            "GrossSquareMeters":[gross],
            "BuildingAge":[age],
            "NumberFloorsofBuilding":[floors],
            "NumberOfRooms":[rooms],
            "FloorLocation":[floor_loc],
            "CreditEligibility":[credit],
            "NetSquareMeters":[net],
            "Net_Brut_Oran":[net_bru_ratio],
            "Fiyat_m2_Brut":[fiyat_m2_brut],
            "Fiyat_m2_Net":[fiyat_m2_net]
        })

        price = model.predict(df_input)[0]
        st.success(f"Tahmini Fiyat: {price:,.0f} TL")
