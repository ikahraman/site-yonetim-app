import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from database import SessionLocal
from models import Sakin, Daire, Site

st.set_page_config(page_title="Sakinler Listesi", page_icon="👥")

if not st.session_state.get('giris_yapildi'):
    st.warning("Lütfen giriş yapınız.")
    st.stop()

st.header("👥 Site Sakinleri Listesi")

db = SessionLocal()

siteler = db.query(Site).all()
site_listesi = {s.ad: s.id for s in siteler}

secilen_site_ad = st.selectbox("Hangi Sitenin Sakinleri?", list(site_listesi.keys()))

if secilen_site_ad:
    site_id = site_listesi[secilen_site_ad]
    
    sorgu = db.query(
        Daire.blok,
        Daire.kapi_no,
        Sakin.ad_soyad,
        Sakin.telefon,
        Sakin.tip
    ).join(Daire).filter(Daire.site_id == site_id).all()
    
    if sorgu:
        df = pd.DataFrame(sorgu, columns=["Blok", "Kapı No", "Ad Soyad", "Telefon", "Tipi"])
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption(f"Toplam {len(df)} kişi listelendi.")
    else:
        st.warning("Kayıt bulunamadı.")

db.close()