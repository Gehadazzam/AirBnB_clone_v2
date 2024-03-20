#!/usr/bin/python3
""" State Module for HBNB project """
import sqlalchemy
from os import getenv
from models import storage
from sqlalchemy import ForeignKey
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class State(BaseModel):
    """ State class """
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'states'
        cities = relationship("City", cascade="all, delete", backref="states")
        name = Column(String(128), nullable=False)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            """citites will return"""
            list_v = []
            val = storage.all('City').values()
            for i in val:
                if i.state_id == self.id:
                    list_v.append(i)
            return list_v
