import sys
import os
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import streamlit as st
import db_api

st.set_page_config(page_title="Genel Bakış", page_icon="🏠")

# 1. GÜVENLİK KONTROLÜ
if 'user' not in st.session_state or st.session_state['user'] is None:
    st.warning("Lütfen giriş yapınız.")
    st.stop()

user = st.session_state['user']

# 2. İZOLASYON FİLTRESİ (SİHİRLİ KISIM)
# Bu fonksiyon, adminse "1=1", firmaysa "firma_id=5" gibi bir metin döndürür.
filtre = db_api.get_firma_filter(user)

st.header(f"📊 Genel Durum ({user['rol'].upper()})")

if user['rol'] == 'super_admin':
    st.info("🌍 Süper Admin Modu: Sistemdeki tüm firmaların verilerini görüyorsunuz.")

# --- VERİLERİ TURSO'DAN ÇEK (FİLTRELİ) ---

# A. Site Sayısı
# SQL: SELECT COUNT(*) FROM siteler WHERE firma_id = 5
df_siteler = db_api.sql_to_dataframe(f"SELECT COUNT(*) as sayi FROM siteler WHERE {filtre}")
toplam_site = df_siteler.iloc[0]['sayi'] if not df_siteler.empty else 0

# B. Finansal Durum
# SQL: SELECT tur, SUM(tutar) FROM hareketler WHERE firma_id = 5 GROUP BY tur
df_finans = db_api.sql_to_dataframe(f"SELECT tur, SUM(tutar) as toplam FROM hareketler WHERE {filtre} GROUP BY tur")

toplam_tahsilat = 0
toplam_gider = 0

if not df_finans.empty:
    try:
        df_finans['toplam'] = pd.to_numeric(df_finans['toplam'])
        tahsilat_row = df_finans[df_finans['tur'] == 'tahsilat']
        gider_row = df_finans[df_finans['tur'] == 'gider']
        
        if not tahsilat_row.empty: toplam_tahsilat = tahsilat_row.iloc[0]['toplam']
        if not gider_row.empty: toplam_gider = gider_row.iloc[0]['toplam']
    except:
        pass

kasa_durumu = toplam_tahsilat - toplam_gider

# --- METRİKLER ---
col1, col2, col3 = st.columns(3)
col1.metric("Yönetilen Site", f"{toplam_site} Adet")
col2.metric("Toplam Tahsilat", f"{toplam_tahsilat:,.2f} TL")
col3.metric("Net Kasa", f"{kasa_durumu:,.2f} TL")

st.divider()

# --- GRAFİK (Sadece kendi verileri) ---
st.subheader("Son Hareketler")
sql_hareket = f"SELECT tarih, aciklama, tur, tutar FROM hareketler WHERE {filtre} ORDER BY id DESC LIMIT 5"
df_hareketler = db_api.sql_to_dataframe(sql_hareket)

if not df_hareketler.empty:
    st.dataframe(df_hareketler, use_container_width=True)
else:
    st.info("Henüz veri girişi yok.")