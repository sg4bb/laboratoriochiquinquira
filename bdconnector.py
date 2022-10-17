import mysql.connector


class database :
    #inicializacion del metodo self
    def __init__(self):
        self.connection = mysql.connector.connect(user='root',password='', 
                                    host='localhost', database='userpassword'
        )

        self.cursor = self.connection.cursor()

        print("conexion establecida.")

    #metodo de consulta de usuarios
    def select_user(self,id):
        sql = 'SELECT id_user,user,password,user_privilege FROM user WHERE id_user = {}'.format(id)

        try:
            self.cursor.execute(sql) 
            user = self.cursor.fetchone()

            print("Id:", user[0])
            print("Username:", user[1])
            print("Password:", user[2])
            print("User privilege:", user[3])
        except Exception as error:
            raise

    #metodo de consulta de todos los usuarios
    def select_all_user(self):
        sql = 'SELECT id_user,user,password,user_privilege FROM user'

        try:
            self.cursor.execute(sql)
            users = self.cursor.fetchall()

            for user in users:
                print("Id:", user[0])
                print("Username:", user[1])
                print("Password:", user[2])
                print("User privilege:", user[3])
                print("___________\n")

        except Exception as error:
            raise
    
    #metodo para cambiar password
    def update_password(self, id, password):
        sql = "UPDATE user SET password='{}' WHERE id_user = {}".format(password, id)

        try:
            self.cursor.execute(sql)
            self.connection.commit() #Cambio permanente

        except Exception as error:
            raise 


    def close(self):
        self.connection.close()

database = database()
database.select_user(2)
database.update_password(2,'user321')
database.select_user(2)
database.close()
