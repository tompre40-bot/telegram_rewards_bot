import asyncio
from datetime import datetime
from sqlalchemy import (
    create_engine, Column, Integer, BigInteger, String, Boolean,
    Float, DateTime, ForeignKey, Date, Text
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from config import DB_URL  # DB_URL="sqlite:///rewards_bot.db" or PostgreSQL URL

Base = declarative_base()

# ==============================
# DATABASE TABLES
# ==============================

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    username = Column(String, nullable=True)
    points = Column(Integer, default=0)
    wallet_balance = Column(Float, default=0.0)
    checkin_streak = Column(Integer, default=0)
    last_checkin = Column(DateTime, default=None)
    registered_at = Column(DateTime, default=datetime.utcnow)
    is_banned = Column(Boolean, default=False)


class Referral(Base):
    __tablename__ = "referrals"
    id = Column(Integer, primary_key=True)
    referrer_id = Column(Integer, ForeignKey("users.id"))
    referred_id = Column(Integer, ForeignKey("users.id"))
    task_completed = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False)  # channel, link, shortlink, app
    link = Column(Text, nullable=True)
    points = Column(Integer, default=0)
    premium = Column(Boolean, default=False)
    active = Column(Boolean, default=True)


class UserTask(Base):
    __tablename__ = "user_tasks"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"))
    completed = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Sponsor(Base):
    __tablename__ = "sponsors"
    id = Column(Integer, primary_key=True)
    channel = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    rotation_date = Column(DateTime, default=datetime.utcnow)


class Withdrawal(Base):
    __tablename__ = "withdrawals"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)
    upi_id = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending / approved / rejected
    timestamp = Column(DateTime, default=datetime.utcnow)


class Checkin(Base):
    __tablename__ = "checkins"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date, default=datetime.utcnow)
    streak = Column(Integer, default=0)


class Setting(Base):
    __tablename__ = "settings"
    key = Column(String, primary_key=True)
    value = Column(String)


# ==============================
# DATABASE CONNECTION
# ==============================

engine = create_engine(DB_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully!")

# ==============================
# HELPER FUNCTION
# ==============================

def get_session():
    """Return a new session"""
    return SessionLocal()

# ==============================
# TEST DATABASE
# ==============================

if __name__ == "__main__":
    init_db()
