from database.connection import get_db_connection 

from models.magazine import Magazine
 

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
        if hasattr(self,"_title"):
            AttributeError("Have to provide the title ")
        else: 
            if isinstance(value,str):
                if 5<=len(value)<=50: 
                    self._title = value 
                else: 
                    ValueError ("The title has to be between 5 and 50 characters")
                    
                
    def magazine(self):
        if not hasattr(self, '_magazine'):
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = """
                SELECT magazines.id, magazines.name, magazines.category
                FROM magazines
                JOIN articles ON magazines.id = articles.magazine_id
                WHERE articles.id = ?
            """
            cursor.execute(sql, (self.id,))
            row = cursor.fetchone()
            if row:
                self._magazine = Magazine(row['id'], row['name'], row['category'])
        else:   
            return self._magazine

    def __repr__(self):
        return f'<Article {self.title}>'  
    


                
    
    

        
    
    
