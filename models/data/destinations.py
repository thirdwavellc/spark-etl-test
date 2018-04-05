import os
import errno


class LocalFileDataWriter:

    def __init__(self, path):
        self.path = path
        if not os.path.exists(os.path.dirname(self.path)):
            try:
                os.makedirs(os.path.dirname(self.path))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

    def write(self, content):
        with open(self.path, 'w') as f:
            f.write(content)
