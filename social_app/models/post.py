from social_app.config.mysqlconnection import connectToMySQL


class Post:
    db_name = 'socialfinali'
    def __init__(self,data):
        self.id = data['id'],
        self.media = data['media'],
        self.caption = data['caption'],
        self.content = data['content'],
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at'],
        self.user_id = data['user_id']
    


    @classmethod
    def makeContent(cls,data):
        query = 'INSERT INTO posts ( media, caption,  user_id ) VALUES ( %(media)s, %(caption)s, %(user_id)s );'
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def deletePost(cls,data):
        query = 'DELETE FROM posts WHERE id = %(post_id)s and user_id = %(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query,data)



    @classmethod
    def addLike(cls, data):
        query= 'INSERT INTO likes (post_id, user_id) VALUES ( %(post_id)s, %(user_id)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def removeLike(cls, data):
        query= 'DELETE FROM likes WHERE post_id = %(post_id)s and user_id = %(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    

    @classmethod
    def removeComment(cls,data):
        query = 'DELETE FROM comments WHERE id = %(id)s and user_id = %(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    

    @classmethod
    def likeUnlike(cls,data):
        query = 'SELECT post_id as id FROM likes LEFT JOIN users ON likes.user_id = users.id WHERE user_id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        info = []
        for row in results:
            info.append(row['id'])
        return info


    @classmethod
    def komento(cls,data):
        query = 'INSERT INTO comments ( user_id, post_id, content ) VALUES ( %(user_id)s, %(post_id)s, %(content)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def getPosts(cls):
        query= 'SELECT posts.media, posts.id,posts.caption, users.username as creator_name, users.id as creator_id, count(likes.id) as likesNr, users.profile_pic, posts.created_at FROM posts LEFT JOIN users on posts.user_id = users.id LEFT JOIN likes on likes.post_id = posts.id GROUP BY posts.id ORDER BY created_at DESC;'
        results =  connectToMySQL(cls.db_name).query_db(query)
        posts= []
        if results:
            for row in results:
                idja = str(row['id'])
                query2 = 'SELECT comments.content, users.username, users.id as commenter, comments.id FROM comments LEFT JOIN users ON comments.user_id = users.id WHERE post_id = ' + idja 
                results2 = connectToMySQL(cls.db_name).query_db(query2)
                comments = []
                if results2:
                    for row2 in results2:
                        comments.append(row2)
                row['comments'] = comments
                posts.append(row)
            return posts
        return posts
    

    @classmethod
    def deletePost(cls,data):
        query1 = 'DELETE FROM posts WHERE posts.id = %(post_id)s;'
        result1 =  connectToMySQL(cls.db_name).query_db(query1, data)
        query2= 'DELETE FROM likes WHERE likes.post_id = %(post_id)s;'
        result2 =  connectToMySQL(cls.db_name).query_db(query2, data)
        query3 = 'DELETE FROM comments WHERE comments.post_id = %(post_id)s;'
        return connectToMySQL(cls.db_name).query_db(query3, data)


    @classmethod
    def getCommentByID(cls,data):
        query = 'SELECT * FROM comments WHERE comments.id = %(id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results[0]

    @classmethod
    def getPostById(cls,data):
        query = 'SELECT * FROM posts WHERE posts.id = %(post_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results[0]

    # @classmethod
    # def deleteAllLikes(cls, data):
    #     query= 'DELETE FROM likes WHERE likes.post_id = %(post_id)s;'
    #     return connectToMySQL(cls.db_name).query_db(query, data)
    

    # @classmethod
    # def deleteAllComments(cls,data):
    #     query = 'DELETE FROM comments WHERE comments.post_id = %(post_id)s;'
    #     return connectToMySQL(cls.db_name).query_db(query, data)

