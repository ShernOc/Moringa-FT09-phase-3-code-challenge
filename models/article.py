class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return f'<Article {self.title}>'
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self,value):
        if hasattr(self,"title"):
            AttributeError("Have to provide the title ")
        else: 
            if isinstance(value,str):
                if 5< len(value)<=50: 
                    self._title = value 
                else: 
                    ValueError ("The title has to be between 5 and 50 characters")
            else: 
                TypeError("The title has to be of name string")
                
    @property
    def magazine(self):
        return self._magazine
    

        
    
    
