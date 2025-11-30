import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import sys

# Başlangıçta veritabanı URL'si yok
db_url = None
db_token = None
IS_TURSO = False

# 1. Streamlit Secrets kontrolü (Sunucuda mıyız?)
try:
    if st.secrets is not None and "db" in st.secrets:
        db_url = st.secrets["db"]["url"]
        db_token = st.secrets["db"]["token"]
        IS_TURSO = True
except FileNotFoundError:
    pass # Yerel bilgisayardayız, secrets dosyası yok.
except Exception:
    pass

# 2. Bağlantı URL'sini Belirle
if IS_TURSO and db_url:
    # --- TURSO MODU (CLOUD) ---
    print("🌍 Bulut Modu: Turso'ya bağlanılıyor...")
    if db_url.startswith("libsql://"):
        db_url = db_url.replace("libsql://", "")
    
    # URL'yi oluştur
    DATABASE_URL = f"sqlite+libsql://{db_url}/?authToken={db_token}"
    
    # Bağlantı ayarları
    connect_args = {'check_same_thread': False}

else:
    # --- YEREL MOD (WINDOWS/LOCAL) ---
    print("💻 Yerel Mod: yonetim.db kullanılıyor...")
    DATABASE_URL = "sqlite:///yonetim.db"
    connect_args = {"check_same_thread": False}


# 3. Motoru Başlat
try:
    engine = create_engine(DATABASE_URL, connect_args=connect_args)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Tabloları oluştur
    Base.metadata.create_all(bind=engine)
    
except Exception as e:
    # Eğer Turso kütüphanesi yüklü değilse (Localde) hata verebilir, yakalayalım
    if IS_TURSO:
        st.error(f"Turso Bağlantı Hatası: {e}. Yerel dosyaya dönülüyor.")
        # Fallback (Yedeğin yedeği)
        engine = create_engine("sqlite:///yonetim.db", connect_args={"check_same_thread": False})
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base.metadata.create_all(bind=engine)
    else:
        sys.exit(f"Veritabanı Hatası: {e}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()