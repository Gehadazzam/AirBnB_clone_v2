#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""

import uuid
import models
from os import getenv
from models import storage
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

if getenv("HBNB_TYPE_STORAGE") == 'db':
    Base = declarative_base()
else:
    Base = object
DateTime_t = '%Y-%m-%dT%H:%M:%S.%f'


class BaseModel:
    """A base class for all hbnb models"""
    if getenv('HBNB_TYPE_STORAGE') == "db":
        id = Column(String(60), primary_key=True, nullable=False)
        created_at = Column(
            DateTime, nullable=False, default=datetime.utcnow
        )
        updated_at = Column(
            DateTime, nullable=False, default=datetime.utcnow
        )

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        for k, v in kwargs.items():
            if k == '__class__':
                continue
            setattr(self, k, v)
            if type(self.created_at) is str:
                self.created_at = datetime.strptime(
                    self.created_at, DateTime_t
                )
            if type(self.updated_at) is str:
                self.updated_at = datetime.strptime(
                    self.updated_at, DateTime_t
                )

    def __str__(self):
        """Returns a string representation of the instance"""
        return '[{:s}] ({:s}) {}'.format(
            self.__class__.__name__, self.id, self.__dict__
        )

    def save(self):
        """Updates updated_at with current time when
        instance is changed"""
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dict = self.__dict__.copy()
        if "created_at" in dict:
            dict["created_at"] = dict["created_at"].isoformat()
        if "updated_at" in dict:
            dict["updated_at"] = dict["updated_at"].isoformat()
        if '_password' in dict:
            dict['password'] = dict['_password']
            dict.pop('_password', None)
        if 'amenities' in dict:
            dict.pop('amenities', None)
        if 'reviews' in dict:
            dict.pop('reviews', None)
        dict["__class__"] = self.__class__.__name__
        dict.pop('_sa_instance_state', None)
        if not save_to_disk:
            dict.pop('password', None)
        return dict

    def delete(self):
        """Deletes an instance in the database"""
        storage.delete(self)
