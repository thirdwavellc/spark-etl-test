import json


class EligibilityExporter:

    def __init__(self, entries, file_writer):
        self.entries = list(map(lambda entry: entry.__dict__, entries))
        self.content = json.dumps(self.entries, indent=2)
        self.file_writer = file_writer

    def export(self):
        self.file_writer.write(self.content)
