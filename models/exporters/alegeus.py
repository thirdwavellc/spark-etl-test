from ..entries.alegeus import CensusEntry


class CensusExporter:

    def __init__(self, entries, file_writer):
        entry_dicts = list(map(lambda entry: entry.to_alegeus_census_dict(), entries))
        self.entries = list(map(lambda entry: CensusEntry(entry), entry_dicts))
        self.content = "\n".join(list(map(lambda entry: str(entry.to_content()), self.entries)))
        self.file_writer = file_writer

    def export(self):
        self.file_writer.write(self.content)
