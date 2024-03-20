#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
from sqlalchemy import DateTime
from datetime import datetime as dt
import models
Base = declarative_base()

class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=dt.utcnow())
    updated_at = Column(DateTime, nullable=False, default=dt.utcnow())
    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = dt.utcnow()
            self.updated_at = dt.utcnow()
        else:
            for key, value in kwargs.items():
                setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = dt.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        for value in self.__table__.columns:
            dictionary[value.name] = getattr(self, value.name)
        dictionary.pop("_sa_instance_state", None)
        return dictionary

    def delete(self):
        """delete current instanse"""
        models.storage.delete(self)
