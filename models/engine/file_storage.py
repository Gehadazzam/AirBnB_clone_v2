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
        dict = {}
        if cls is not None:
            for k, v in self.__objects.items():
                if isinstance(v, cls):
                    dict[k] = v
            return dict

        return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            new_dic = {}
            new_dic.update(FileStorage.__objects)
            for key, val in new_dic.items():
                new_dic[key] = val.to_dict()
            json.dump(new_dic, f)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            new_diction = {}
            with open(FileStorage.__file_path, 'r') as f:
                new_diction = json.load(f)
                for key, val in new_diction.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """returns the list of objects of one type of class"""
        if obj is not None:
            k = "{}.{}".format(obj.__class__.__name__, obj.id)
            del self.__objects[k]
