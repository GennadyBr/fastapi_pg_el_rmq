from sqlalchemy import Column, Integer, String, JSON, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column('username', String(36), unique=True, nullable=False)
    email = Column('email', String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    config = Column(JSON, nullable=False)
    __table_args__ = (
        CheckConstraint(
            'char_length(username) > 5',
            name='username_min_length'
        ),
        # CheckConstraint(
        #     "regexp_like(email,'^[a-zA-Z][a-zA-Z0-9_\.\-]+@([a-zA-Z0-9-]{2,}\.)+([a-zA-Z]{2,4}|[a-zA-Z]{2}\.[a-zA-Z]{2})$')",
        #     name='emailcheck'
        # ),
    )
