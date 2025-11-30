import requests
import streamlit as st
import pandas as pd

# 1. Bağlantı Bilgilerini Al (Secrets'tan veya kodun içinden)
try:
    URL = st.secrets["db"]["url"]
    TOKEN = st.secrets["db"]["token"]
except:
    # Eğer secrets yoksa, buraya elle yazdıklarınızı kullanır (Acil durum)
    URL = "libsql://site-yonetim-db-..." 
    TOKEN = "eyJ..."

def execute_sql(sql):
    """
    Turso HTTP API'sine SQL sorgusu gönderir.
    Dönüş: (Başarılı mı?, Sonuç/Hata Mesajı)
    """
    # URL Dönüşümü (libsql -> https)
    http_url = URL.replace('libsql://', 'https://')
    if not http_url.startswith("https://"):
        http_url = f"https://{http_url}"

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "requests": [
            {
                "type": "execute",
                "stmt": { "sql": sql }
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{http_url}/v2/pipeline",
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"HTTP Hatası: {response.status_code} - {response.text}"
            
    except Exception as e:
        return False, f"Bağlantı Hatası: {e}"

def sql_to_dataframe(sql):
    """
    SQL sorgusunu çalıştırır ve sonucu Pandas DataFrame'e çevirir.
    Streamlit tabloları için idealdir.
    """
    success, result = execute_sql(sql)
    
    if not success:
        st.error(result)
        return pd.DataFrame()
    
    try:
        # Turso yanıt yapısını ayrıştır
        # Yanıt yapısı: results[0].response.result.rows ve cols
        base = result['results'][0]['response']['result']
        
        cols = [c['name'] for c in base['cols']]
        rows = []
        
        for row in base['rows']:
            # Turso verileri tipine göre (text, value) döndürür, temizleyelim
            clean_row = []
            for cell in row:
                # Hücre değeri 'value' veya 'text' içinde olabilir
                clean_row.append(cell.get('value') if 'value' in cell else cell.get('text'))
            rows.append(clean_row)
            
        return pd.DataFrame(rows, columns=cols)
        
    except Exception as e:
        # Veri yoksa veya hata varsa boş dön
        return pd.DataFrame()