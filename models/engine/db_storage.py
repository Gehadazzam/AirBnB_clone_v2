#!/usr/bin/python3
""" DBStorage module for HBNB project """
import json
import os
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

DB_class = {
    "BaseModel": BaseModel,
    "User": User,
    "State": State,
    "City": City,
    "Amenity": Amenity,
    "Place": Place,
    "Review": Review
}

class DBStorage:
    """New engine DBStorage: (models/engine/db_storage.py)"""

    __engine = None
    __session = None

    def __init__(self):
        """create the engine (self.__engine)"""
        hbnb_dev = getenv('HBNB_MYSQL_USE')
        hbnb_dev_pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        hbnb_dev_db = getenv('HBNB_MYSQL_DB')
        db_url = "mysql+mysqldb://{}:{}@{}:3306/{}".format(
            hbnb_dev, hbnb_dev_pwd, host, hbnb_dev_db
        )
        self.__engine = create_engine(
            db_url, pool_pre_ping=True
        )
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """query on the current database session (self.__session)"""
        if not self.__session:
            self.reload()
        objects = {}
        if type(cls) == str:
            cls = DB_class.get(cls, None)
        k = "{}.{}".format(obj.__class__.__name__, obj.id)
        if cls:
            for obj in self.__session.query(cls):
                objects[k] = obj
        else:
            for cls in DB_class.values():
                for obj in self.__session.query(cls):
                    objects[k] = obj
        return objects

    def reload(self):
        """inherit from Base must be imported before calling"""
        session_factory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(session_factory)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        if not self.__session:
            self.reload()
        if obj:
            self.__session.delete(obj)

    def close(self):
        self.__session.remove()

    def get(self, cls, id):
        if (
            cls is not None
            and type(cls) is str
            and id is not None
            and type(id) is str
            and cls in DB_class
        ):
            cls = DB_class[cls]
            result = self.__session.query(cls).filter(cls.id == id).first()
            return result
        else:
            return None

    def count(self, cls=None):
        n = 0
        if type(cls) == str and cls in DB_class:
            cls = DB_class[cls]
            n = self.__session.query(cls).count()
        elif cls is None:
            for cls in DB_class.values():
                n += self.__session.query(cls).count()
        return n
