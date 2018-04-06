import os
import errno


class LocalFileDataWriter:

    def __init__(self, path):
        self.path = path

    def write(self, content):
        if not os.path.exists(os.path.dirname(self.path)):
            try:
                os.makedirs(os.path.dirname(self.path))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(self.path, 'w') as f:
            f.write(content)


class RemoteFileDataWriter:

    def __init__(self,sftp,path):
        self.path = path
        self.sftp = sftp

    def write(self,content):
        folder_path = "/".join(self.path.split('/')[:-1])
        if not self.dir_exists(self.sftp,folder_path):
            self.sftp.mkdir(folder_path)
        file = self.sftp.open(self.path,'w+')
        file.write(content)

    def dir_exists(self,sftp, path):
        try:
            sftp.stat(path)
        except (IOError, e):
            if e.errno == errno.ENOENT:
                return False
            raise
        else:
            return True
