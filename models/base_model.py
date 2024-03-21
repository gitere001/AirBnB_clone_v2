#!/usr/bin/python3
"""defines a base class for all models in our hbnb clone where all classes
are initialized
"""

import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from models import storage_type

Base = declarative_base()


class BaseModel:
    """Base class for all models in the HBNB clone.

    Attributes:
        id (sqlalchemy String): unique identification the base  model.
        created_at (sqlalchemy DateTime): The date and time of creation.
        updated_at (sqlalchemy DateTime): The date and time of last update.
    """

    id = Column(String(60),
                nullable=False,
                primary_key=True,
                unique=True)
    created_at = Column(DateTime,
                        nullable=False,
                        default=datetime.utcnow)
    updated_at = Column(DateTime,
                        nullable=False,
                        default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initializes a new model instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            for k in kwargs:
                if k in ['created_at', 'updated_at']:
                    setattr(self, k, datetime.fromisoformat(kwargs[k]))
                elif k != '__class__':
                    setattr(self, k, kwargs[k])
            if storage_type == 'db':
                if not hasattr(kwargs, 'id'):
                    setattr(self, 'id', str(uuid.uuid4()))
                if not hasattr(kwargs, 'created_at'):
                    setattr(self, 'created_at', datetime.now())
                if not hasattr(kwargs, 'updated_at'):
                    setattr(self, 'updated_at', datetime.now())

    def __str__(self):
        """Returns a string representation of the instance."""
        return '[{}] ({}) {}'.format(
            self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed."""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Converts instance into dictionary format.

        Returns:
            dict: A dictionary containing all attributes of the instance.
        """
        instance_dict = self.__dict__.copy()
        instance_dict['__class__'] = self.__class__.__name__
        for k in instance_dict:
            if isinstance(instance_dict[k], datetime):
                instance_dict[k] = instance_dict[k].isoformat()
        if '_sa_instance_state' in instance_dict.keys():
            del instance_dict['_sa_instance_state']
        return instance_dict

    def delete(self):
        """Deletes the current instance from the storage."""
        from models import storage
        storage.delete(self)
