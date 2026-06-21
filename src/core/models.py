"""Database models"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    """User model"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)

class Command(Base):
    """Command history model"""
    __tablename__ = 'commands'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    command_text = Column(Text, nullable=False)
    intent = Column(String(50), nullable=False)
    confidence = Column(Float)
    execution_status = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    execution_time = Column(Float)

class Session(Base):
    """Session model"""
    __tablename__ = 'sessions'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(100), unique=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    is_active = Column(Boolean, default=True)