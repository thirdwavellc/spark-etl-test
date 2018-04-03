import os


class LocalFileDataWriter:

    def __init__(self, path):
        self.path = path

    def write(self, content):
        with open(self.path, 'w') as f:
            f.write(content)
