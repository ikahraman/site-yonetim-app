import sys
import os
from datetime import datetime

# --- PATH AYARI ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
# ------------------

import streamlit as st
import db_api

st.set_page_config(page_title="Finans", page_icon="💰")

if 'user' not in st.session_state or st.session_state['user'] is None:
    st.warning("Lütfen giriş yapınız.")
    st.stop()

user_id = st.session_state['user']['id']
# Şimdilik varsayılan firma ID 1 kabul edelim (Süper admin mantığı)
firma_id = 1 

st.header("💰 Finansal İşlemler")

# 1. SİTE SEÇİMİ (Veritabanından Doldur)
df_siteler = db_api.sql_to_dataframe("SELECT id, ad FROM siteler")

if df_siteler.empty:
    st.error("Hiç site tanımlı değil! Önce 'Veri Yönetimi'nden örnek veri basın.")
    st.stop()

site_dict = dict(zip(df_siteler['ad'], df_siteler['id']))
secilen_site_ad = st.selectbox("Site Seçiniz", list(site_dict.keys()))
secilen_site_id = site_dict[secilen_site_ad]

# --- YENİ İŞLEM EKLEME ---
with st.expander("➕ Yeni Gelir/Gider Ekle", expanded=True):
    with st.form("finans_form"):
        col1, col2 = st.columns(2)
        islem_turu = col1.selectbox("İşlem Türü", ["tahsilat", "gider", "borc"])
        tutar = col2.number_input("Tutar (TL)", min_value=0.0, step=100.0)
        aciklama = st.text_input("Açıklama", "Ocak 2025 Aidat")
        
        kaydet = st.form_submit_button("Kaydet")
        
        if kaydet:
            # SQL INSERT SORGUSU
            # daire_id şimdilik 0 (Genel) yapıyoruz, detaylandırılabilir.
            sql = f"""
                INSERT INTO hareketler (firma_id, site_id, daire_id, tur, aciklama, tutar, kaydeden_user_id)
                VALUES ({firma_id}, {secilen_site_id}, 0, '{islem_turu}', '{aciklama}', {tutar}, {user_id})
            """
            
            success, msg = db_api.execute_sql(sql)
            
            if success:
                st.success("İşlem Başarıyla Kaydedildi!")
                st.rerun() # Listeyi güncelle
            else:
                st.error(f"Kayıt Hatası: {msg}")

# --- GEÇMİŞ LİSTESİ ---
st.subheader(f"{secilen_site_ad} - Hesap Hareketleri")

sql_gecmis = f"SELECT tarih, tur, aciklama, tutar FROM hareketler WHERE site_id = {secilen_site_id} ORDER BY id DESC"
df_gecmis = db_api.sql_to_dataframe(sql_gecmis)

if not df_gecmis.empty:
    st.dataframe(df_gecmis, use_container_width=True)
else:
    st.info("Bu site için kayıt bulunamadı.")