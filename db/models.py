from sqlalchemy import Column, Integer, String, JSON, CheckConstraint, PickleType
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from typing import Dict

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column('username', String(36), unique=True, nullable=False)
    email = Column('email', String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    config = Column(JSONB, nullable=False)
    __table_args__ = (
        CheckConstraint(
            'char_length(username) > 5',
            name='username_min_length'
        ),
    )
