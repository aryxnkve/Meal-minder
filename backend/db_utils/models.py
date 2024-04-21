
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from utils.util import get_hashed_password
import bcrypt
from sqlalchemy.orm import validates, relationship
import re
from fastapi import HTTPException
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    enc_password = Column(String)
    first_name = Column(String, unique=True)
    last_name = Column(String, unique=True)

    def __init__(self, username, first_name, last_name, password):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.set_password(password)

    def __iter__(self):
        for key in ["id", "first_name", "last_name", "username"]:
            # if key in ["account_created", "account_updated"]:
            #     yield key, parse_timestamp(getattr(self, key))
            # else:
                yield key, getattr(self, key)

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.enc_password.encode('utf-8'))
    
    def set_password(self, password):
        if not password:
            raise HTTPException('Password not provided')

        if not isinstance(password, str):
            raise HTTPException('password should be a string')

        if len(password) < 8 or len(password) > 50:
            raise HTTPException(status_code=500, detail=
                'Password must be between 8 and 50 characters')
        self.enc_password = get_hashed_password(password).decode('utf-8')

