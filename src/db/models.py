from uuid import uuid4
from datetime import datetime, date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Text, Integer, Date, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from sqlalchemy.ext.declarative import declarative_base
from src.db.database import Base
from sqlalchemy.orm import configure_mappers

# models.py

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(Text, nullable=True)
    uid = Column(String, unique=True, nullable=False)  # Firebase UID
    plan = Column(String(20), default="free")  # free, pro
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    pdfs = relationship("PDF", back_populates="user")
    chats = relationship("ChatHistory", back_populates="user")
    usage = relationship("UsageTracker", back_populates="user", cascade="all, delete")
    # usage = relationship("UsageTracker", back_populates="user")


class PDF(Base):
    __tablename__ = "pdfs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    filename = Column(String, nullable=False)
    upload_path = Column(Text, nullable=False)
    chunk_count = Column(Integer, default=0)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="pdfs")
    chunks = relationship("PDFChunk", back_populates="pdf", cascade="all, delete")

class PDFChunk(Base):
    __tablename__ = "pdf_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    pdf_id = Column(UUID(as_uuid=True), ForeignKey("pdfs.id"))
    chunk_text = Column(Text)
    # embedding = Column(Vector(1536))  # using pgvector

    pdf = relationship("PDF", back_populates="chunks")

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    pdf_id = Column(UUID(as_uuid=True), ForeignKey("pdfs.id"), nullable=True)
    question = Column(Text, nullable=False)
    answer = Column(Text)
    tokens_used = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="chats")

class UsageTracker(Base):
    __tablename__ = "usage_tracker"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)  # ✅ Add this line
    user = relationship("User", back_populates="usage")

    date = Column(Date, default=date.today)
    pdf_count = Column(Integer, default=0)
    chat_count = Column(Integer, default=0)
    limit_reached = Column(Boolean, default=False)

    __table_args__ = (UniqueConstraint('user_id', 'date', name='uix_user_date'),)

class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    stripe_customer_id = Column(String)
    subscription_status = Column(String)
    next_billing_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")

configure_mappers()
