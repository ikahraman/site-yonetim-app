import sys
import os

# --- PATH AYARI (Hata almamak için) ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
# --------------------------------------

import streamlit as st
import db_api
import pandas as pd

st.set_page_config(page_title="Genel Bakış", page_icon="🏠")

# Giriş Kontrolü
if 'user' not in st.session_state or st.session_state['user'] is None:
    st.warning("Lütfen önce giriş yapınız.")
    st.stop()

st.header("📊 Genel Durum Özeti")

# --- VERİLERİ TURSO'DAN ÇEK ---
# 1. Site Sayısı
df_siteler = db_api.sql_to_dataframe("SELECT COUNT(*) as sayi FROM siteler")
toplam_site = df_siteler.iloc[0]['sayi'] if not df_siteler.empty else 0

# 2. Finansal Durum (Gelir - Gider)
df_finans = db_api.sql_to_dataframe("SELECT tur, SUM(tutar) as toplam FROM hareketler GROUP BY tur")

toplam_tahsilat = 0
toplam_gider = 0

if not df_finans.empty:
    try:
        # Tutar sütununu sayıya çevir (garanti olsun)
        df_finans['toplam'] = pd.to_numeric(df_finans['toplam'])
        
        # Filtrele
        tahsilat_row = df_finans[df_finans['tur'] == 'tahsilat']
        gider_row = df_finans[df_finans['tur'] == 'gider']
        
        if not tahsilat_row.empty: toplam_tahsilat = tahsilat_row.iloc[0]['toplam']
        if not gider_row.empty: toplam_gider = gider_row.iloc[0]['toplam']
    except:
        pass

kasa_durumu = toplam_tahsilat - toplam_gider

# --- METRİKLERİ GÖSTER ---
col1, col2, col3 = st.columns(3)
col1.metric("Yönetilen Site", f"{toplam_site} Adet")
col2.metric("Toplam Tahsilat", f"{toplam_tahsilat:,.2f} TL")
col3.metric("Net Kasa", f"{kasa_durumu:,.2f} TL", delta_color="normal")

st.divider()

# --- GRAFİK ---
st.subheader("Son Hareketler")
df_hareketler = db_api.sql_to_dataframe("SELECT tarih, aciklama, tur, tutar FROM hareketler ORDER BY id DESC LIMIT 5")
if not df_hareketler.empty:
    st.dataframe(df_hareketler, use_container_width=True)
else:
    st.info("Henüz veri girişi yok.")