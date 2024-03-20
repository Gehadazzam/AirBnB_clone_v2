#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage as db
from os import environ as en

env = en.get("HBNB_TYPE_STORAGE")
if env == "db":
    storage = db()
    storage.reload()
else:
    storage = FileStorage()
    storage.reload()
