#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.review import Review
from models import storage_type
from sqlalchemy.sql.schema import Table
from sqlalchemy import Column, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship

if storage_type == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('place_id'),
                                 primary_key=True,
                                 nullable=False),
                          Column('amenity_id',
                                 String(60),
                                 ForeignKey('place_id'),
                                 primary_key=True,
                                 nullable=False)
                          )


class Place(BaseModel):
    """ A place to stay """
    __tablename__ = 'places'
    if storage_type == 'db':
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship('Review', backref='place',
                               cascade='all, delete, delete-orphan')
        amenities = relationship('Amenity', secondary=place_amenity,
                                 viewonly=False, backref='place_amenities')
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

        @property
        def reviews(self):
            '''
                returns the list of Review instances with place_id
                equals to the current Place.id
                => It will be the FileStorage relationship
                between Place and Review
            '''
            from models import storage
            review_list = []
            reviews_ = storage.all(Review)
            for review_ in reviews_.values():
                if review_.place_id == self.id:
                    review_list.append(review_)
            return review_list

        @property
        def amenities(self):
            """
                eturns the list of Amenity instances based
                on the attribute amenity_ids that contains
                all Amenity.id linked to the Place
            """
            from models import storage
            amenities_list = []
            amenities_ = storage.all(Amenity)
            for amenity_ in amenities_.values():
                if amenity_.id in self.amenity_ids:
                    amenities_list.append(amenity_)
            return amenities_list

        @amenities.setter
        def amenities(self, obj):
            """
                handles append method for adding an Amenity.id
                to the attribute amenity_ids.
                This method should accept only
                Amenity object, otherwise, do nothing.
            """
            if obj is not None:
                if isinstance(obj, Amenity):
                    if obj.id not in self.amenity_ids:
                        self.amenity_ids.append(obj.id)
