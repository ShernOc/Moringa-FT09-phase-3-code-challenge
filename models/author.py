from database.connection import get_db_connection  

from models.article import Article
from models.magazine import Magazine

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
            # else: 
            #     TypeError("The name has to be of name string")
                
    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
            SELECT articles.id, articles.title, articles.content, articles.author_id, articles.magazine_id 
            FROM articles
            JOIN magazines ON articles.magazine_id = magazines.id
            WHERE articles.author_id = ?
            """
        cursor.execute(sql, (self.id,))
        rows = cursor.fetchall()

        return [Article(row["id"], row["title"], row["content"], row["author_id"], row["magazine_id"]) for row in rows]
    
    def magazines(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
        SELECT magazines.id, magazines.name, magazines.category
        FROM magazines
        JOIN articles ON magazines.id = articles.magazine_id
        WHERE articles.author_id = ?
        """
        cursor.execute(sql, (self._id,))
        rows = cursor.fetchall()

        return [Magazine(row["id"], row["name"], row["category"]) for row in rows]

    def __repr__(self):
        return f'<Author {self.name}>'


#test 

author_1 = Author("Carry Bradshaw")
author_2 = Author("Nathaniel Hawthorne")

# magazine1 = Magazine("Vogue", "Fashion")
# magazine2 = Magazine("How to Kill a Mocking Bird", "Lifestyle")



article_1 = Article(author_1, "How to wear a tutu with style")
article_2 = Article(author_2,"Dating life in NYC")


# getting the magazine
print([mag.name for mag in author_1.magazines()])
