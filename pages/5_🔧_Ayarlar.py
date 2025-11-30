import sys
import os

# --- PATH AYARI (db_api'yi bulmak için) ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
# ------------------------------------------

import streamlit as st
import db_api  # Yeni motorumuz

st.set_page_config(page_title="Ayarlar", page_icon="🔧")

# Giriş Kontrolü
if 'user' not in st.session_state or st.session_state['user'] is None:
    st.warning("Lütfen giriş yapınız.")
    st.stop()

user = st.session_state['user']

st.header("🔧 Ayarlar ve Profil")

# Sekmeler
tab1, tab2 = st.tabs(["👤 Profil Ayarları", "📡 Sistem Durumu"])

# ---------------------------------------------------------
# SEKME 1: PROFİL GÜNCELLEME
# ---------------------------------------------------------
with tab1:
    st.subheader("Bilgilerimi Güncelle")
    
    with st.form("profil_form"):
        yeni_ad = st.text_input("Ad Soyad", value=user.get('ad_soyad', ''))
        yeni_email = st.text_input("E-Posta", value=user.get('email', ''), disabled=True) # Email değişmesin
        yeni_sifre = st.text_input("Yeni Şifre (Değiştirmek istemiyorsanız boş bırakın)", type="password")
        
        btn_guncelle = st.form_submit_button("Bilgileri Kaydet")
        
        if btn_guncelle:
            # SQL Hazırla
            if yeni_sifre:
                sql = f"UPDATE kullanicilar SET ad_soyad = '{yeni_ad}', sifre = '{yeni_sifre}' WHERE id = {user['id']}"
            else:
                sql = f"UPDATE kullanicilar SET ad_soyad = '{yeni_ad}' WHERE id = {user['id']}"
            
            # Gönder
            success, msg = db_api.execute_sql(sql)
            
            if success:
                st.success("Profiliniz başarıyla güncellendi! Lütfen tekrar giriş yapın.")
                # Session'ı güncelle
                st.session_state['user']['ad_soyad'] = yeni_ad
            else:
                st.error(f"Güncelleme hatası: {msg}")

# ---------------------------------------------------------
# SEKME 2: SİSTEM BAĞLANTISI
# ---------------------------------------------------------
with tab2:
    st.subheader("Veritabanı Bağlantı Durumu")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"🔑 Kullanıcı ID: {user['id']}")
        st.info(f"🏢 Firma ID: {user.get('firma_id', 'Süper Admin')}")
        
    with col2:
        # Turso Testi
        if st.button("Bağlantıyı Test Et"):
            with st.spinner("Turso'ya ping atılıyor..."):
                success, response = db_api.execute_sql("SELECT 1")
                if success:
                    st.success("🟢 BAĞLANTI BAŞARILI (Online)")
                    st.json(response)
                else:
                    st.error("🔴 BAĞLANTI HATASI")
                    st.error(response)

    st.divider()
    st.caption("Bu uygulama Turso Cloud Veritabanı (HTTP API) kullanmaktadır.")