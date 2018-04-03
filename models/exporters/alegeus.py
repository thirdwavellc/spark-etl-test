import json
from ..entries.alegeus import CensusEntry


class CensusExporter:

    def __init__(self, entries, file_writer):
        # TODO: format this as EDI, not JSON
        self.entries = list(map(lambda entry: entry.__dict__, CensusEntry.from_eligibility_entries(entries)))
        self.content = json.dumps(self.entries, indent=2)
        self.file_writer = file_writer

    def export(self):
        self.file_writer.write(self.content)
