#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""

import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {
    "Amenity": Amenity,
    "BaseModel": BaseModel,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User,
}


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if not cls:
            return self.__objects
        elif type(cls) == str:
            return {
                k: v for k, v in self.__objects.items() if (
                    v.__class__.__name__ == cls
                )
            }
        else:
            return {
                k: v for k, v in self.__objects.items() if (
                    v.__class__ == cls
                )
            }

    def new(self, obj):
        """Adds new object to storage dictionary"""
        if obj is not None:
            k = "{}.{}".format(
                    obj.__class__.__name__, obj.id
                )
            self.__objects[k] = obj

    def save(self):
        """Saves storage dictionary to file"""
        temp = {}
        for k in self.__objects:
            temp[k] = self.__objects[k].to_dict(
                save_to_disk=True
            )
        with open(self.__file_path, "w") as f:
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            with open(self.__file_path, "r") as f:
                temp = json.load(f)
            for k in temp:
                self.__objects[k] = classes[temp[k]["__class__"]](**temp[k])
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """returns the list of objects of one type of class"""
        if obj is not None:
            k = "{}.{}".format(obj.__class__.__name__, obj.id)
            del self.__objects[k]
            self.save()

    def close(self):
        """Dispose of current session if active"""
        self.reload()

    def get(self, cls, id):
        """get an object"""
        if (
            cls is not None
            and type(cls) is str
            and type(id) is str
            and id is not None
            and cls in classes
        ):
            k = "{}.{}".format(cls, id)
            v = self.__objects.get(k, None)
            return v
        else:
            return None

    def count(self, cls=None):
        """Count objects"""
        n = 0
        if type(cls) == str and cls in classes:
            n = len(self.all(cls))
        elif cls is None:
            n = len(self.__objects)
        return n
