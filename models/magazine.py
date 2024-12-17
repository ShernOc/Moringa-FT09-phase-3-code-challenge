from database.connection import get_db_connection

class Magazine:
    all = {}
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
        return f'<Magazine {self.name}>'
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self,value):
        if isinstance(value,int):
            TypeError("The id has to be an integer")
        self._id = value
        
    @property
    def name(self):
        return self._name 
    
    @name.setter
    def name (self,value):
        if isinstance(value,str):
            if 2< len(value)<16:
                self._name = value
            else: 
                ValueError ("The name has to be greater than 2 and less than 16 characters")
        else: 
                TypeError("The name has to be of name string")
    @property
    def category(self):
        return self._category
        
    @category.setter    
    def category(self,value):
        if isinstance(value,str):
            if len(value)>0:
                self._category = value
            else: 
                ValueError("The category  to be greater than 2 and less than 16 characters")
        else: 
                TypeError("The name has to be of name string")
                
    def save(self):
        CONN= get_db_connection()
        CURSOR = CONN.cursor()
        sql = """
            INSERT INTO magazines (name, category)
            VALUES (?,?)
        """
        CURSOR.execute(sql, (self.name, self.category))
        CONN.commit()
        
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    #creates a new entry in the database
    def create(cls, name, category):
        magazine = cls(name, category)
        magazine.save()
        return magazine
    
    def get_magazine_id(self):
        return self.id
    

    def articles(self):
        from models.article import Article
        CONN= get_db_connection()
        CURSOR = CONN.cursor()
        """retrieves and returns a list of articles in this magazine """
        sql = """
            SELECT ar.*
            FROM articles ar
            INNER JOIN magazines m ON ar.magazine = m.id
            WHERE m.id = ?
        """

        CURSOR.execute(sql, (self.id,))
        article_data = CURSOR.fetchall()

        articles = []
        for row in article_data:
            articles.append(Article(*row))

        return articles
    
    def contributors(self):
        from models.author import Author
        conn = get_db_connection()
        CURSOR = conn.cursor()
        """retrieves and returns a lst of authors who wrote articles in this magazine"""
        sql = """
            SELECT DISTINCT a.*
            FROM authors a
            INNER JOIN articles ar ON ar.author = a.id
            INNER JOIN magazines m on ar.magazine = m.id
            WHERE m.id = ?
        """

        CURSOR.execute(sql, (self.id,))
        author_data = CURSOR.fetchall()

        authors = []
        for row in author_data:
            authors.append(Author(*row))
        return authors
    
    def article_titles(self):
        conn = get_db_connection()
        CURSOR = conn.cursor()
        """
        Retrieves and returns a list of titles (strings) of all articles written for this magazine.
        Returns None if the magazine has no articles.
        """
        sql = """
            SELECT ar.title
            FROM articles ar
            INNER JOIN magazines m ON ar.magazine = m.id
            WHERE m.id = ?
        """

        CURSOR.execute(sql, (self.id,))
        article_data = CURSOR.fetchall()

        if not article_data:
            return None

        titles = [row[0] for row in article_data]
        return titles

    def contributing_authors(self):
        from models.author import Author
        conn = get_db_connection()
        CURSOR = conn.cursor()

        sql = """
            SELECT DISTINCT a.*
            FROM authors a
            INNER JOIN articles ar ON ar.author = a.id
            INNER JOIN magazines m on ar.magazine = m.id
            WHERE m.id = ?
            GROUP BY a.id
            HAVING COUNT(ar.id) > 2
        """

        CURSOR.execute(sql, (self.id,))
        author_data = CURSOR.fetchall()

        if not author_data:
            return None

        authors = []
        for row in author_data:
            authors.append(Author(*row)) 
        return authors
