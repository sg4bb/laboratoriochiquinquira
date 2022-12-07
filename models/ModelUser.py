from .entities.User import User
import string


class ModelUser():

    # Usuario (Login y Register)

    # Metodo para logearse
    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT iduser, username, password, fullname FROM user_data
                    WHERE username = '{}'""".format(user.username)

            cursor.execute(sql)
            row = cursor.fetchone()

            if row != None:
                user = User(row[0], row[1], User.check_password(
                    row[2], user.password), row[3])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    # Metodo para registrar
    @classmethod
    def register(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = "INSERT INTO user_data (username, password, fullname, email, address, genre, cellphone, profile_pic) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')".format(
                user.username, user.password, user.fullname, user.email, user.address, user.genre, user.cellphone, user.profile_pic)

            cursor.execute(sql)
            cursor.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    # metodo para consultar el usuario que se registro
    @classmethod
    def consultidForPrivilege(self, db, username):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT iduser FROM user_data WHERE username = '{}'".format(
                username)

            cursor.execute(sql)
            row = cursor.fetchone()

            return row
        except Exception as ex:
            raise Exception(ex)

    # Metodo para registrar privilegios
    @classmethod
    def regprivilege(self, db, iduser):
        try:
            cursor = db.connection.cursor()
            sql = "INSERT INTO user_privilege (iduser, privilege) VALUES ('{}', 3)".format(
                iduser)

            cursor.execute(sql)
            cursor.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    # Metodo para UserMixin logeo.
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

    # Metodo para comprobar username.
    @classmethod
    def checkuser(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT iduser, username FROM user_data WHERE username = '{}'".format(
                user.username)

            cursor.execute(sql)
            row = cursor.fetchone()

            if row == None:
                return '1'
            else:
                return '0'
        except Exception as ex:
            raise Exception(ex)

    # Metodo para comprobar email.
    @classmethod
    def checkemail(self, db, email):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT iduser, username, email FROM user_data WHERE email = '{}'".format(
                email.email)

            cursor.execute(sql)
            row = cursor.fetchone()

            if row == None:
                return '1'
            else:
                return '0'
        except Exception as ex:
            raise Exception(ex)

    # Metodo para verificar Caracteres especiales.
    @classmethod
    def special_char(self, username):
        username = str(username)

        for i in username:
            if i in string.punctuation:
                return True
                break

        return False

    # Metodo para chequear el privilegio.
    @classmethod
    def checkprivilege(self, db, iduser):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT iduser, privilege FROM user_privilege WHERE iduser = '{}'".format(
                iduser)

            cursor.execute(sql)
            row = cursor.fetchone()

            return row
        except Exception as ex:
            raise Exception(ex)


# Examenes


    @classmethod
    def consultexam(self, db, iduser):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT fecexam, tipexam, globulos_rojos, globulos_blancos, emoglobina, hematocrito, plaquetas, vcm, hcm, chcm, docexam FROM examenes WHERE iduser = '{}' ORDER BY fecexam ASC".format(
                iduser)

            cursor.execute(sql)
            row = cursor.fetchall()

            return row
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def consultvalor(self, db, valor, iduser):
        try:
            cursor = db.connection.cursor()

            # si toca '1' desea filtrar Globulos Rojos.
            if valor == '1':
                print('llegue hasta aqui')
                sql = "SELECT fecexam, globulos_rojos FROM examenes WHERE iduser = '{}' ORDER BY fecexam ASC".format(
                    iduser)

            # si toca '2' desea filtrar globulos blancos.
            if valor == '2':
                sql = "SELECT fecexam, globulos_blancos FROM examenes WHERE iduser = '{}' ORDER BY fecexam ASC".format(
                    iduser)

            # si toca '3' desea filtrar Emoglobina.
            if valor == '3':
                sql = "SELECT fecexam, emoglobina FROM examenes WHERE iduser = '{}' ORDER BY fecexam ASC".format(
                    iduser)

            # si toca '4' desea filtrar hematocritos.
            if valor == '4':
                sql = "SELECT fecexam, hematocrito FROM examenes WHERE iduser = '{}' ORDER BY fecexam ASC".format(
                    iduser)

            # si toca '5' desea filtrar Plaquetas.
            if valor == '5':
                sql = "SELECT fecexam, plaquetas FROM examenes WHERE iduser = '{}' ORDER BY fecexam ASC".format(
                    iduser)

            # si toca '6' desea filtrar VCM.
            if valor == '6':
                sql = "SELECT fecexam, vcm FROM examenes WHERE iduser = '{}' ORDER BY fecexam ASC".format(
                    iduser)

            # si toca '7' desea filtrar HCM.
            if valor == '7':
                sql = "SELECT fecexam, hcm FROM examenes WHERE iduser = '{}' ORDER BY fecexam ASC".format(
                    iduser)

            # si toca '6' desea filtrar CHCM.
            if valor == '8':
                sql = "SELECT fecexam, chcm FROM examenes WHERE iduser = '{}' ORDER BY fecexam ASC".format(
                    iduser)

            cursor.execute(sql)
            row = cursor.fetchall()

            return row
        except Exception as ex:
            raise Exception(ex)


# Solicitudes
    # Agregar


    @classmethod
    def newsolic(self, db, iduser, tipo, fecha, acotacion, status):
        try:
            cursor = db.connection.cursor()
            sql = "INSERT INTO citas_solic (iduser, tipexam, fecha_solic, acotaci_solic, statusnamesolic) VALUES ('{0}','{1}','{2}','{3}','{4}')".format(
                iduser, tipo, fecha, acotacion, status)

            cursor.execute(sql)
            cursor.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    # Consultar para la tabla normal usuario
    @classmethod
    def consultsolictable(self, db, iduser):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT numsolic, fecha_solic, tipexam, acotaci_solic FROM citas_solic WHERE iduser = '{}' AND statusnamesolic = '2' ORDER BY fecha_solic DESC".format(
                iduser)

            cursor.execute(sql)
            row = cursor.fetchall()

            return row
        except Exception as ex:
            raise Exception(ex)

    # Consultar para todas staff
    @classmethod
    def consultsolicstaff(self, db):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT `citas_solic`.`numsolic`, `user_data`.`fullname`, `citas_solic`.`fecha_solic`, `citas_solic`.`acotaci_solic`
                     FROM `citas_solic` 
	                    LEFT JOIN `user_data` ON `citas_solic`.`iduser` = `user_data`.`iduser`;"""

            cursor.execute(sql)
            row = cursor.fetchall()

            return row
        except Exception as ex:
            raise Exception(ex)

    # Borrar
    @classmethod
    def deletesolic(self, db, numsolic, iduser):
        try:
            cursor = db.connection.cursor()
            sql = "DELETE FROM citas_solic WHERE iduser = '{0}' AND numsolic = '{1}'".format(
                iduser, numsolic)

            cursor.execute(sql)
            cursor.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    # Consultar para editar
    @classmethod
    def consultsolicedit(self, db, numsolic, iduser):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT numsolic, fecha_solic, tipexam, acotaci_solic FROM citas_solic WHERE iduser = '{0}' AND numsolic = '{1}'".format(
                iduser, numsolic)

            cursor.execute(sql)
            row = cursor.fetchone()

            return row
        except Exception as ex:
            raise Exception(ex)

    # Updatear una solicitud de cita
    @classmethod
    def updatesolic(self, db, tipo, fecha, acotacion, numsolic, iduser):
        try:
            cursor = db.connection.cursor()
            sql = """
                UPDATE citas_solic
                SET tipexam       = '{0}',
                    fecha_solic   = '{1}',
                    acotaci_solic = '{2}'
                WHERE iduser = '{3}' 
                AND   numsolic = '{4}'
            """.format(tipo, fecha, acotacion, iduser, numsolic)

            cursor.execute(sql)
            cursor.connection.commit()
        except Exception as ex:
            raise Exception(ex)


# Citas agendadas
    # Consultar


    @classmethod
    def citasagendConsult(self, db, iduser):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT fecha, tipexam, status FROM citas_agend WHERE iduser = '{}' ORDER BY fecha DESC".format(
                iduser)

            cursor.execute(sql)
            row = cursor.fetchall()

            return row
        except Exception as ex:
            raise Exception(ex)
