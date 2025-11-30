import sys
import os
import pandas as pd

# --- PATH AYARI (Motoru bulmak için şart) ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
# ------------------------------------------

import streamlit as st
import db_api  # <--- ARTIK YENİ MOTORU KULLANIYORUZ

st.set_page_config(page_title="Siteler ve Daireler", page_icon="🏢")

# Giriş Kontrolü
if 'user' not in st.session_state or st.session_state['user'] is None:
    st.warning("Lütfen giriş yapınız.")
    st.stop()

st.header("🏢 Site ve Daire Yönetimi")

# 1. Site Seçimi
df_siteler = db_api.sql_to_dataframe("SELECT id, ad FROM siteler")

if df_siteler.empty:
    st.warning("Henüz hiç site yok. 'Veri Yönetimi' sayfasından örnek veri ekleyebilirsiniz.")
    st.stop()

site_dict = dict(zip(df_siteler['ad'], df_siteler['id']))
secilen_site_ad = st.selectbox("İncelemek İstediğiniz Siteyi Seçin:", list(site_dict.keys()))

if secilen_site_ad:
    site_id = site_dict[secilen_site_ad]
    
    # İstatistikler
    df_daire_sayi = db_api.sql_to_dataframe(f"SELECT COUNT(*) as sayi FROM daireler WHERE site_id = {site_id}")
    daire_sayisi = df_daire_sayi.iloc[0]['sayi'] if not df_daire_sayi.empty else 0
    
    df_sakin_sayi = db_api.sql_to_dataframe(f"SELECT COUNT(*) as sayi FROM sakinler s JOIN daireler d ON s.daire_id = d.id WHERE d.site_id = {site_id}")
    sakin_sayisi = df_sakin_sayi.iloc[0]['sayi'] if not df_sakin_sayi.empty else 0
    
    col1, col2 = st.columns(2)
    col1.info(f"Toplam Daire: **{daire_sayisi}**")
    col2.info(f"Kayıtlı Sakin: **{sakin_sayisi}**")
    
    st.divider()
    
    # 2. Detaylı Liste (JOIN İşlemi)
    # Yeni motor ile SQL sorgusu
    sql = f"""
        SELECT d.blok, d.kapi_no, s.ad_soyad, s.telefon, s.tip
        FROM daireler d
        LEFT JOIN sakinler s ON s.daire_id = d.id
        WHERE d.site_id = {site_id}
        ORDER BY d.blok, d.kapi_no
    """
    
    df_liste = db_api.sql_to_dataframe(sql)
    
    if not df_liste.empty:
        st.dataframe(
            df_liste, 
            use_container_width=True,
            column_config={
                "blok": "Blok",
                "kapi_no": "Kapı No",
                "ad_soyad": "Sakin Adı",
                "telefon": "Telefon",
                "tip": "Durum (Malik/Kiracı)"
            },
            hide_index=True
        )
    else:
        st.info("Bu sitede henüz daire kaydı yok.")