class Search_Info:
    def __init__(self, year, loc, sess_type) -> None:
        self._year = year
        self._location = loc
        self._session_type = sess_type
        
    @property
    def year(self):
        return self._year
    
    @year.setter
    def year(self, new_val):
        self._year = new_val
    
    @property
    def location(self):
        return self._location
    
    @location.setter
    def location(self, new_val):
        self._location = new_val  
    
    @property
    def session_type(self):
        return self._session_type
    
    @session_type.setter
    def session_type(self, new_val):
        self._session_type = new_val  
    
    def __str__(self) -> str:
        return f'{self._year} "{self._location}" Grand Prix {self._session_type}'
