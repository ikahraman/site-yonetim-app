import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="Site Yönetim MVP", page_icon="🏢", layout="wide")

st.title("🏢 Profesyonel Site Yönetim Paneli")

# Basit Oturum Yönetimi (Session State)
if 'giris_yapildi' not in st.session_state:
    st.session_state['giris_yapildi'] = False

if not st.session_state['giris_yapildi']:
    st.info("Lütfen sisteme giriş yapın. (Demo Şifre: admin)")
    sifre = st.text_input("Şifre", type="password")
    
    if st.button("Giriş Yap"):
        if sifre == "admin":
            st.session_state['giris_yapildi'] = True
            st.success("Giriş Başarılı! Yan menüden işlemlere başlayabilirsiniz.")
            st.rerun()
        else:
            st.error("Hatalı şifre!")
else:
    st.write("### Hoş Geldiniz!")
    st.write("Sol taraftaki menüden yapmak istediğiniz işlemi seçin.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("💡 **İpucu:** Önce 'Siteler' menüsünden bir site ekleyerek başlayın.")
    with col2:
        if st.button("Çıkış Yap"):
            st.session_state['giris_yapildi'] = False
            st.rerun()