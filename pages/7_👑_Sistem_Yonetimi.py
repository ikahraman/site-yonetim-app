import sys
import os
import pandas as pd

# --- PATH AYARI (Motoru bulmak için) ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
# ------------------------------------------

import streamlit as st
import db_api
import time # Yenileme için kullanılıyor

st.set_page_config(page_title="Sistem Yönetimi", page_icon="👑")

# 1. GÜVENLİK KONTROLÜ (Sadece Süper Admin Girebilir)
if 'user' not in st.session_state or st.session_state['user'] is None:
    st.warning("Lütfen giriş yapınız.")
    st.stop()

user = st.session_state['user']

if user['rol'] != 'super_admin':
    st.error("⛔ YETKİSİZ ERİŞİM! Bu sayfa sadece Sistem Yöneticisi içindir.")
    st.stop()

st.header("👑 SaaS Sistem Yönetimi")
st.info(f"Hoş Geldiniz, {user['ad_soyad']}. Buradan yeni müşteri firmalar tanımlayabilirsiniz.")

tab1, tab2 = st.tabs(["🏢 Firma Yönetimi", "👥 Kullanıcı/Admin Yönetimi"])

# ---------------------------------------------------------
# SEKME 1: FİRMA YÖNETİMİ
# ---------------------------------------------------------
with tab1:
    col1, col2 = st.columns([1, 2])
    
    # A. YENİ FİRMA EKLEME
    with col1:
        st.subheader("Yeni Firma Ekle")
        with st.form("yeni_firma_form"):
            firma_ad = st.text_input("Firma Adı", placeholder="Örn: Ege Yönetim Ltd.")
            yetkili = st.text_input("Yetkili Kişi")
            tel = st.text_input("Telefon")
            
            btn_firma_ekle = st.form_submit_button("Firmayı Oluştur")
            
            if btn_firma_ekle:
                if firma_ad:
                    # SQL: INSERT INTO firmalar
                    sql = f"INSERT INTO firmalar (ad, yetkili_ad, telefon) VALUES ('{firma_ad}', '{yetkili}', '{tel}')"
                    success, msg = db_api.execute_sql(sql)
                    if success:
                        st.success(f"✅ '{firma_ad}' başarıyla oluşturuldu! Sayfa yenileniyor...")
                        # Yenileme: Liste güncellensin
                        time.sleep(0.5) 
                        st.rerun()
                    else:
                        st.error(f"Hata: {msg}")
                else:
                    st.warning("Firma adı boş olamaz.")

    # B. FİRMA LİSTESİ
    with col2:
        st.subheader("Mevcut Müşteri Firmalar")
        # SQL: SELECT * FROM firmalar
        df_firmalar = db_api.sql_to_dataframe("SELECT * FROM firmalar ORDER BY id DESC")
        
        if not df_firmalar.empty:
            st.dataframe(
                df_firmalar, 
                use_container_width=True,
                column_config={
                    "id": "ID",
                    "ad": "Firma Adı",
                    "abonelik_durumu": "Durum",
                    "olusturma_tarihi": "Kayıt Tarihi"
                }
            )
        else:
            st.info("Henüz kayıtlı firma yok.")

# ---------------------------------------------------------
# SEKME 2: KULLANICI / ADMIN YÖNETİMİ
# ---------------------------------------------------------
with tab2:
    st.subheader("Firma Yöneticisi Tanımla")
    
    # Firma Seçimi
    df_firmalar = db_api.sql_to_dataframe("SELECT id, ad FROM firmalar")
    
    if df_firmalar.empty:
        st.warning("Önce firma oluşturmalısınız.")
    else:
        firma_dict = dict(zip(df_firmalar['ad'], df_firmalar['id']))
        secilen_firma_ad = st.selectbox("Hangi Firma İçin Kullanıcı Açılacak?", list(firma_dict.keys()))
        secilen_firma_id = firma_dict[secilen_firma_ad]
        
        with st.form("yeni_admin_form"):
            new_email = st.text_input("E-Posta (Kullanıcı Adı)")
            new_pass = st.text_input("Şifre", type="password")
            new_name = st.text_input("Ad Soyad")
            
            # Rol seçimi (Sadece firma admini veya personel ekleyebilir)
            new_role = st.selectbox("Yetki Seviyesi", ["firma_admin", "personel"])
            
            btn_user_ekle = st.form_submit_button("Kullanıcıyı Oluştur")
            
            if btn_user_ekle:
                if new_email and new_pass:
                    # Email kontrolü (Unique)
                    check = db_api.sql_to_dataframe(f"SELECT id FROM kullanicilar WHERE email = '{new_email}'")
                    if not check.empty:
                        st.error("Bu e-posta adresi zaten kullanılıyor!")
                    else:
                        # SQL: INSERT INTO kullanicilar
                        sql = f"""
                            INSERT INTO kullanicilar (firma_id, email, sifre, ad_soyad, rol) 
                            VALUES ({secilen_firma_id}, '{new_email}', '{new_pass}', '{new_name}', '{new_role}')
                        """
                        success, msg = db_api.execute_sql(sql)
                        if success:
                            st.success(f"✅ Kullanıcı '{new_email}' başarıyla {secilen_firma_ad} firmasına eklendi!")
                        else:
                            st.error(f"Kayıt Hatası: {msg}")
                else:
                    st.warning("E-posta ve şifre zorunludur.")
                    
    st.divider()
    st.subheader("Tüm Sistem Kullanıcıları")
    # Süper Admin dahil tüm kullanıcıları listele
    df_users = db_api.sql_to_dataframe("""
        SELECT k.id, k.ad_soyad, k.email, k.rol, f.ad as firma_adi 
        FROM kullanicilar k 
        LEFT JOIN firmalar f ON k.firma_id = f.id
        ORDER BY k.id DESC
    """)
    st.dataframe(df_users, use_container_width=True)