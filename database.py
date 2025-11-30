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
    # URL Temizliği
    if db_url.startswith("libsql://"):
        db_url = db_url.replace("libsql://", "")
    elif db_url.startswith("https://"):
        db_url = db_url.replace("https://", "")
    
    # URL Oluşturma
    DATABASE_URL = f"sqlite+libsql://{db_url}/?authToken={db_token}"
    connect_args = {'check_same_thread': False}
    
    # ⚠️ KRİTİK DEĞİŞİKLİK: Fallback (Yedek) mekanizmasını kaldırdık.
    # Turso'da hata varsa direkt patlasın ki görelim.
    try:
        engine = create_engine(DATABASE_URL, connect_args=connect_args)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base.metadata.create_all(bind=engine)
        print("✅ Turso bağlantısı başarılı!")
    except Exception as e:
        # Hatayı Streamlit ekranına bas
        st.error(f"🚨 TURSO BAĞLANTI HATASI: {e}")
        st.stop() # Uygulamayı durdur

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