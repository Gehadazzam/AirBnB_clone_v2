#!/usr/bin/python3
""" DBStorage module for HBNB project """

import os
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

DB_class = {
    "Amenity": Amenity,
    "Place": Place,
    "City": City,
    "State": State,
    "Review": Review,
    "User": User,
}


class DBStorage:
    """New engine DBStorage: (models/engine/db_storage.py)"""

    __engine = None
    __session = None

    def __init__(self):
        """create the engine (self.__engine)"""
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        database = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                user, password, host, database
            )
        )
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session (self.__session)"""
        dict = {}
        if not self.__session:
            self.reload()
        if type(cls) == str:
            cls = DB_class.get(cls, None)
        if cls:
            for obj in self.__session.query(cls):
                dict[(
                    "{}.{}".format(obj.__class__.__name__, obj.id)
                )] = obj
        else:
            for cls in DB_class.values():
                for obj in self.__session.query(cls):
                    dict[(
                        "{}.{}".format(obj.__class__.__name__, obj.id)
                    )] = obj
        return dict

    def reload(self):
        """inherit from Base must be imported before calling"""
        sess = sessionmaker(
            bind=self.__engine, expire_on_commit=False
        )
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sess)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj:
            if not self.__session:
                self.reload()
            self.__session.delete(obj)

    def close(self):
        """Dispose of current session if active"""
        self.__session.remove()

    def get(self, cls, id):
        """get an object"""
        if (
            cls is not None
            and type(cls) is str
            and type(id) is str
            and id is not None
            and cls in DB_class
        ):
            cls = DB_class[cls]
            i = self.__session.query(cls).filter(
                cls.id == id
            ).first()
            return i
        else:
            return None

    def count(self, cls=None):
        """Count objects"""
        n = 0
        if type(cls) == str and cls in DB_class:
            cls = DB_class[cls]
            n = self.__session.query(cls).count()
        elif cls is None:
            for cls in DB_class.values():
                n += self.__session.query(cls).count()
        return n
