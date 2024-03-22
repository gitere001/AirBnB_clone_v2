#!/usr/bin/python3
"""Module for unit tests of the State class"""

from tests.test_models.test_base_model import test_basemodel
from models.state import State
import os


class TestState(test_basemodel):
    """Test cases for the State class"""

    def __init__(self, *args, **kwargs):
        """Initialize the test class for State"""
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name(self):
        """Test the type of name attribute"""
        new = self.value()
        self.assertEqual(type(new.name), str if
                         os.getenv('HBNB_TYPE_STORAGE') != 'db' else
                         type(None))
