import json


class CensusEntry:

    def __init__(self, entry_dict):
        for key, value in entry_dict.items():
            setattr(self, key, value)

    # TODO: format this as EDI, not JSON
    def to_content(self):
        return json.dumps(self.__dict__)
