#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""
    classes = {
        "Amenity": Amenity,
        "BaseModel": BaseModel,
        "City": City,
        "Place": Place,
        "Review": Review,
        "State": State,
        "User": User
    }
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
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
        """sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            k = "{}.{}".format(
                obj.__class__.__name__, obj.id
            )
            self.__objects[k] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        j_obj = {}
        for key in self.__objects:
            j_obj[key] = self.__objects[key].to_dict(
                save_to_disk=True
            )
        with open(self.__file_path, 'w') as f:
            json.dump(j_obj, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except:
            pass

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            del self.__objects[
                "{}.{}".format(obj.__class__.__name__, obj.id)
            ]
            self.save()

    def close(self):
        """Deserialize JSON file to objects"""
        self.reload()

    def get(self, cls, id):
        """get an object"""
        if cls is not None and type(cls) is str and id is not None and\
           type(id) is str and cls in classes:
            key = cls + '.' + id
            obj = self.__objects.get(key, None)
            return obj
        else:
            return None

    def count(self, cls=None):
        """Count"""
        t = 0
        if type(cls) == str and cls in classes:
            t = len(self.all(cls))
        elif cls is None:
            t = len(self.__objects)
        return t
