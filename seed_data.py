import random
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Site, Daire, Sakin, FinansHareket, HareketTuru

# Türkçe veri üreticisi
fake = Faker('tr_TR')

def veritabani_temizle(db: Session):
    print("🧹 Eski veriler temizleniyor...")
    db.query(FinansHareket).delete()
    db.query(Sakin).delete()
    db.query(Daire).delete()
    db.query(Site).delete()
    db.commit()

def rastgele_tarih_uret(baslangic, bitis):
    delta = bitis - baslangic
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return baslangic + timedelta(seconds=random_second)

def veri_bas(db: Session):
    print("🚀 Veri üretimi başladı... (Bu işlem 10-20 saniye sürebilir)")
    
    # 1. SİTELERİ OLUŞTUR (10 Adet)
    siteler = []
    site_isimleri = [
        "Mavi Çam Sitesi", "Huzur Apartmanı", "Güneş Park Evleri", 
        "Deniz Yıldızı Konutları", "Manzara Towers", "Yeşil Vadi Sitesi",
        "Kardelen Apt.", "Akasya Evleri", "Modern Palas", "Elite Residence"
    ]
    
    for isim in site_isimleri:
        site = Site(
            ad=isim,
            adres=fake.address()
        )
        db.add(site)
        siteler.append(site)
    db.commit()
    print(f"✅ {len(siteler)} adet site oluşturuldu.")

    # 2. DAİRELER VE SAKİNLERİ OLUŞTUR (~400 Adet)
    daireler = []
    bloklar = ["A", "B", "C", "D"]
    
    for site in siteler:
        # Her sitede rastgele 20-50 daire olsun
        daire_sayisi = random.randint(20, 50)
        aidat_tutari = random.choice([500, 750, 1000, 1500]) # Siteye özel aidat
        
        for i in range(1, daire_sayisi + 1):
            blok = random.choice(bloklar)
            kapi_no = str(i)
            
            daire = Daire(
                site_id=site.id,
                blok=blok,
                kapi_no=kapi_no
            )
            db.add(daire)
            db.flush() # ID almak için flush
            daireler.append((daire, aidat_tutari)) # Aidat bilgisini tuple olarak tut
            
            # Daireye Sakin Ata
            sakin = Sakin(
                daire_id=daire.id,
                ad_soyad=fake.name(),
                telefon=fake.phone_number(),
                tip=random.choice(["Malik", "Kiracı", "Malik"]) # Malik ağırlıklı
            )
            db.add(sakin)
            
    db.commit()
    print(f"✅ {len(daireler)} adet daire ve sakin oluşturuldu.")

    # 3. FİNANSAL GEÇMİŞ OLUŞTUR (Son 1 Yıl)
    print("💸 Finansal işlemler (Borç/Tahsilat) üretiliyor...")
    
    bugun = datetime.now()
    gecmis_bir_yil = bugun - timedelta(days=365)
    
    hareket_sayaci = 0
    
    # Her ay için döngü
    for ay in range(12):
        islem_ayi = gecmis_bir_yil + timedelta(days=ay*30)
        ay_adi = islem_ayi.strftime("%B %Y")
        
        for daire, aidat in daireler:
            # A) HER AY HERKESE BORÇ YAZ (AİDAT TAHAKKUKU)
            borc = FinansHareket(
                site_id=daire.site_id,
                tutar=aidat,
                tur="borc",
                aciklama=f"{ay_adi} Aidat Tahakkuku",
                tarih=islem_ayi.replace(day=1) # Ayın 1'inde borç yazılır
            )
            db.add(borc)
            hareket_sayaci += 1
            
            # B) SAKİNLERİN %80'i ÖDEME YAPSIN (TAHSILAT)
            if random.random() > 0.2: 
                # Bazen tam öder, bazen eksik, bazen geç
                odeme_tarihi = rastgele_tarih_uret(islem_ayi, islem_ayi + timedelta(days=25))
                tahsilat = FinansHareket(
                    site_id=daire.site_id,
                    tutar=aidat, # Düzenli ödeyenler
                    tur="tahsilat",
                    aciklama=f"{ay_adi} Aidat Ödemesi",
                    tarih=odeme_tarihi
                )
                db.add(tahsilat)
                hareket_sayaci += 1
        
        # C) HER SİTEYE RASTGELE GİDERLER EKLE (Elektrik, Su, Temizlik)
        for site in siteler:
            for _ in range(random.randint(1, 3)):
                gider_tutari = random.uniform(1000, 5000)
                gider = FinansHareket(
                    site_id=site.id,
                    tutar=gider_tutari,
                    tur="gider",
                    aciklama=f"{random.choice(['ASAT Su Faturası', 'CK Enerji Elektrik', 'Temizlik Malzemesi', 'Asansör Bakımı'])} - {ay_adi}",
                    tarih=islem_ayi.replace(day=random.randint(5, 25))
                )
                db.add(gider)
                hareket_sayaci += 1
                
    db.commit()
    print(f"✅ Toplam {hareket_sayaci} adet finansal işlem kaydı girildi.")
    print("🏁 İŞLEM TAMAMLANDI! `streamlit run main.py` komutuyla uygulamayı başlatabilirsiniz.")

if __name__ == "__main__":
    db = SessionLocal()
    # Tabloları oluştur (Eğer yoksa)
    Base.metadata.create_all(bind=engine)
    
    # Temizle ve Doldur
    veritabani_temizle(db)
    veri_bas(db)
    db.close()