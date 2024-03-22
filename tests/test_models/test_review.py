#!/usr/bin/python3
"""Module for unit tests of the Review class"""

from tests.test_models.test_base_model import test_basemodel
from models.review import Review
import os


class TestReview(test_basemodel):
    """Test cases for the Review class"""

    def __init__(self, *args, **kwargs):
        """Initialize the test class for Review"""
        super().__init__(*args, **kwargs)
        self.name = "Review"
        self.value = Review

    def test_place_id(self):
        """Test the type of place_id attribute"""
        new = self.value()
        self.assertEqual(type(new.place_id), str if
                         os.getenv('HBNB_TYPE_STORAGE') != 'db' else
                         type(None))

    def test_user_id(self):
        """Test the type of user_id attribute"""
        new = self.value()
        self.assertEqual(type(new.user_id), str if
                         os.getenv('HBNB_TYPE_STORAGE') != 'db' else
                         type(None))

    def test_text(self):
        """Test the type of text attribute"""
        new = self.value()
        self.assertEqual(type(new.text), str if
                         os.getenv('HBNB_TYPE_STORAGE') != 'db' else
                         type(None))
