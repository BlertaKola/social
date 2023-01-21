from social_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask import flash


class User:
    db_name = 'socialfinali'
    def __init__(self,data):
        self.id = data['id'],
        self.username = data['username'],
        self.email = data['email'],
        self.password = data['password'],
        self.profile_pic = data['profile_pic'],
        self.about = data['about'],
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at']



    @classmethod
    def addUser(cls,data):
        query = 'INSERT INTO users ( username, email, password ) VALUES ( %(username)s, %(email)s, %(password)s );'
        return connectToMySQL(cls.db_name).query_db(query,data)
    



    @classmethod
    def makeFriendRequest(cls,data):
        query = 'INSERT INTO friend_request ( loggedUser_id, receiver_id, status ) VALUES ( %(loggedUser_id)s, %(receiver_id)s, %(status)s);'
        return connectToMySQL(cls.db_name).query_db(query,data)




    @classmethod
    def getAllUsersToSendRequest(cls, data):
        query = 'SELECT u.* FROM   users u WHERE  u.id <> %(user_id)s AND  NOT EXISTS ( SELECT NULL FROM   friendships f WHERE ( f.friend_id = u.id AND f.loggedUser_id = %(user_id)s ) OR    ( f.friend_id = %(user_id)s AND f.loggedUser_id = u.id ));'
        results = connectToMySQL(cls.db_name).query_db(query,data)
        users = []
        if results:
            for row in results:
                users.append(row)
            return users
        return users





    
    @classmethod
    def getAllFriends(cls, data):
        query= 'SELECT users.id as user, users.username, users.profile_pic, friendships.id, friendships.friend_id, friendships.loggedUser_id FROM friendships   LEFT JOIN users ON (friendships.loggedUser_id = users.id or friendships.friend_id = users.id)  WHERE ((friendships.friend_id = %(user_id)s or friendships.loggedUser_id = %(user_id)s) and users.id != %(user_id)s);'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        friends = []
        if results:
            for row in results:
                friends.append(row)
            return friends
        return friends
    




    
    @classmethod
    def getNumberOfConnections(cls,data):
        query = 'SELECT  count(friendships.id) AS number FROM friendships WHERE friendships.loggedUser_id = %(user_id)s OR friendships.friend_id = %(user_id)s;'
        result = connectToMySQL(cls.db_name).query_db(query,data)
        return result[0]


    @classmethod
    def getAllRequestReceived(cls, data):
        query = 'SELECT friend_request.loggedUser_id, friend_request.receiver_id, friend_request.id, users.username, users.profile_pic, users.id as friendId FROM friend_request LEFT JOIN users on friend_request.loggedUser_id = users.id WHERE friend_request.receiver_id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query,data)
        users = []
        if results:
            for row in results:
                users.append(row)
            return users
        return users




    
    @classmethod
    def getSentRequest(cls, data):
        query='Select friend_request.receiver_id from friend_request LEFT JOIN users on friend_request.receiver_id = users.id WHERE friend_request.loggedUser_id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query,data)
        users = []
        if results:
            for row in results:
                users.append(row['receiver_id'])
            return users
        return users
    




    @classmethod
    def deleteRequest(cls, data):
        query = 'DELETE FROM friend_request WHERE receiver_id = %(receiver_id)s and loggedUser_id = (loggedUser_id);'
        return connectToMySQL(cls.db_name).query_db(query,data)




    @classmethod
    def searchUser(cls,data):
        query = 'SELECT * FROM users WHERE  username  LIKE %(username)s;'
        results = connectToMySQL(cls.db_name).query_db(query,data)
        users = []
        if results: 
            for row in results:
                users.append(row)
            return users
        return False




    @classmethod
    def getUserPosts(cls, data):
        query= 'SELECT posts.media, posts.id,posts.caption, users.username as creator_name, users.id as creator_id, count(likes.id) as likesNr,users.profile_pic, posts.created_at FROM posts LEFT JOIN users on posts.user_id = users.id LEFT JOIN likes on likes.post_id = posts.id  WHERE users.id = %(user_id)s GROUP BY posts.id;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        posts = []
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
    def getAllUsersEmail(cls):
        query = 'SELECT email FROM users;'
        results = connectToMySQL(cls.db_name).query_db(query)
        emails = []
        if results:
            for row in results:
                emails.append(row)
            return emails
        return emails
        


    @classmethod
    def approveRequest( cls, data):
        query = 'INSERT INTO friendships (loggedUser_id, friend_id) VALUES (%(loggedUser_id)s,%(friend_id)s);'
        result = connectToMySQL(cls.db_name).query_db(query,data)
        query2 = 'DELETE FROM friend_request WHERE loggedUser_id = %(friend_id)s and receiver_id = %(loggedUser_id)s;'
        return connectToMySQL(cls.db_name).query_db(query2,data)
    



    @classmethod
    def rejectRequest( cls, data):
        query = 'DELETE FROM friend_request WHERE loggedUser_id = %(loggedUser_id)s and receiver_id = %(receiver_id)s;'
        return connectToMySQL(cls.db_name).query_db(query,data)




    @classmethod
    def updateUserInfo(cls,data):
        query = 'UPDATE users SET username = %(username)s,  about = %(about)s WHERE users.id = %(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query,data)




    @classmethod
    def updateUserPhoto(cls,data):
        query = 'UPDATE users SET profile_pic = %(profile_pic)s WHERE users.id = %(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query,data)




    @classmethod
    def getUserByID(cls,data):
        query = 'SELECT * FROM users WHERE users.id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return results[0]




    @classmethod
    def getUserByEmail(cls,data):
        query = 'SELECT * FROM users WHERE users.email = %(email)s;'
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if results:
            return results[0]
        return False
    

    @staticmethod
    def validateUser(user):
        is_valid = True
        if len(user['username']) < 1:
            flash("Username is required to register!", 'username')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'emailRegister')
            is_valid = False 
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters long!", 'passwordRegister')
            is_valid = False
        return is_valid


