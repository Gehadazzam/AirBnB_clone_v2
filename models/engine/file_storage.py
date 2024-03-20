#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from os.path import exists


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""

    __file_path = "file.json"
    __objects = {}

    def delete(self, obj=None):
        """delete object"""

        if obj is None:
            pass
        else:
            value = f"{type(obj).__name__}.{obj.id}"
            if value in self.__objects:
                del self.__objects[value]

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None:
            return self.__objects
        else:
            return {
                key: obj for key, obj in self.__objects.items()
                if isinstance(obj, cls)
            }

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()["__class__"] + "." + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, "w") as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def class_dict(self):
        """
        to correctly serialize and deserialize instances of the new classes
        """
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        class_dict = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review,
        }
        return class_dict

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
            "BaseModel": BaseModel,
            "User": User,
            "Place": Place,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Review": Review,
        }
        if exists(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
                line = json.load(f)
                line = {
                    k: self.class_dict()
                    [v["__class__"]](**v) for k, v in line.items()
                }
                FileStorage.__objects = line
        else:
            return

    @property
    def cities(self):
        """list of states and cities"""
        import models
        from models.city import City as C
        from models.state import State as S
        return [city for city in models.storage.all(C) if city.state.id == self.id]
