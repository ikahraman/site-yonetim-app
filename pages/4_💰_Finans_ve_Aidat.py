import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from database import SessionLocal
from models import Site, FinansHareket

st.set_page_config(page_title="Finans", page_icon="💰")

if not st.session_state.get('giris_yapildi'):
    st.warning("Lütfen giriş yapınız.")
    st.stop()

db = SessionLocal()

st.header("💰 Finansal İşlemler")

siteler = db.query(Site).all()
site_isimleri = {site.ad: site.id for site in siteler}
secilen_site_ad = st.selectbox("Site Seçiniz", list(site_isimleri.keys()))

if secilen_site_ad:
    secilen_site_id = site_isimleri[secilen_site_ad]

    # --- YENİ İŞLEM EKLEME ---
    with st.expander("➕ Yeni Finansal İşlem Ekle"):
        with st.form("finans_form"):
            col1, col2 = st.columns(2)
            islem_turu = col1.selectbox("İşlem Türü", ["borc", "tahsilat", "gider"])
            tutar = col2.number_input("Tutar (TL)", min_value=0.0, step=100.0)
            aciklama = st.text_input("Açıklama", "Ocak 2025 Aidat")
            
            kaydet = st.form_submit_button("Kaydet")
            
            if kaydet:
                yeni_hareket = FinansHareket(
                    site_id=secilen_site_id,
                    tur=islem_turu,
                    tutar=tutar,
                    aciklama=aciklama,
                    tarih=datetime.now()
                )
                db.add(yeni_hareket)
                db.commit()
                st.success("İşlem Başarıyla Kaydedildi!")
                st.rerun()

    # --- HAREKET GEÇMİŞİ ---
    st.subheader(f"{secilen_site_ad} - Hesap Hareketleri")
    
    hareketler = db.query(FinansHareket).filter(FinansHareket.site_id == secilen_site_id).order_by(FinansHareket.tarih.desc()).all()
    
    if hareketler:
        data = []
        for h in hareketler:
            data.append({
                "Tarih": h.tarih,
                "Tür": h.tur,
                "Açıklama": h.aciklama,
                "Tutar": h.tutar
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Bu site için henüz işlem kaydı yok.")

db.close()