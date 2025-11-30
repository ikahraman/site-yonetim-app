import sys
import os
import pandas as pd

# --- PATH AYARI ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
# ------------------

import streamlit as st
import db_api  # YENİ MOTOR

st.set_page_config(page_title="Sakinler Listesi", page_icon="👥")

if 'user' not in st.session_state or st.session_state['user'] is None:
    st.warning("Lütfen giriş yapınız.")
    st.stop()

st.header("👥 Site Sakinleri Listesi")

# Site Seçimi
df_siteler = db_api.sql_to_dataframe("SELECT id, ad FROM siteler")

if df_siteler.empty:
    st.warning("Kayıtlı site bulunamadı.")
    st.stop()

site_dict = dict(zip(df_siteler['ad'], df_siteler['id']))
secilen_site_ad = st.selectbox("Hangi Sitenin Sakinleri?", list(site_dict.keys()))

if secilen_site_ad:
    site_id = site_dict[secilen_site_ad]
    
    # SQL ile veri çekme
    sql = f"""
        SELECT d.blok, d.kapi_no, s.ad_soyad, s.telefon, s.tip
        FROM sakinler s
        JOIN daireler d ON s.daire_id = d.id
        WHERE d.site_id = {site_id}
    """
    
    df = db_api.sql_to_dataframe(sql)
    
    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption(f"Toplam {len(df)} kişi listelendi.")
    else:
        st.warning("Bu sitede kayıtlı sakin bulunamadı.")