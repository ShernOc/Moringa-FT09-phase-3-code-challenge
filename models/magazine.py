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
            self._id = value
        else:
            TypeError("The id has to be an integer")
        
        
    @property
    def name(self):
        return self._name 
    
    @name.setter
    def name (self,value):
        if isinstance(value,str) and 2<=len(value)<=16:
                self._name = value
        else: 
            ValueError ("The name has to be greater than 2 and less than 16 characters and must be a string")
      
    @property
    def category(self):
        return self._category
        
    @category.setter    
    def category(self,value):
        if isinstance(value,str) and len(value)>0:
            self._category = value
        else: 
            ValueError("The category  to be greater than 0 and of string type")
                
    def articles(self):
        from models.article import Article
        CONN= get_db_connection()
        CURSOR = CONN.cursor()
        sql = """
            SELECT articles.id,articles.title, articles.content, articles.author_id, articles.magazine_id
            FROM articles 
            WHERE articles.magazine_id = ?
        """

        CURSOR.execute(sql, (self._id,))
        article_data = CURSOR.fetchall()

        articles = []
        for row in article_data:
            articles.append(Article(*row))

        return articles
    
    def contributors(self):
        from models.author import Author
        conn = get_db_connection()
        CURSOR = conn.cursor()
        
        sql = """
            SELECT DISTINCT author.id, author.name
            FROM authors 
            JOIN articles ON author.id = articles.author_id
            WHERE articles.magazine_id = ?
        """

        CURSOR.execute(sql, (self._id,))
        author_data = CURSOR.fetchall()

        authors = []
        for row in author_data:
            authors.append(Author(*row))
        return authors
    
    def article_titles(self):
        from models.author import Author
        conn = get_db_connection()
        CURSOR = conn.cursor()
        
        sql = """
            SELECT article.title
            FROM articles 
            WHERE articles.magazine_id = ?
        """

        CURSOR.execute(sql, (self._id,))
        article_data = CURSOR.fetchall()

        if not article_data:
            return None

        titles = [row[0] for row in article_data]
        return titles

    def contributing_authors(self):
        conn = get_db_connection()
        CURSOR = conn.cursor()

        sql = """
            SELECT DISTINCT articles.id, articles.title, articles.content, articles.author_id, articles.magazine_id
            FROM authors_id
            INNER JOIN articles ar ON articles.author = article_id
            INNER JOIN magazines m on ar.magazine = mid
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

# #test 
# magazine1 = Magazine("Vogue", "Fashion", "life")
# magazine2 = Magazine("How to Kill a Mocking Bird", "Lifestyle")

# #contributing authors 
# print([author.name for author in magazine1.contributing_authors()])



