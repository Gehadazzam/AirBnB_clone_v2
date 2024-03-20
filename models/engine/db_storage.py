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

classes = {
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
        dict = {}
        if cls:
            obj = self.__session.query(self.classes()[cls].all())
        else:
            list_t = ['State', 'City', 'User', 'Place', 'Amenity', 'Review']
            for i in list_t:
                obj += self.__session.query(i).all()
            for k in obj:
                n = "{}.{}".format(k.__class__.__name__, k.id)
                dict[n] = k
        return dict

    def reload(self):
        """inherit from Base must be imported before calling"""
        Base.metadata.create_all(self.__engine)
        self.__session = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        Session = scoped_session(self.__session)
        self.__session = Session()

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def close(self):
        """Dispose of current session if active"""
        self.__session.remove()
