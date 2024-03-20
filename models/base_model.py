#!/usr/bin/python3

"""This is the base module containing all common attributes/methods
for other classes"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from models import storage_type


Base = declarative_base()


class BaseModel:
    """A class representing the base model for other classes in
    the hbnb project."""
    id = Column(String(60), nullable=False, primary_key=True, unique=True)
    created_at = Column(DATETIME, nullable=False,
                        default=datetime.now(timezone.utc))
    updated_at = Column(DATETIME, nullable=False,
                        default=datetime.now(timezone.utc))

    def __init__(self, *args, **kwargs):
        """Initialize a new instance of the BaseModel class.

        Attributes:
            id (uuid.UUID): A universally unique identifier for the instance.
            created_at (datetime.datetime): The datetime object representing
            the creation time (UTC).
            updated_at (datetime.datetime): The datetime object representing
            the last update time (UTC).
        """
        if not kwargs:

            self.id = str(uuid.uuid4())
            self.created_at = datetime.now(timezone.utc)
            self.updated_at = datetime.now(timezone.utc)

        else:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key in ('created_at', 'updated_at'):
                        setattr(self, key, datetime.fromisoformat(value))
                    else:
                        setattr(self, key, value)
            # if os.getenv('HBNB_TYPE_STORAGE') in ('db'):
            if storage_type == 'db':

                if not hasattr(kwargs, 'id'):
                    setattr(self, 'id', str(uuid.uuid4()))
                if not hasattr(kwargs, 'created_at'):
                    setattr(self, 'created_at', datetime.now(timezone.utc))
                if not hasattr(kwargs, 'updated_at'):
                    setattr(self, 'updated_at', datetime.now(timezone.utc))

    def save(self):
        """Update the 'updated_at' attribute with the current UTC time."""
        from models import storage
        self.updated_at = datetime.now(timezone.utc)
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert the BaseModel instance to a dictionary representation.

        Returns:
            dict: A dictionary containing all attributes of the instance,
            including class name,
                'created_at', and 'updated_at' formatted as ISO 8601 strings.
        """
        inst_dict = self.__dict__.copy()
        inst_dict["__class__"] = self.__class__.__name__
        inst_dict["created_at"] = self.created_at.isoformat()
        inst_dict["updated_at"] = self.updated_at.isoformat()
        return inst_dict

    def delete(self):
        """Deletes this BaseModel instance from the storage"""
        from models import storage
        storage.delete(self)

    def __str__(self):
        """Return a string representation of the BaseModel instance.

        Returns:
            str: A string containing the class name, 'id', and attribute
            dictionary of the instance.
        """
        class_name = self.__class__.__name__
        return f"[{class_name}] ({self.id}) {self.__dict__}"
