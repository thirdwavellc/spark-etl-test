import json
import csv


class CensusEntry:

    def __init__(self, entry_dict):
        """Custom object created from a dictionary

        Notes:

        Args:
            entry_dict: dict (same as using **args)
        """
        for key, value in entry_dict.items():
            setattr(self, key, value)

    # TODO: format this as EDI, not JSON
    def to_json(self):
        """Takes the current object, get's a dictionary of the object attributes and converts to json format.

        Args:
            None

        Yields:
            str

        """
        print(type(json.dumps(self.__dict__)))
        return json.dumps(self.__dict__)

    def to_dict(self):
        """Takes the current object, and returns a dictionary of the obejcts attributes

        Args:
            None

        Yields:
            dict

        """
        return self.__dict__
