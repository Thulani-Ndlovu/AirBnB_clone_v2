#!/usr/bin/python3
from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

if getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.place import place_amenity

classes = {"user": User, "State": State, "City": City, "Amenity": Amenity,
           "Place": Place, "Review": Review}


class DBStorage:
    """ Engine DB Storage"""
    __engine = None
    __session = None

    def __init__(self):
        '''DataBase instantiation'''
        MYSQL_USER = getenv('HBNB_MYSQL_USER')
        MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                MYSQL_USER,
                MYSQL_PWD,
                MYSQL_HOST,
                MYSQL_DB
            ), pool_pre_ping=True
        )

        if HBNB_ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        ''' Query on the current database session. all objects
            depending on the class name cls
        '''
        dictionary = {}
        if cls is None:
            for i in classes.values():
                objects = self.__session.query(i).all()
                for object in objects:
                    key = object.__class__.__name__ + '.' + object.id
                    dictionary[key] = object
        else:
            objects = self.__session.query(cls).all()
            for object in objects:
                key = object.__class__.__name__ + '.' + object.id
                dictionary[key] = object
        return dictionary

    def new(self, obj):
        '''adds the object to the current database session'''
        if obj is not None:
            try:
                self.__session.add(obj)
                self.__session.flush(obj)
                self.__session.refresh(obj)
            except Exception as e:
                self.__session.rollback()
                raise e

    def save(self):
        '''commits all changes of the current database session'''
        self.__session.commit()

    def delete(self, obj=None):
        '''deletes from the current database session obj if not None'''
        if obj is not None:
            self.__session.query(type(obj)).filter(
                type(obj).id == obj.id).delete()

    def reload(self):
        '''
            Create all tables in the database(feature of SQLALCHEMY)
            (WARNING: all classes who inherit from Base must be imported
            before calling Base.metadata.create_all(engine))
        '''
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)()

    def close(self):
        '''close sqlachemy session'''
        self.__session.close()
