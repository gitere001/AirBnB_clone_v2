#!/usr/bin/python3

"""This is the base module containing all common attributes/methods
for other classes"""
import uuid
from datetime import datetime
import models


class BaseModel:
    """A class representing the base model for other classes in
    the hbnb project."""
    def __init__(self, *args, **kwargs):
        """Initialize a new instance of the BaseModel class.

        Attributes:
            id (uuid.UUID): A universally unique identifier for the instance.
            created_at (datetime.datetime): The datetime object representing
            the creation time (UTC).
            updated_at (datetime.datetime): The datetime object representing
            the last update time (UTC).
        """
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                elif key == "created_at" or key == "updated_at":
                    setattr(self, key, datetime.strptime(value, time_format))
                else:
                    setattr(self, key, str(value))

        models.storage.new(self)

    def save(self):
        """Update the 'updated_at' attribute with the current UTC time."""
        self.updated_at = datetime.utcnow()
        models.storage.save()

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

    def __str__(self):
        """Return a string representation of the BaseModel instance.

        Returns:
            str: A string containing the class name, 'id', and attribute
            dictionary of the instance.
        """
        class_name = self.__class__.__name__
        return f"[{class_name}] ({self.id}) {self.__dict__}"
