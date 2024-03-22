#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from os import getenv

if getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.place import place_amenity

classes = {"User": User, "State": State, "City": City,
           "Amenity": Amenity, "Place": Place, "Review": Review}


class DBStorage:
    """responsible to manage storage of hbnb in a SQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """intitializing the sql database  storage"""
        user = getenv('HBNB_MYSQL_USER')
        pword = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db_name = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')

        DATABASE_URL = f"mysql+mysqldb://{user}:{pword}@{host}:3306/{db_name}"
        self.__engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """return dictionary of models currently in storage"""
        objects = dict()
        if cls is None:
            for clss in classes.values():
                query = self.__session.query(clss).all()
                for obj in query:
                    obj_key = f'{obj.__class__.__name__}.{obj.id}'
                    objects[obj_key] = obj
        else:
            query = self.__session.query(cls).all()
            for obj in query:
                obj_key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                objects[obj_key] = obj
        return objects

    def delete(self, obj=None):
        """Removes an object from the storage database"""
        if obj is not None:
            self.__session.query(type(obj)).filter(
                type(obj).id == obj.id).delete(
                synchronize_session=False
            )

    def new(self, obj):
        """Adds new object to storage database"""
        if obj is not None:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception as ex:
                self.__session.rollback()
                raise ex

    def save(self):
        """Commits the session changes to database"""
        self.__session.commit()

    def reload(self):
        """Loads storage database"""
        Base.metadata.create_all(self.__engine)
        SessionFactory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        self.__session = scoped_session(SessionFactory)()

    def close(self):
        """Closes the storage engine."""
        self.__session.close()
