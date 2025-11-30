import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import sys

# Başlangıç değişkenleri
db_url = None
db_token = None
IS_TURSO = False

# 1. Streamlit Secrets kontrolü
try:
    if st.secrets is not None and "db" in st.secrets:
        db_url = st.secrets["db"]["url"]
        db_token = st.secrets["db"]["token"]
        IS_TURSO = True
except FileNotFoundError:
    pass 
except Exception:
    pass

# 2. Bağlantı Mantığı
if IS_TURSO and db_url:
    # --- TURSO MODU ---
    
    # URL Temizliği: 'libsql://' protokolünü tamamen kaldırıp sadece domain'i alıyoruz.
    if "://" in db_url:
        db_url = db_url.split("://")[1]
    
    # URL Oluşturma (Kritik Düzeltme Burası)
    # 1. Protokolü sqlite+libsql yapıyoruz.
    # 2. Domain'i ekliyoruz.
    # 3. Sonuna secure=true ekleyerek 308 hatasını engelliyoruz.
    DATABASE_URL = f"sqlite+libsql://{db_url}/?authToken={db_token}&secure=true"
    
    connect_args = {'check_same_thread': False}
    
    try:
        engine = create_engine(DATABASE_URL, connect_args=connect_args)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base.metadata.create_all(bind=engine)
        print("✅ Turso bağlantısı başarılı!")
    except Exception as e:
        st.error(f"🚨 TURSO BAĞLANTI HATASI: {e}")
        st.info("İpucu: Secrets ayarlarındaki URL'nin başında 'libsql://' olduğundan emin olun.")
        st.stop()

else:
    # --- YEREL MOD ---
    DATABASE_URL = "sqlite:///yonetim.db"
    connect_args = {"check_same_thread": False}
    
    engine = create_engine(DATABASE_URL, connect_args=connect_args)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()