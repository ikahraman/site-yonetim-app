import sys
import os

# Ana klasöre erişim izni (Hata almamak için şart)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from database import SessionLocal
# seed_data.py dosyasındaki fonksiyonları çağırıyoruz
from seed_data import veri_bas, veritabani_temizle

st.set_page_config(page_title="Ayarlar", page_icon="🔧")

if not st.session_state.get('giris_yapildi'):
    st.warning("Lütfen ana sayfadan giriş yapınız.")
    st.stop()

st.header("🔧 Sistem Ayarları ve Demo Veri")

st.info("Bu panel geliştirme aşamasında sistemi test etmek için kullanılır.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🗑️ Verileri Temizle")
    st.write("Veritabanındaki tüm site, daire ve finans kayıtlarını kalıcı olarak siler.")
    if st.button("Tüm Verileri Sil", type="primary"):
        db = SessionLocal()
        with st.spinner("Veriler siliniyor..."):
            veritabani_temizle(db)
        st.success("Veritabanı başarıyla temizlendi!")
        db.close()

with col2:
    st.subheader("🎲 Demo Veri Yükle")
    st.write("Sistemi test etmek için rastgele siteler, kişiler ve aidat işlemleri oluşturur.")
    if st.button("Rastgele Veri Üret"):
        db = SessionLocal()
        with st.spinner("Yapay zeka verileri üretiyor... (Bu işlem 15-20 sn sürebilir)"):
            # Önce temizleyelim ki üst üste binmesin
            veritabani_temizle(db) 
            # Sonra yeni veri basalım
            veri_bas(db)
        st.balloons()
        st.success("Harika! Yeni veriler yüklendi. Diğer menülerden kontrol edebilirsiniz.")
        db.close()

st.divider()
st.caption("Not: Bu işlemler geri alınamaz.")