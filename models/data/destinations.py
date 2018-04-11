import os
import errno
import csv

class LocalFileDataWriter:

    def __init__(self, path):
        self.path = path

    """This object takes a file path parameter to where the file should be written

    Args:
        path (str): file path for file (including filename and extension)

    """

    def write(self, content):
        """Takes the current object and writes a file to the path provided

        Args:
            content:str

        Returns:
            None

        """
        if not os.path.exists(os.path.dirname(self.path)):
            try:
                os.makedirs(os.path.dirname(self.path))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(self.path, 'w') as f:
            f.write(content)

class LocalCsvWriter:

    def __init__(self,path):
        """This object takes a file path parameter to where the file should be written

        Args:
            path (str): file path for file (including filename and extension)

        """
        self.path = path

    def write(self,content):
        """Takes the current object and writes a file to the path provided

        Args:
            content:array of dictionaries

        Returns:
            None

        """
        if not os.path.exists(os.path.dirname(self.path)):
            try:
                os.makedirs(os.path.dirname(self.path))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        if (len(content)>0):
            with open(self.path,'w') as f:
                fieldnames = content[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for row in content:
                   writer.writerow(row)



class RemoteFileDataWriter:

    def __init__(self,sftp,path):
        """This object takes a file path parameter and sftp object

        Args:
            path (sftp): sftp paramiko object
            path (str): file path for file (including filename and extension)

        """
        self.path = path
        self.sftp = sftp

    def write(self,content):
        """Takes the current object and writes a file to the path provided

        Args:
            content:str

        Returns:
            None

        """
        folder_path = "/".join(self.path.split('/')[:-1])
        if not self.dir_exists(self.sftp,folder_path):
            self.sftp.mkdir(folder_path)
        file = self.sftp.open(self.path,'w+')
        file.write(content)

    def dir_exists(self,sftp, path):
        """Checks to see if the directory already exists or not

        Args:
            sftp: paramikot sftp object
            path: str

        Returns:
            True or False

        """
        try:
            sftp.stat(path)
        except (IOError, e):
            if e.errno == errno.ENOENT:
                return False
            raise
        else:
            return True
