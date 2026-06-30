import os
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, BigInteger

DATABASE_URL = "sqlite+aiosqlite:///efc_database.db"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

# Foydalanuvchilar jadvali
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String, nullable=True)
    som_balance = Column(Float, default=0.0) # So'm hamyon
    efc_balance = Column(Float, default=0.0) # EFC coin
    coin_balance = Column(Integer, default=0) # Oddiy coin
    total_spins = Column(Integer, default=0) # Foydalanuvchining aylantirishlar soni

# Balans to'ldirish buyurtmalari
class DepositOrder(Base):
    __tablename__ = 'deposit_orders'
    id = Column(Integer, primary_key=True, autoincrement=True) # Tartibli raqam
    user_telegram_id = Column(BigInteger, nullable=False)
    username = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    file_id = Column(String, nullable=False) # Chek rasmi IDsi
    status = Column(String, default="pending") # pending, approved, rejected

# Global sozlamalar (Omad g'ildiragi hisoblagichi uchun)
class GlobalSetting(Base):
    __tablename__ = 'global_settings'
    key = Column(String, primary_key=True)
    value = Column(Integer, default=0)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Global hisoblagichni noldan yaratib qo'yamiz
    async with async_session() as session:
        async with session.begin():
            res = await session.get(GlobalSetting, "wheel_counter")
            if not res:
                session.add(GlobalSetting(key="wheel_counter", value=0))
        await session.commit()
      
