#!/usr/bin/python3
"""This module defines a class User"""
import sqlalchemy
import hashlib
import models
from models import storage
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    """ The user class """
    if getenv('HBNB_TYPE_STORAGE') != 'db':
        email = ""
        passwd = ""
        first_name = ""
        last_name = ""
    else:
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        passwd = Column(
            'password', String(128), nullable=False
        )
        first_name = Column(
            String(128), nullable=True
        )
        last_name = Column(
            String(128), nullable=True
        )
        places = relationship(
            "Place",
            backref="user",
            cascade="all, delete-orphan"
        )
        reviews = relationship(
            "Review",
            backref="user",
            cascade="all, delete-orphan"
        )

    def __init__(self, *args, **kwargs):
        """ Initialize User """
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        return self.passwd

    @password.setter
    def password(self, pwd):
        self.passwd = pwd
