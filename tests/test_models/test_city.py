#!/usr/bin/python3
"""Module for unit tests of the City class"""

from tests.test_models.test_base_model import test_basemodel
from models.city import City
import os


class TestCity(test_basemodel):
    """Test cases for the City class"""

    def __init__(self, *args, **kwargs):
        """Initialize the test class for City"""
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def test_state_id(self):
        """Test the type of state_id attribute"""
        new = self.value()
        self.assertEqual(type(new.state_id), str if
                         os.getenv('HBNB_TYPE_STORAGE') != 'db' else
                         type(None))

    def test_name(self):
        """Test the type of name attribute"""
        new = self.value()
        self.assertEqual(type(new.name), str if
                         os.getenv('HBNB_TYPE_STORAGE') != 'db' else
                         type(None))
