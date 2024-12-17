class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f'<Author {self.name}>'
    
    @property
    def name(self):
        return self._name
    
    @name.setter 
    def name(self,value):
        
        if hasattr(self,"name"):
            AttributeError("Have to provide the name")
        else: 
            if isinstance(value,str):
                if len(value)>=0: 
                    self._name = value 
                else: 
                    ValueError ("The value has to be greater than 0 characters")
            else: 
                TypeError("The name has to be of name string")
        
    def create_author(self, cursor):
         # inserting a new author 
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (self._name,))
        self._id = cursor.lastrowid



    @classmethod
      # getting all authors
    def get_all_authors(cls, cursor):
        cursor.execute("SELECT * FROM authors")
        authors_data = cursor.fetchall()
        return [cls(id=row[0], name=row[1]) for row in authors_data]

    def articles(self, cursor):
        # getting all articles associated with a specific author
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self._id,))
        articles_data = cursor.fetchall()
        return articles_data

    def magazines(self, cursor):
         # getting all magazines associated with a specific author
        cursor.execute("""
            SELECT magazines.*
            FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        """, (self._id,))
        magazines_data = cursor.fetchall()
        return magazines_data

   
                
        
            
        
        
        
