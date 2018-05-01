import json


class EligibilityExporter:

    def __init__(self, entries, file_writer):
        """Exporter object

        Note:

        Args:
            entries:list of custome EligibiltyEntry objects
            file_writer: takes any object from the destinations.py file (Ex: LocalFileDataWriter, LocalCsvWriter)

        Attributes:
            entries_dic: dict
            content: str
            file_writer: filedatawriter object
        """

        self.content = json.dumps(entries, indent=2)
        self.file_writer = file_writer

    def export(self):
        """Calls the write function of the file_writer attribute

        Args:
            None

        Returns:
            None (writes file)

        """
        self.file_writer.write(self.content)
