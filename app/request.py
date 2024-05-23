class Request:
    def __init__(self, http_method: str, path: str, http_version: str) -> None:
        self._http_method = http_method 
        self._path = path 
        self._http_version = http_version 


    @property
    def http_method(self):
"""The http_method property."""
        return self._http_method
    
    @http_method.setter
    def http_method(self, value):
        self._http_method = value


    @property
    def path(self):
        """The path property."""
        return self._path
    
    @path.setter
    def path(self, value):
        self._path = value
        

    @property
    def http_version(self):
        """The http_version property."""
        return self._http_version


    @http_version.setter
    def http_version(self, value):
        self._http_version = value


 

    def __str__(self) -> None:
        str = f'Http Method: {self._http_method}\n'
        str += f'Request path: {self._path}\n'
        str += f'Http Version: {self._http_version}'

        return str


    def has_directory(self, directory: str, first_directory: bool = False) -> bool:
        
        if first_directory:
            if self.path.startswith(directory):
                return True

        if directory in self.path:
            return True

        return False
