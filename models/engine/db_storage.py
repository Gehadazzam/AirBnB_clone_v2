#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""


from sqlalchemy import create_engine
from os import environ as en
from models.base_model import Base, BaseModel
from sqlalchemy.orm import sessionmaker as sm
from sqlalchemy.orm import scoped_session as ss


class DBStorage:
    """move the storage using sqlalchemy"""

    __engine = None
    __session = None

    def __init__(self):
        """init the variable"""

        "get envieronment"
        user = en.get("HBNB_MYSQL_USER")
        pas = en.get("HBNB_MYSQL_PWD")
        host = en.get("HBNB_MYSQL_HOST", "localhost")
        db = en.get("HBNB_MYSQL_DB")

        "create the engine"
        self.__engine = create_engine(
            f"mysql+mysqldb://{user}: {pas}@{host}/{db}", pool_pre_ping= True
        )
        env = en.get("HBNB_ENV")

        "drop if was test"
        if env == "test":
            Base.metadata.drop_all(self.__engine)
        "create if not"
        Base.metadata.create_all(self.__engine)

        "creat the session"
        self.__session = ss(sm(bind=self.__engine))
        
    def all(self, cls=None):
        """query all objects"""
        dic = {}
        if cls is None:
            q = self.__session.query(Base)
        else:
            q = []
            for cls in BaseModel.__subclasses__():
             for x in self.__session.query(cls).all():
                 q.append(x)
        for z in q:
            k = f"{z.__class__.__name__}.{z.id}"
            dic[k] = z
        return dic

    def new(self, sth):
        """add new something to the database"""

        self.__session.add(sth)

    def save(self):
       """commit all changes"""
       self.__session.commit()

    def delete(self, obj=None):
        """Delete object if not none"""

        self.__session.delete(obj)
     
    def reload(self):
        """recreate the previous data"""

        Base.metadat.create_all(self.__engine)
        self.__session = ss(sm(bind=self.__engine), expire_on_commit=False)
