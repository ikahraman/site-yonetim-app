import sys
import os

# Ana dizini görmesi için (modül hatasını çözer)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from database import SessionLocal
from models import Site, FinansHareket

st.set_page_config(page_title="Genel Bakış", page_icon="🏠")

if not st.session_state.get('giris_yapildi'):
    st.warning("Lütfen ana sayfadan giriş yapınız.")
    st.stop()

st.header("📊 Genel Durum Özeti")

db = SessionLocal()

# Metrikleri Hesapla
toplam_site = db.query(Site).count()

tum_hareketler = db.query(FinansHareket).all()
toplam_tahsilat = sum([h.tutar for h in tum_hareketler if h.tur == "tahsilat"])
bekleyen_borc = sum([h.tutar for h in tum_hareketler if h.tur == "borc"])

col1, col2, col3 = st.columns(3)
col1.metric("Yönetilen Site", f"{toplam_site} Adet")
col2.metric("Toplam Tahsilat", f"{toplam_tahsilat:,.0f} TL")
col3.metric("Bekleyen Alacak", f"{bekleyen_borc:,.0f} TL", delta_color="inverse")

st.divider()

st.subheader("Finansal Hareket Grafiği")
if tum_hareketler:
    df = pd.DataFrame([h.__dict__ for h in tum_hareketler])
    st.bar_chart(df, x="tarih", y="tutar", color="tur")
else:
    st.info("Henüz veri girişi yapılmamış. 'Ayarlar' menüsünden demo veri yükleyebilirsiniz.")

db.close()