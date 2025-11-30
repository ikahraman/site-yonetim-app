import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from database import SessionLocal
from models import Site, Daire, Sakin

st.set_page_config(page_title="Siteler ve Daireler", page_icon="🏢")

if not st.session_state.get('giris_yapildi'):
    st.warning("Lütfen giriş yapınız.")
    st.stop()

db = SessionLocal()

st.header("🏢 Site ve Daire Yönetimi")

siteler = db.query(Site).all()
site_listesi = {s.ad: s.id for s in siteler}

secilen_site_ad = st.selectbox("İncelemek İstediğiniz Siteyi Seçin:", list(site_listesi.keys()))

if secilen_site_ad:
    site_id = site_listesi[secilen_site_ad]
    
    daire_sayisi = db.query(Daire).filter(Daire.site_id == site_id).count()
    sakin_sayisi = db.query(Sakin).join(Daire).filter(Daire.site_id == site_id).count()
    
    col1, col2 = st.columns(2)
    col1.info(f"Toplam Daire: **{daire_sayisi}**")
    col2.info(f"Kayıtlı Sakin: **{sakin_sayisi}**")
    
    st.divider()
    
    # JOIN ile detaylı veri çekme
    sorgu = db.query(
        Daire.blok, 
        Daire.kapi_no, 
        Sakin.ad_soyad, 
        Sakin.telefon, 
        Sakin.tip
    ).outerjoin(Sakin, Sakin.daire_id == Daire.id)\
     .filter(Daire.site_id == site_id)\
     .order_by(Daire.blok, Daire.kapi_no)\
     .all()
    
    if sorgu:
        df = pd.DataFrame(sorgu, columns=["Blok", "Kapı No", "Ad Soyad", "Telefon", "Durum"])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.warning("Bu sitede veri yok.")

db.close()