

class LocalFileData:
    """ Captures return data from modules that produce local files """

    def __init__(self, file_path, name):
        self.file_path = file_path
        self.name = name

    def __str__(self):
        return 'file_path={}, name={}'.format(self.file_path, self.name)