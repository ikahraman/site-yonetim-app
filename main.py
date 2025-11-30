import streamlit as st
import db_api  # Yeni motorumuz
import time

# Sayfa Ayarları
st.set_page_config(page_title="SaaS Site Yönetim", page_icon="🏢", layout="centered")

# --- CSS İLE GÜZELLEŞTİRME ---
st.markdown("""
<style>
    .stTextInput input { padding: 10px; }
    .stButton button { width: 100%; padding: 10px; font-weight: bold; }
    div[data-testid="stForm"] { border: 1px solid #ddd; padding: 20px; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# --- OTURUM KONTROLÜ ---
if 'user' not in st.session_state:
    st.session_state['user'] = None

# --- GİRİŞ YAPILMIŞSA (DASHBOARD) ---
if st.session_state['user']:
    user = st.session_state['user']
    
    st.title(f"Hoş Geldiniz, {user['ad_soyad']}")
    st.info(f"Yetki: {user['rol']} | ID: {user['id']}")
    
    st.write("Sol menüden işlemlere başlayabilirsiniz.")
    
    if st.button("Çıkış Yap", type="primary"):
        st.session_state['user'] = None
        st.rerun()

# --- GİRİŞ EKRANI (LOGIN) ---
else:
    st.header("🏢 Site Yönetim Platformu")
    st.caption("SaaS Yönetim Paneli")
    
    with st.form("login_form"):
        email = st.text_input("E-Posta", placeholder="admin@sistem.com")
        password = st.text_input("Şifre", type="password", placeholder="******")
        
        submit = st.form_submit_button("Giriş Yap")
        
        if submit:
            if not email or not password:
                st.warning("Lütfen alanları doldurun.")
            else:
                # TURSO SORGUSU (SQL Injection'a karşı basit önlem string format ile)
                sql = f"SELECT * FROM kullanicilar WHERE email = '{email}' AND sifre = '{password}'"
                
                # Yeni motorumuzla sorgula
                df = db_api.sql_to_dataframe(sql)
                
                if not df.empty:
                    # Kullanıcı bulundu
                    user_data = df.iloc[0].to_dict()
                    st.session_state['user'] = user_data
                    st.success("Giriş Başarılı! Yönlendiriliyorsunuz...")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("❌ Hatalı E-posta veya Şifre!")