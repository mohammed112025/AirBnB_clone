#!/usr/bin/python3
"""
The `BaseModel` module.
"""
from datetime import datetime
from uuid import uuid4
import models


class BaseModel:
    """
    Class that defines all common attributes/methods for other classes.

    A parent class to take care of the initialization, serialization
    and deserialization of the future instances.

    Public instance attributes:
        - id (string): an id for each BaseModel instance
        - created_at (datetime): the datetime when an instance is created
        - updated_at (datetime): the last datetime when an instance is updated

    Public instance methods:
        - save(self): updates the public instance attribute updated_at with
        the current datetime
        - to_dict(self): returns a dictionary containing all keys/values of
        __dict__ of the instance
    """

    def __init__(self, *args, **kwargs):
        """Create a new instance of BaseModel and define its attributes."""

        if not kwargs:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)
        else:
            if kwargs.get("__class__"):
                del kwargs["__class__"]
            self.__dict__.update(kwargs)
            date_format = "%Y-%m-%dT%H:%M:%S.%f"
            self.created_at = datetime.strptime(self.created_at, date_format)
            self.updated_at = datetime.strptime(self.updated_at, date_format)

    def __str__(self):
        """Return the string representation of a BaseModel instance."""
        return f"[{type(self).__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Update the updated_at attribute with the current datetime."""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Create a dictionary representation of a BaseModel instance."""
        instance_dict = self.__dict__.copy()
        instance_dict["__class__"] = type(self).__name__
        date_format = "%Y-%m-%dT%H:%M:%S.%f"
        instance_dict["created_at"] = self.created_at.strftime(date_format)
        instance_dict["updated_at"] = self.updated_at.strftime(date_format)
        return instance_dict
