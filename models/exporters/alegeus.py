from ..entries.alegeus import CensusEntry


class CensusExporter:

    def __init__(self, entries, file_writer):
        """Exporter object

        Note:

        Args:
            entries:list of custome EligibiltyEntry objects
            file_writer: takes any object from the destinations.py file (Ex: LocalFileDataWriter, LocalCsvWriter)
        """

        entry_dicts = list(map(lambda validator: validator.entry.to_alegeus_census_dict(), entries))
        self.entries = list(map(lambda entry: CensusEntry(entry), entry_dicts))
        self.errors =  list(map(lambda validator: validator.errors, entries))
        self.content = list(map(lambda entry: entry.to_dict(), self.entries))
        self.file_writer = file_writer

    def export(self):
        """Calls the write function of the file_writer attribute

        Args:
            None

        Yields:
            None (writes file)

        """
        self.file_writer.write(self.content)
