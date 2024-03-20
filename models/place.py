#!/usr/bin/python3
""" Place Module for HBNB project """
import models
from models import storage
import sqlalchemy
from os import getenv
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base

if getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table(
        'place_amenity', Base.metadata, Column(
            'place_id',
            String(60),
            ForeignKey('places.id'),
            primary_key=True,
            nullable=False
        ), Column(
            'amenity_id',
            String(60),
            ForeignKey('amenities.id'),
            primary_key=True,
            nullable=False
        )
    )


class Place(BaseModel, Base):
    """ A place to stay """
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'places'
        city_id = Column(
            String(60),
            ForeignKey="cities.id",
            nullable=False
        )
        user_id = Column(
            String(60),
            ForeignKey="users.id",
            nullable=False
        )
        name = Column(
            String(128),
            nullable=False
        )
        description = Column(
            String(1024),
            nullable=True
        )
        number_rooms = Column(
            Integer,
            default=0,
            nullable=False
        )
        number_bathrooms = Column(
            Integer,
            default=0,
            nullable=False
        )
        max_guest = Column(
            Integer,
            default=0,
            nullable=False
        )
        price_by_night = Column(
            Integer,
            default=0,
            nullable=False
        )
        latitude = Column(
            Float,
            nullable=True,
        )
        longitude = Column(
            Float,
            nullable=True,
        )
        reviews = relationship(
            "Review",
            cascade="all, delete",
            backref="places"
        )
        amenities = relationship(
            "Amenity",
            secondary='place_amenity',
            viewonly=False,
            backref="place_amenities"
        )
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    def __init__(self, *args, **kwargs):
        """initializes Place"""
        super().__init__(*args, **kwargs)

    @property
    def reviews(self):
        values_r = storage.all("Review").values()
        list_r = []
        for review in values_r:
            if review.place_id == self.id:
                list_r.append(review)
        return list_r

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def amenities(self):
            values_a = storage.all("Amenity").values()
            list_a = []
            for amenity in values_a:
                if amenity.place_id == self.id:
                    list_a.append(amenity)
            return list_a
