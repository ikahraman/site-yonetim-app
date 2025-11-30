import sys
import os
import pandas as pd

# --- PATH AYARI ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
# ------------------

import streamlit as st
import db_api

st.set_page_config(page_title="Veri Yönetimi", page_icon="💾")

st.header("💾 Sistem Veritabanı Yönetimi")
st.info("Bu panel teknik bakım ve test verisi oluşturmak içindir.")

# --- SEKME YAPISI ---
tab1, tab2, tab3 = st.tabs(["🏗️ Tablo & Veri Sıfırlama", "👀 Veri İncele", "⚡ SQL Konsolu"])

# ---------------------------------------------------------
# SEKME 1: KURULUM VE VERİ BASMA
# ---------------------------------------------------------
with tab1:
    st.subheader("⚠️ Tehlikeli Bölge")
    
    # 1. GÜVENLİK KİLİDİ
    onay = st.checkbox("Riskleri kabul ediyorum ve veritabanı işlemi yapmak istiyorum.")
    
    if onay:
        col1, col2 = st.columns(2)
        
        # BUTON A: TABLOLARI SIFIRLA
        with col1:
            if st.button("♻️ Tabloları SIFIRLA (Her Şeyi Sil)", type="primary"):
                with st.spinner("Tüm veriler siliniyor ve tablolar yeniden kuruluyor..."):
                    # Önce Eskileri Sil
                    tables = ["hareketler", "sakinler", "daireler", "siteler", "kullanicilar", "firmalar"]
                    for t in tables:
                        db_api.execute_sql(f"DROP TABLE IF EXISTS {t}")
                    
                    # Yeni SaaS Şemasını Kur
                    queries = [
                        "CREATE TABLE firmalar (id INTEGER PRIMARY KEY AUTOINCREMENT, ad TEXT NOT NULL, abonelik_durumu TEXT DEFAULT 'aktif')",
                        "CREATE TABLE kullanicilar (id INTEGER PRIMARY KEY AUTOINCREMENT, firma_id INTEGER, email TEXT, sifre TEXT, ad_soyad TEXT, rol TEXT, FOREIGN KEY(firma_id) REFERENCES firmalar(id))",
                        "CREATE TABLE siteler (id INTEGER PRIMARY KEY AUTOINCREMENT, firma_id INTEGER, ad TEXT, adres TEXT, bakiye REAL DEFAULT 0)",
                        "CREATE TABLE daireler (id INTEGER PRIMARY KEY AUTOINCREMENT, firma_id INTEGER, site_id INTEGER, blok TEXT, kapi_no TEXT, tip TEXT)",
                        "CREATE TABLE sakinler (id INTEGER PRIMARY KEY AUTOINCREMENT, firma_id INTEGER, daire_id INTEGER, ad_soyad TEXT, telefon TEXT, tip TEXT)",
                        "CREATE TABLE hareketler (id INTEGER PRIMARY KEY AUTOINCREMENT, firma_id INTEGER, site_id INTEGER, daire_id INTEGER, tarih DATETIME DEFAULT CURRENT_TIMESTAMP, tur TEXT, aciklama TEXT, tutar REAL, kaydeden_user_id INTEGER)"
                    ]
                    
                    for sql in queries:
                        db_api.execute_sql(sql)
                        
                    # Admin ve Firma Ekle
                    db_api.execute_sql("INSERT INTO firmalar (ad) VALUES ('Demo Yönetim A.Ş.')")
                    db_api.execute_sql("INSERT INTO kullanicilar (firma_id, email, sifre, ad_soyad, rol) VALUES (1, 'admin@sistem.com', 'admin123', 'Sistem Yöneticisi', 'super_admin')")
                    
                    st.success("✅ Veritabanı sıfırlandı! Admin kullanıcısı oluşturuldu.")

        # BUTON B: ÖRNEK VERİ BAS
        with col2:
            if st.button("🎲 Örnek Veri Doldur"):
                with st.spinner("Siteler ve daireler oluşturuluyor..."):
                    # 1. Firma ID'sini al (İlk firma)
                    firma_id = 1
                    
                    # 2. Örnek SQL'ler
                    sqls = [
                        # Siteler
                        f"INSERT INTO siteler (firma_id, ad, adres) VALUES ({firma_id}, 'Papatya Sitesi', 'İstanbul')",
                        f"INSERT INTO siteler (firma_id, ad, adres) VALUES ({firma_id}, 'Mavi Bloklar', 'Ankara')",
                        
                        # Daireler (Site 1 için)
                        f"INSERT INTO daireler (firma_id, site_id, blok, kapi_no) VALUES ({firma_id}, 1, 'A', '1')",
                        f"INSERT INTO daireler (firma_id, site_id, blok, kapi_no) VALUES ({firma_id}, 1, 'A', '2')",
                        f"INSERT INTO daireler (firma_id, site_id, blok, kapi_no) VALUES ({firma_id}, 1, 'B', '5')",
                        
                        # Sakinler
                        f"INSERT INTO sakinler (firma_id, daire_id, ad_soyad, tip) VALUES ({firma_id}, 1, 'Ahmet Yılmaz', 'Malik')",
                        f"INSERT INTO sakinler (firma_id, daire_id, ad_soyad, tip) VALUES ({firma_id}, 2, 'Ayşe Demir', 'Kiracı')",
                        
                        # Hareketler
                        f"INSERT INTO hareketler (firma_id, site_id, daire_id, tur, tutar, aciklama) VALUES ({firma_id}, 1, 1, 'borc', 1500, 'Ocak Aidat')",
                        f"INSERT INTO hareketler (firma_id, site_id, daire_id, tur, tutar, aciklama) VALUES ({firma_id}, 1, 0, 'gider', 5000, 'Asansör Bakımı')"
                    ]
                    
                    basarili = 0
                    for sql in sqls:
                        success, _ = db_api.execute_sql(sql)
                        if success: basarili += 1
                        
                    st.success(f"✅ {basarili} adet örnek kayıt eklendi!")
    else:
        st.warning("⚠️ İşlem yapmak için yukarıdaki onay kutusunu işaretleyin.")

# ---------------------------------------------------------
# SEKME 2: VERİ İZLEME
# ---------------------------------------------------------
with tab2:
    st.subheader("Tablo İçerikleri")
    
    # Tüm tabloları listele
    tablo_sec = st.selectbox("Tablo Seç", ["firmalar", "kullanicilar", "siteler", "daireler", "sakinler", "hareketler"])
    
    if st.button("Verileri Getir"):
        with st.spinner("Turso'dan veri çekiliyor..."):
            df = db_api.sql_to_dataframe(f"SELECT * FROM {tablo_sec}")
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                st.caption(f"Toplam {len(df)} kayıt.")
            else:
                st.info("Bu tabloda veri yok.")

# ---------------------------------------------------------
# SEKME 3: SQL KONSOLU
# ---------------------------------------------------------
with tab3:
    st.subheader("SQL Konsolu")
    st.caption("Doğrudan SQL sorgusu çalıştırabilirsiniz.")
    
    sql_command = st.text_area("SQL Sorgusu", "SELECT * FROM siteler")
    
    if st.button("Çalıştır"):
        if "SELECT" in sql_command.upper():
            df = db_api.sql_to_dataframe(sql_command)
            st.dataframe(df)
        else:
            success, msg = db_api.execute_sql(sql_command)
            if success:
                st.success(f"İşlem Başarılı! Mesaj: {msg}")
            else:
                st.error(f"Hata: {msg}")