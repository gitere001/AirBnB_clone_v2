#!/usr/bin/python3
"""Module for unit tests of the BaseModel class"""

from models.base_model import BaseModel
from datetime import datetime
import unittest
import json
import os


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                 'BaseModel tests not supported for database storage')
class TestBaseModel(unittest.TestCase):
    """Test cases for the BaseModel class"""

    def __init__(self, *args, **kwargs):
        """Initialize the test class for BaseModel"""
        super().__init__(*args, **kwargs)
        self.model_name = 'BaseModel'
        self.model_class = BaseModel

    def setUp(self):
        """Set up the test environment"""
        pass

    def tearDown(self):
        """Tear down the test environment"""
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_init(self):
        """Test initialization of the BaseModel class"""
        self.assertIsInstance(self.model_class(), BaseModel)
        if self.model_class is not BaseModel:
            self.assertIsInstance(self.model_class(), BaseModel)
        else:
            self.assertNotIsInstance(self.model_class(), BaseModel)

    def test_default(self):
        """Test default instantiation of BaseModel"""
        instance = self.model_class()
        self.assertEqual(type(instance), self.model_class)

    def test_kwargs(self):
        """Test instantiation of BaseModel with kwargs"""
        instance = self.model_class()
        copy = instance.to_dict()
        new_instance = BaseModel(**copy)
        self.assertFalse(new_instance is instance)

    def test_kwargs_int(self):
        """Test instantiation of BaseModel with integer kwargs"""
        instance = self.model_class()
        copy = instance.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new_instance = BaseModel(**copy)

    def test_save(self):
        """Test the save method of BaseModel"""
        instance = self.model_class()
        instance.save()
        key = self.model_name + "." + instance.id
        with open('file.json', 'r') as f:
            data = json.load(f)
            self.assertEqual(data[key], instance.to_dict())

    def test_str(self):
        """Test the __str__ method of BaseModel"""
        instance = self.model_class()
        expected_output = '[{}] ({}) {}'.format(
            self.model_name, instance.id, instance.__dict__)
        self.assertEqual(str(instance), expected_output)

    def test_to_dict(self):
        """Test the to_dict method of BaseModel"""
        instance = self.model_class()
        dict_representation = instance.to_dict()
        self.assertEqual(instance.to_dict(), dict_representation)
        self.assertIsInstance(dict_representation, dict)
        self.assertIn('id', dict_representation)
        self.assertIn('created_at', dict_representation)
        self.assertIn('updated_at', dict_representation)
        instance.firstname = 'John'
        instance.lastname = 'Doe'
        self.assertIn('firstname', instance.to_dict())
        self.assertIn('lastname', instance.to_dict())
        self.assertIsInstance(dict_representation['created_at'], str)
        self.assertIsInstance(dict_representation['updated_at'], str)
        datetime_now = datetime.today()
        instance.id = '012345'
        instance.created_at = instance.updated_at = datetime_now
        expected_dict = {
            'id': '012345',
            '__class__': instance.__class__.__name__,
            'created_at': datetime_now.isoformat(),
            'updated_at': datetime_now.isoformat()
        }
        self.assertDictEqual(instance.to_dict(), expected_dict)
        if os.getenv('HBNB_TYPE_STORAGE') != 'db':
            self.assertDictEqual(
                self.model_class(id='u-b34', age=13).to_dict(),
                {
                    '__class__': instance.__class__.__name__,
                    'id': 'u-b34',
                    'age': 13
                }
            )
            self.assertDictEqual(
                self.model_class(id='u-b34', age=None).to_dict(),
                {
                    '__class__': instance.__class__.__name__,
                    'id': 'u-b34',
                    'age': None
                }
            )
        self.assertIn('__class__', instance.to_dict())
        self.assertNotIn('__class__', instance.__dict__)
        self.assertNotEqual(instance.to_dict(), instance.__dict__)
        self.assertNotEqual(
            instance.to_dict()['__class__'],
            instance.__class__
        )

    def test_kwargs_none(self):
        """Test instantiation of BaseModel with kwargs set to None"""
        kwargs = {None: None}
        with self.assertRaises(TypeError):
            instance = self.model_class(**kwargs)

    def test_kwargs_one(self):
        """Test instantiation of BaseModel with one argument in kwargs"""
        kwargs = {'name': 'test'}
        instance = self.model_class(**kwargs)
        self.assertEqual(instance.name, kwargs['name'])

    def test_id(self):
        """Test the id attribute of the BaseModel class"""
        instance = self.model_class()
        self.assertEqual(type(instance.id), str)

    def test_created_at(self):
        """Test the created_at attribute of the BaseModel class"""
        instance = self.model_class()
        self.assertEqual(type(instance.created_at), datetime)

    def test_updated_at(self):
        """Test the updated_at attribute of the BaseModel class"""
        instance = self.model_class()
        self.assertEqual(type(instance.updated_at), datetime)
        dict_representation = instance.to_dict()
        new_instance = BaseModel(**dict_representation)
        self.assertFalse(new_instance.created_at == new_instance.updated_at)
