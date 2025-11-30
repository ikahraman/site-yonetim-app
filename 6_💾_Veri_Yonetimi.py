
import sys
import os

# Bu 2 satır, Python'un ana klasördeki dosyaları (db_api.py) görmesini sağlar
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import streamlit as st
import db_api # Az önce oluşturduğumuz dosya

st.set_page_config(page_title="Veri Yönetimi", page_icon="💾")

st.header("💾 Veritabanı Yönetimi (HTTP API)")

# --- SEKME 1: TABLOLARI OLUŞTUR ---
tab1, tab2, tab3 = st.tabs(["🏗️ Kurulum", "👀 Veri İzle", "⚡ SQL Çalıştır"])

with tab1:
    st.subheader("Tablo Kurulumu")
    st.write("Bu buton veritabanındaki tabloları sıfırdan oluşturur (Yoksa).")
    
    if st.button("Tabloları Oluştur (Site Yönetimi)"):
        queries = [
            # 1. Siteler Tablosu
            """CREATE TABLE IF NOT EXISTS siteler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ad TEXT NOT NULL,
                adres TEXT
            )""",
            
            # 2. Daireler Tablosu
            """CREATE TABLE IF NOT EXISTS daireler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site_id INTEGER,
                blok TEXT,
                kapi_no TEXT,
                FOREIGN KEY(site_id) REFERENCES siteler(id)
            )""",
            
            # 3. Sakinler Tablosu
            """CREATE TABLE IF NOT EXISTS sakinler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                daire_id INTEGER,
                ad_soyad TEXT,
                telefon TEXT,
                tip TEXT,
                FOREIGN KEY(daire_id) REFERENCES daireler(id)
            )""",
            
            # 4. Hareketler (Finans) Tablosu
            """CREATE TABLE IF NOT EXISTS hareketler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site_id INTEGER,
                daire_id INTEGER,
                tarih DATETIME DEFAULT CURRENT_TIMESTAMP,
                tur TEXT,
                aciklama TEXT,
                tutar REAL
            )"""
        ]
        
        progress_text = "Tablolar oluşturuluyor..."
        my_bar = st.progress(0, text=progress_text)
        
        for i, sql in enumerate(queries):
            success, msg = db_api.execute_sql(sql)
            if not success:
                st.error(f"Hata: {msg}")
            my_bar.progress((i + 1) / len(queries), text=progress_text)
            
        st.success("Tüm tablolar başarıyla oluşturuldu!")
        
    st.divider()
    
    st.subheader("Örnek Veri Ekle")
    if st.button("Rastgele Veri Bas"):
        # Önce basit bir insert deneyelim
        sqls = [
            "INSERT INTO siteler (ad, adres) VALUES ('Güneş Sitesi', 'İstanbul')",
            "INSERT INTO siteler (ad, adres) VALUES ('Deniz Apt', 'İzmir')",
            "INSERT INTO daireler (site_id, blok, kapi_no) VALUES (1, 'A', '1')",
            "INSERT INTO daireler (site_id, blok, kapi_no) VALUES (1, 'A', '2')",
            "INSERT INTO sakinler (daire_id, ad_soyad, tip) VALUES (1, 'Ahmet Yılmaz', 'Malik')",
            "INSERT INTO hareketler (site_id, daire_id, tur, tutar, aciklama) VALUES (1, 1, 'borc', 1000, 'Ocak Aidat')"
        ]
        
        for sql in sqls:
            db_api.execute_sql(sql)
        st.success("Örnek veriler eklendi!")

# --- SEKME 2: VERİLERİ İZLE ---
with tab2:
    st.subheader("Tablo İçerikleri")
    
    tablo_sec = st.selectbox("Tablo Seç", ["siteler", "daireler", "sakinler", "hareketler"])
    
    if st.button("Verileri Getir"):
        df = db_api.sql_to_dataframe(f"SELECT * FROM {tablo_sec}")
        if not df.empty:
            st.dataframe(df)
        else:
            st.info("Bu tabloda veri yok.")

# --- SEKME 3: MANUEL SQL ---
with tab3:
    st.subheader("SQL Konsolu")
    sql_command = st.text_area("SQL Sorgusu Yaz", "SELECT * FROM siteler")
    
    if st.button("Çalıştır"):
        if "SELECT" in sql_command.upper():
            df = db_api.sql_to_dataframe(sql_command)
            st.dataframe(df)
        else:
            success, msg = db_api.execute_sql(sql_command)
            if success:
                st.success(f"İşlem Başarılı! Yanıt: {msg}")
            else:
                st.error(msg)