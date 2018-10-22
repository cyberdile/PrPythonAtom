import os
import pickle as pkl

class FileWriter:
    
    def __init__(self, path):
        if self._check_path(path):
            self.path_ = path
            self.file = None

    def _check_path(self, path):
        return os.path.isdir(os.path.dirname(path))
            
    def __enter__(self):
        self.file = open(self.path_, 'a')
        return self
    
    def __exit__(self, exit_type, exit_value, exit_traceback):
        self.file.close()
        self.file = None
        
    @property        
    def path(self):
        return self.path_
    
    @path.getter
    def path(self):
        return self.path_
    
    @path.setter
    def path(self, value):
        if self._check_path(value):
            self.path_ = value
        
    @path.deleter
    def path(self):
        del self.path_

    def print_file(self):
        with open(self.path, 'r') as f:
            print(f.read())
    
    def write(self, some_string):
        if self.file is not None:
            self.file.write(some_string)
    
    def save_yourself(self, file_name):
        if self._check_path(file_name):
            with open(file_name, 'wb') as f:
                pkl.dump(self, f)
    
    @classmethod
    def load_file_writer(cls, pickle_file):
        if cls._check_path(cls, pickle_file):
            with open(pickle_file, 'rb') as f:
                return pkl.load(f)

