from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import enum

Base = declarative_base()

class HareketTuru(str, enum.Enum):
    BORC = "borc"      # Aidat Tahakkuku
    TAHSILAT = "tahsilat"  # Ödeme Alma
    GIDER = "gider"     # Elektrik faturası vb.

class Site(Base):
    __tablename__ = 'siteler'
    id = Column(Integer, primary_key=True, index=True)
    ad = Column(String, nullable=False)
    adres = Column(String)
    # İlişkiler
    daireler = relationship("Daire", back_populates="site")
    hareketler = relationship("FinansHareket", back_populates="site")

class Daire(Base):
    __tablename__ = 'daireler'
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey('siteler.id'))
    blok = Column(String)
    kapi_no = Column(String)
    
    site = relationship("Site", back_populates="daireler")
    sakinler = relationship("Sakin", back_populates="daire")

class Sakin(Base):
    __tablename__ = 'sakinler'
    id = Column(Integer, primary_key=True, index=True)
    daire_id = Column(Integer, ForeignKey('daireler.id'))
    ad_soyad = Column(String)
    telefon = Column(String)
    tip = Column(String) # Malik / Kiracı
    
    daire = relationship("Daire", back_populates="sakinler")

class FinansHareket(Base):
    __tablename__ = 'hareketler'
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey('siteler.id'))
    tutar = Column(Float, nullable=False)
    tur = Column(String) # borc, tahsilat, gider
    aciklama = Column(String)
    tarih = Column(DateTime, default=datetime.utcnow)
    
    site = relationship("Site", back_populates="hareketler")