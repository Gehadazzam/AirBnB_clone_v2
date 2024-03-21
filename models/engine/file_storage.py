#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """storage hbnb in JSON"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of models
        """
        if cls is not None:
            new_obj_dict = {}
            for key, value in self.__objects.items():
                if isinstance(value, cls):
                    new_obj_dict[key] = value
            return new_obj_dict

        return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage dict"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            t = {}
            t.update(FileStorage.__objects)
            for k, v in t.items():
                t[k] = v.to_dict()
            json.dump(t, f)

    def reload(self):
        """Loads storage dict"""
        classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Method that deletes obj from __objects"""
        if obj is not None:
            # get the key for this obj class name.id
            k = obj.__class__.__name__ + '.' + obj.id
            del self.__objects[k]
