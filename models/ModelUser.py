from .entities.User import User
import string

class ModelUser():

        #Metodo para logearse
    @classmethod  
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT iduser, username, password, fullname FROM user_data
                    WHERE username = '{}'""".format(user.username)

            cursor.execute(sql)
            row = cursor.fetchone()

            if row != None:
                user = User(row[0], row[1], User.check_password(row[2], user.password), row[3])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    #Metodo para registrar
    @classmethod
    def register(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = "INSERT INTO user_data (username, password, fullname, email, address, genre, cellphone, profile_pic) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')".format(user.username,user.password,user.fullname,user.email,user.address,user.genre,user.cellphone,user.profile_pic)

            cursor.execute(sql)
            cursor.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    #Metodo para UserMixin logeo.
    @classmethod  
    def get_by_id(self, db, iduser):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT iduser, username, fullname FROM user_data
                    WHERE iduser = '{}'""".format(iduser)

            cursor.execute(sql)
            row = cursor.fetchone()

            if row != None:
                logged_user = User(row[0], row[1], None, row[2])
                return logged_user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    #Metodo para comprobar username.
    @classmethod
    def checkuser(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT iduser, username FROM user_data WHERE username = '{}'".format(user.username)

            cursor.execute(sql)
            row = cursor.fetchone()

            if row == None:
                return '1'
            else:
                return '0'
        except Exception as ex:
            raise Exception(ex)

    #Metodo para comprobar email.
    @classmethod
    def checkemail(self, db, email):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT iduser, username, email FROM user_data WHERE email = '{}'".format(email.email)

            cursor.execute(sql)
            row = cursor.fetchone()

            if row == None:
                return '1'
            else:
                return '0'
        except Exception as ex:
            raise Exception(ex)

    #Metodo para verificar Caracteres especiales.
    @classmethod
    def special_char(self, username):
        username = str(username)

        for i in username:
            if i in string.punctuation:
                return True
                break
            
        return False