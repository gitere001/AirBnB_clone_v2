#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models import storage_type
from models.city import City
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'  # Define the table name for SQLAlchemy

    if storage_type == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state',
                              cascade='all, delete-orphan')

    else:
        name = ''

        @property
        def cities(self):
            """
            returns the list of city instances with same state_id
            """
            from models import storage
            all_cities = []
            cities = storage.all(City)
            for city in cities.values():
                if city.state_id == self.id:
                    all_cities.append(city)
            return all_cities
