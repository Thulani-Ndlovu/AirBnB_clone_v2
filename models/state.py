#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
from models import storage_type
from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel):
    """ State class """

    __tablename__ = 'states'
    if storage_type == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state',
                              cascade='all, delete, delete-orphan')
    else:
        name = ""

        @property
        def cities(self):
            """
                Returns the list of city instances with state_id
                equals to the current state_id.
                It will be the Filestorage relationship between state and city
            """
            from models import storage
            listCities = []
            cities_ = storage.all(City)
            for city_ in cities_.values():
                if city_.state_id == self.id:
                    listCities.append(city_)
            return listCities
