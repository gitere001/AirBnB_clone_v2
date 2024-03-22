#!/usr/bin/python3
"""Module for unit tests of the User class"""

from tests.test_models.test_base_model import test_basemodel
from models.user import User


class TestUser(test_basemodel):
    """Test cases for the User class"""

    def __init__(self, *args, **kwargs):
        """Initialize the test class for User"""
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User

    def test_first_name(self):
        """Test the type of first_name attribute"""
        new = self.value()
        self.assertEqual(type(new.first_name), str)

    def test_last_name(self):
        """Test the type of last_name attribute"""
        new = self.value()
        self.assertEqual(type(new.last_name), str)

    def test_email(self):
        """Test the type of email attribute"""
        new = self.value()
        self.assertEqual(type(new.email), str)

    def test_password(self):
        """Test the type of password attribute"""
        new = self.value()
        self.assertEqual(type(new.password), str)
