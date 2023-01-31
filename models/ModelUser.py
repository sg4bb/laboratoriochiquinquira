from .entities.User import User
import string
from datetime import datetime
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
            sql = "SELECT fecexam, tipexam, globulos_rojos, globulos_blancos, emoglobina, hematocrito, plaquetas, vcm, hcm, chcm, doc FROM examenes WHERE iduser = '{}' ORDER BY fecexam ASC".format(
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
	                    LEFT JOIN `user_data` ON `citas_solic`.`iduser` = `user_data`.`iduser` WHERE `citas_solic`.`statusnamesolic` = 2;"""

            cursor.execute(sql)
            row = cursor.fetchall()

            return row
        except Exception as ex:
            raise Exception(ex)

    # Consultar para todas staff Con usuario
    @classmethod
    def consultsolicstaffus(self, db, numsolic):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT `citas_solic`.`numsolic`, `user_data`.`fullname`, `citas_solic`.`fecha_solic`, `citas_solic`.`acotaci_solic`, `user_data`.`iduser`
                     FROM `citas_solic` 
	                    LEFT JOIN `user_data` ON `citas_solic`.`iduser` = `user_data`.`iduser` WHERE `citas_solic`.`statusnamesolic` = 2 AND `citas_solic`.`numsolic` = {};""".format(numsolic)

            cursor.execute(sql)
            row = cursor.fetchone()

            return row
        except Exception as ex:
            raise Exception(ex)

        # Updatear una solicitud de cita
    @classmethod
    def updatesolicStaff(self, db, tipo, fecha, acotacion, numsolic, iduser):
        try:
            cursor = db.connection.cursor()
            sql = """
                UPDATE citas_solic
                SET tipexam       = '{0}',
                    fecha_solic   = '{1}',
                    acotaci_solic = '{2}',
                    iduser        = '{3}' 
                WHERE   numsolic = '{4}'
            """.format(tipo, fecha, acotacion, iduser, numsolic)

            cursor.execute(sql)
            cursor.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def checksolic(self, db, numsolic):
        try:
            cursor = db.connection.cursor()
            sql = "UPDATE citas_solic SET statusnamesolic = '3' WHERE numsolic = '{}'".format(numsolic)

            cursor.execute(sql)
            cursor.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def delsolic(self, db, numsolic):
        cursor = db.connection.cursor()
        sql = "DELETE FROM citas_solic WHERE numsolic = '{0}'".format(numsolic)
        try:
            cursor.execute(sql)
            cursor.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    # Consulta de usuarios solicitudes
    @classmethod
    def consultusersolic(self, db):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT `user_data`.`fullname`, `user_data`.`iduser`
                     FROM `user_data` 
	                    LEFT JOIN `user_privilege` ON `user_data`.`iduser` = `user_privilege`.`iduser` WHERE `user_privilege`.`privilege` = 3;
            """

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

    
    #   Examenes para card
    @classmethod 
    def examlastpac(self, db, iduser):
        try:
            cursor = db.connection.cursor()

            sql = "SELECT fecexam, globulos_rojos , globulos_blancos, emoglobina , hematocrito, plaquetas, vcm, hcm, chcm FROM examenes WHERE iduser = '{}' ORDER BY numexam DESC".format(iduser)

            cursor.execute(sql)
            row = cursor.fetchall()

            return row
        except Exception as ex:
            raise Exception(ex)





# -- Examenes

    #Usuario



    #Staff y administrador



        #1- Vista Consulta todos los examenes
    @classmethod
    def consultexam_staff(self, db):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT `examenes`.`numexam`, `examenes`.`fecexam`, `examenes`.`tipexam`, `examenes`.`numcita`, `user_data`.`fullname`, `examenes`.`globulos_rojos`, `examenes`.`globulos_blancos`, `examenes`.`emoglobina`, `examenes`.`hematocrito`, `examenes`.`plaquetas`, `examenes`.`vcm`, `examenes`.`hcm`, `examenes`.`chcm`, `examenes`.doc
                     FROM `examenes` 
	                    LEFT JOIN `user_data` ON `user_data`.`iduser` = `examenes`.`iduser`;
            """

            cursor.execute(sql)
            row = cursor.fetchall()

            return row
        except Exception as ex:
            raise Exception(ex)

            #1.1 - Consultar citas
    @classmethod
    def consultcitas_staff(self, db, numsolic):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT `citas_agend`.`fecha`, `user_data`.`fullname`, `citas_agend`.`numcita`, `citas_solic`.`acotaci_solic`
                    FROM `citas_agend`
	                    LEFT JOIN `citas_solic` ON `citas_agend`.`iduser` = `citas_solic`.`iduser`
	                    LEFT JOIN `user_data` ON `citas_agend`.`iduser` = `user_data`.`iduser`
                    WHERE `citas_solic`.`numsolic` = `citas_agend`.`numsolic` AND `citas_agend`.`numcita` = '{0}'
            """.format(numsolic)

            cursor.execute(sql)
            row = cursor.fetchall()

            return row
        except Exception as ex:
            raise Exception(ex)

            #1.2 - Consultar documentos para descarga.
    @classmethod
    def consultdocs_staff(self, db, numdoc):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT name_doc, file_doc FROM doc_examenes WHERE id_doc = '{}';".format(numdoc)

            cursor.execute(sql)
            row = cursor.fetchone()

            return row
        except Exception as ex:
            raise Exception(ex)



            #1.3 - Filtrado
    #1.3.1 - Consultar usuarios 
    @classmethod
    def consultusers_staff(self, db):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT `user_data`.`iduser` , `user_data`.`fullname` 
                      FROM `user_data` 
	                    LEFT JOIN `user_privilege` ON `user_privilege`.`iduser` = `user_data`.`iduser` WHERE `user_privilege`.`privilege` = '3';"""
            
            cursor.execute(sql)
            row = cursor.fetchall()

            return row
        except Exception as ex:
            raise Exception(ex)

    #1.3.2 - Consulta particular de las peticiones

        #a. Consulta de citas del usuario ()
    @classmethod
    def consultcituser_staff(self, db, iduser):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT `examenes`.`numexam`, `examenes`.`fecexam`, `examenes`.`tipexam`, `examenes`.`numcita`, `user_data`.`fullname`, `examenes`.`globulos_rojos`, `examenes`.`globulos_blancos`, `examenes`.`emoglobina`, `examenes`.`hematocrito`, `examenes`.`plaquetas`, `examenes`.`vcm`, `examenes`.`hcm`, `examenes`.`chcm`, `examenes`.`doc`
                     FROM `examenes` 
	                    LEFT JOIN `user_data` ON `user_data`.`iduser` = `examenes`.`iduser` WHERE `user_data`.`iduser` = '{}';""".format(iduser)

            cursor.execute(sql)
            row = cursor.fetchall()

            return row
        except Exception as ex:
            raise Exception(ex)


        #b. Consulta de citas fechas entre ambas Fec MaxMin
    @classmethod
    def consultcitfec_staff(self, db, fecmin, fecmax):
        try:
            cursor = db.connection.cursor()

            if (fecmin and fecmax) != None:
                if (datetime.strptime(fecmin,'%Y/%m/%d')) > (datetime.strptime(fecmax,'%Y/%m/%d')):
                    aux = fecmax
                    fecmax = fecmin
                    fecmin = aux

                sql = """SELECT `examenes`.`numexam`, `examenes`.`fecexam`, `examenes`.`tipexam`, `examenes`.`numcita`, `user_data`.`fullname`, `examenes`.`globulos_rojos`, `examenes`.`globulos_blancos`, `examenes`.`emoglobina`, `examenes`.`hematocrito`, `examenes`.`plaquetas`, `examenes`.`vcm`, `examenes`.`hcm`, `examenes`.`chcm`, `examenes`.`doc`
                         FROM `examenes` 
                            LEFT JOIN `user_data` ON `user_data`.`iduser` = `examenes`.`iduser` WHERE `examenes`.`fecexam` BETWEEN '{0}' AND '{1}';""".format(fecmin, fecmax)
            else:
                if fecmin is None:
                    sql = """SELECT `examenes`.`numexam`, `examenes`.`fecexam`, `examenes`.`tipexam`, `examenes`.`numcita`, `user_data`.`fullname`, `examenes`.`globulos_rojos`, `examenes`.`globulos_blancos`, `examenes`.`emoglobina`, `examenes`.`hematocrito`, `examenes`.`plaquetas`, `examenes`.`vcm`, `examenes`.`hcm`, `examenes`.`chcm`, `examenes`.`doc`
                            FROM `examenes` 
                                LEFT JOIN `user_data` ON `user_data`.`iduser` = `examenes`.`iduser` WHERE `examenes`.`fecexam` < '{}';""".format(fecmax)
                else:
                    sql = """SELECT `examenes`.`numexam`, `examenes`.`fecexam`, `examenes`.`tipexam`, `examenes`.`numcita`, `user_data`.`fullname`, `examenes`.`globulos_rojos`, `examenes`.`globulos_blancos`, `examenes`.`emoglobina`, `examenes`.`hematocrito`, `examenes`.`plaquetas`, `examenes`.`vcm`, `examenes`.`hcm`, `examenes`.`chcm`, `examenes`.`doc`
                             FROM `examenes` 
                                LEFT JOIN `user_data` ON `user_data`.`iduser` = `examenes`.`iduser` WHERE `examenes`.`fecexam` > '{}';""".format(fecmin)
                
            cursor.execute(sql)
            row = cursor.fetchall()

            return row
        except Exception as ex:
            raise Exception(ex)
        
        #c. Consulta de citas fechas con usuario
    @classmethod
    def consultcitfecU_staff(self, db, iduser, fecmin, fecmax):
        try:
            cursor = db.connection.cursor()

            if fecmin and fecmax != None:
                if (datetime.strptime(fecmin,'%Y/%m/%d')) > (datetime.strptime(fecmax,'%Y/%m/%d')):
                    aux = fecmax
                    fecmax = fecmin
                    fecmin = aux

                sql = """SELECT `examenes`.`numexam`, `examenes`.`fecexam`, `examenes`.`tipexam`, `examenes`.`numcita`, `user_data`.`fullname`, `examenes`.`globulos_rojos`, `examenes`.`globulos_blancos`, `examenes`.`emoglobina`, `examenes`.`hematocrito`, `examenes`.`plaquetas`, `examenes`.`vcm`, `examenes`.`hcm`, `examenes`.`chcm`, `examenes`.`doc`
                         FROM `examenes` 
	                        LEFT JOIN `user_data` ON `user_data`.`iduser` = `examenes`.`iduser` WHERE `examenes`.`iduser` = '{0}' AND `examenes`.`fecexam` BETWEEN '{1}' AND '{2}';""".format(iduser, fecmin, fecmax)
            else:
                if fecmin is None:
                    sql = """SELECT `examenes`.`numexam`, `examenes`.`fecexam`, `examenes`.`tipexam`, `examenes`.`numcita`, `user_data`.`fullname`, `examenes`.`globulos_rojos`, `examenes`.`globulos_blancos`, `examenes`.`emoglobina`, `examenes`.`hematocrito`, `examenes`.`plaquetas`, `examenes`.`vcm`, `examenes`.`hcm`, `examenes`.`chcm`, `examenes`.`doc`
                            FROM `examenes` 
                                LEFT JOIN `user_data` ON `user_data`.`iduser` = `examenes`.`iduser` WHERE `examenes`.`iduser` = '{0}' AND `examenes`.`fecexam` < '{1}';""".format(iduser, fecmax)
                else:
                    sql = """SELECT `examenes`.`numexam`, `examenes`.`fecexam`, `examenes`.`tipexam`, `examenes`.`numcita`, `user_data`.`fullname`, `examenes`.`globulos_rojos`, `examenes`.`globulos_blancos`, `examenes`.`emoglobina`, `examenes`.`hematocrito`, `examenes`.`plaquetas`, `examenes`.`vcm`, `examenes`.`hcm`, `examenes`.`chcm`, `examenes`.`doc`
                            FROM `examenes` 
                                LEFT JOIN `user_data` ON `user_data`.`iduser` = `examenes`.`iduser` WHERE `examenes`.`iduser` = '{0}' AND `examenes`.`fecexam` > '{1}';""".format(iduser, fecmin)

            cursor.execute(sql)
            row = cursor.fetchall()

            return row
        except Exception as ex:
            raise Exception(ex)





        #2 Insertar examenes 
    # Insertar documento
    @classmethod
    def adddocexam_staff(self, db, namenewdoc, datanewdoc):
        try:
            cursor = db.connection.cursor()

            sql = "INSERT INTO doc_examenes (name_doc, file_doc) VALUES (%s, %s)"

            cursor.execute(sql, (namenewdoc, datanewdoc))
            cursor.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    # insertar valores
    @classmethod
    def addexam_staff(self, db, paciente, tipo, cita, fecha, gr, gb, emoglobina, hematocritos, plaquetas, vcm, hcm, chcm, id_doc):
        try:
            cursor = db.connection.cursor()
            

            sql1 = "INSERT INTO `examenes` (`iduser`, `tipexam`, `numcita`, `fecexam`, `globulos_rojos`, `globulos_blancos`, `emoglobina`, `hematocrito`, `plaquetas`, `vcm`, `hcm`, `chcm`, `doc`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"   
           

            cursor.execute(sql1, (paciente, tipo, cita, fecha, gr, gb, emoglobina, hematocritos, plaquetas, vcm, hcm, chcm, id_doc))
            cursor.connection.commit()

            sql2 = "UPDATE citas_agend SET status = '2' WHERE numcita = '{}'".format(cita)

            cursor.execute(sql2)
            cursor.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    #2.1 Sub-Bloque consultas
    
        # a. Pacientes
    @classmethod
    def consultpacexam_staff(self, db):
        try:
            cursor = db.connection.cursor()

            sql = """SELECT `user_data`.`iduser` , `user_data`.`fullname` 
                     FROM `user_data`
	                    LEFT JOIN `citas_agend` ON `user_data`.`iduser` = `citas_agend`.`iduser` WHERE `citas_agend`.`status` = '1'; """
            
            cursor.execute(sql)
            row = cursor.fetchall()

            return row
        except Exception as ex:
            raise Exception(ex)


        # b. Citas
    @classmethod
    def consultcitexam_staff(self, db):
        try:
            cursor = db.connection.cursor()

            sql = """SELECT `citas_agend`.`numcita`, `citas_agend`.`fecha` , `user_data`.`fullname`
                     FROM `user_data`
	                    LEFT JOIN `citas_agend` ON `user_data`.`iduser` = `citas_agend`.`iduser` WHERE `citas_agend`.`status` = '1'; """
            
            cursor.execute(sql)
            row = cursor.fetchall()

            return row
        except Exception as ex:
            raise Exception(ex)

        # c. Documento 
    @classmethod
    def consultdocexam_staff(self, db, namedoc):
        try:
            cursor = db.connection.cursor()

            sql = "SELECT id_doc FROM doc_examenes WHERE name_doc = '{}' ORDER BY id_doc DESC".format(namedoc)

            cursor.execute(sql)
            row = cursor.fetchone()

            return row
        except Exception as ex:
            raise Exception(ex)


        #3 - Borrar examen
    @classmethod
    def delexam_staff(self, db, numexam):
        try:
            cursor = db.connection.cursor()

            sql = "DELETE FROM examenes WHERE numexam = '{}'".format(numexam)

            cursor.execute(sql)
            cursor.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    
        #4 Editar

    # a. consulta de examen a editar
    @classmethod
    def consultexamedit_staff(self, db, numexam):
        try:
            cursor = db.connection.cursor()

            sql = """SELECT `examenes`.`numexam`, `examenes`.`iduser`, `user_data`.`fullname`, `examenes`.`numcita`, `citas_agend`.`fecha`,`examenes`.`tipexam`, `examenes`.`fecexam`, `examenes`.`globulos_rojos`, `examenes`.`globulos_blancos`, `examenes`.`emoglobina`, `examenes`.`hematocrito`, `examenes`.`plaquetas`, `examenes`.`vcm`, `examenes`.`hcm`, `examenes`.`chcm`, `examenes`.`doc`
                     FROM `examenes`
	                    LEFT JOIN `user_data` ON `examenes`.`iduser` = `user_data`.`iduser`
                        LEFT JOIN `citas_agend` ON `examenes`.`numcita` = `citas_agend`.`numcita`
                            WHERE `examenes`.`numexam` = '{}'""".format(numexam)

            cursor.execute(sql)
            row = cursor.fetchone()

            return row
        except Exception as ex:
            raise Exception(ex)

    # consultar citas con status ya realizadas
    @classmethod
    def consultcitcomp_staff(self, db):
        try:
            cursor = db.connection.cursor()

            sql = """SELECT `citas_agend`.`numcita`, `citas_agend`.`fecha` , `user_data`.`fullname`
                     FROM `user_data`
	                    LEFT JOIN `citas_agend` ON `user_data`.`iduser` = `citas_agend`.`iduser` WHERE `citas_agend`.`status` = '2' ORDER BY `citas_agend`.`fecha` DESC;"""
            
            cursor.execute(sql)
            row = cursor.fetchall()

            return row
        except Exception as ex:
            raise Exception(ex)

    # consultar examen
    @classmethod
    def consultnumdoc_staff(self, db, numexam):
        try:
            cursor = db.connection.cursor()

            sql = "SELECT doc FROM examenes WHERE numexam = '{}'".format(numexam)

            cursor.execute(sql)
            row = cursor.fetchone()

            return row
        except Exception as ex:
            raise Exception(ex)

    # actualizar registro

        #a. sin documento
    @classmethod
    def updtexam_valores_staff(self, db, numexam, paciente, tipo, cita, fecha, gr, gb, emoglobina, hematocritos, plaquetas, vcm, hcm, chcm, doc):
        try:
            cursor = db.connection.cursor()

            if doc is None:
                sql = """UPDATE examenes SET iduser = '{0}', tipexam = '{1}', numcita = '{2}', fecexam = '{3}', globulos_rojos = '{4}', globulos_blancos = '{5}',
                emoglobina = '{6}', hematocrito = '{7}', plaquetas = '{8}', vcm = '{9}', hcm = '{10}', chcm = '{11}'
                WHERE numexam = '{12}'""".format(paciente, tipo, cita, fecha, gr, gb, emoglobina, hematocritos, plaquetas, vcm, hcm, chcm, numexam)
            else:
                sql = """UPDATE examenes SET iduser = '{0}', tipexam = '{1}', numcita = '{2}', fecexam = '{3}', globulos_rojos = '{4}', globulos_blancos = '{5}',
                emoglobina = '{6}', hematocrito = '{7}', plaquetas = '{8}', vcm = '{9}', hcm = '{10}', chcm = '{11}', doc = '{12}'
                WHERE numexam = '{13}'""".format(paciente, tipo, cita, fecha, gr, gb, emoglobina, hematocritos, plaquetas, vcm, hcm, chcm, doc, numexam)

            cursor.execute(sql)
            cursor.connection.commit()
        except Exception as ex:
            raise Exception(ex)



        #b. actualizar documento -por ahora en pruebas- 
    # Sub bloque para actualizar el documento

        #Insertanddo el doc
    # @classmethod
    # def updtexam_doc_staff(self, db, namenewdoc, datanewdoc):
    #     try:
    #         cursor = db.connection.cursor()

    #         sql = "INSERT INTO doc_examenes (name_doc, file_doc) VALUES (%s, %s)"
            


    #         cursor.execute(sql, (namenewdoc, datanewdoc))
    #         cursor.connection.commit()
    #     except Exception as ex:
    #         raise Exception(ex)

        #Borrando el anterior
    @classmethod
    def delold_doc_staff(self, db, numdoc):
        try:
            cursor = db.connection.cursor()
            sql = "DELETE FROM doc_examenes WHERE id_doc = '{}'".format(numdoc)

            cursor.execute(sql)
            cursor.connection.commit()
        except Exception as ex:
            raise Exception(ex)




# -- Citas

    #Usuario



    #Staff y administrador



        #1- Vista Consulta todas las citas
    @classmethod
    def consultcit_staff(self, db):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT `citas_agend`.`numcita`, `citas_agend`.`fecha`, `citas_agend`.`tipexam`, `user_data`.`fullname`, `citas_agend`.`numsolic`, `citas_agend`.`status`
                     FROM `citas_agend`
	                    LEFT JOIN `user_data` ON `citas_agend`.`iduser` = `user_data`.`iduser` ORDER BY `citas_agend`.`numcita` DESC"""

            cursor.execute(sql)
            row = cursor.fetchall()

            return row
        except Exception as ex:
            raise Exception(ex)

        #1.1 - Consulta Solicitud para Modal
    @classmethod
    def consultsolicmodal_staff(self, db, numsolic):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT `citas_solic`.`numsolic` , `user_data`.`fullname`, `citas_solic`.`fecha_solic`, `citas_solic`.`acotaci_solic`, `citas_solic`.`statusnamesolic`
                     FROM `citas_solic`
	                    LEFT JOIN `user_data` ON `citas_solic`.`iduser` = `user_data`.`iduser` WHERE `citas_solic`.`numsolic` = '{}'""".format(numsolic)
            
            cursor.execute(sql)
            row = cursor.fetchall()

            return row
        except Exception as ex:
            raise Exception(ex)


    #Sub bloque de filtrados
        #Consulta solo por estado de cita
    @classmethod
    def concitS_staff(self, db, status):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT `citas_agend`.`numcita`, `citas_agend`.`fecha`, `citas_agend`.`tipexam`, `user_data`.`fullname`, `citas_agend`.`numsolic`, `citas_agend`.`status`
                     FROM `citas_agend`
	                    LEFT JOIN `user_data` ON `citas_agend`.`iduser` = `user_data`.`iduser` WHERE `citas_agend`.`status` = '{}' ORDER BY `citas_agend`.`numcita` DESC""".format(status)
            
            cursor.execute(sql)
            row = cursor.fetchall()

            return row
        except Exception as ex:
            raise Exception(ex)

        #Consulta con fechas y estado de cita
    @classmethod
    def concitfecS_staff(self, db, status, fecmin, fecmax):
        try:
            cursor = db.connection.cursor()

            if fecmin and fecmax != None:
                if (datetime.strptime(fecmin,'%Y/%m/%d')) > (datetime.strptime(fecmax,'%Y/%m/%d')):
                    aux = fecmax
                    fecmax = fecmin
                    fecmin = aux
                
                sql = """SELECT `citas_agend`.`numcita`, `citas_agend`.`fecha`, `citas_agend`.`tipexam`, `user_data`.`fullname`, `citas_agend`.`numsolic`, `citas_agend`.`status`
                         FROM `citas_agend`
	                        LEFT JOIN `user_data` ON `citas_agend`.`iduser` = `user_data`.`iduser` WHERE `citas_agend`.`status` = '{0}' AND `citas_agend`.`fecha` BETWEEN '{1}' AND '{2}' ORDER BY `citas_agend`.`numcita` DESC""".format(status, fecmin, fecmax)
            else:
                if fecmin is None:
                    sql = """SELECT `citas_agend`.`numcita`, `citas_agend`.`fecha`, `citas_agend`.`tipexam`, `user_data`.`fullname`, `citas_agend`.`numsolic`, `citas_agend`.`status`
                             FROM `citas_agend`
	                            LEFT JOIN `user_data` ON `citas_agend`.`iduser` = `user_data`.`iduser` WHERE `citas_agend`.`status` = '{0}' AND `citas_agend`.`fecha` < '{1}' ORDER BY `citas_agend`.`numcita` DESC""".format(status, fecmax)
                else:
                    sql = """SELECT `citas_agend`.`numcita`, `citas_agend`.`fecha`, `citas_agend`.`tipexam`, `user_data`.`fullname`, `citas_agend`.`numsolic`, `citas_agend`.`status`
                             FROM `citas_agend`
	                            LEFT JOIN `user_data` ON `citas_agend`.`iduser` = `user_data`.`iduser` WHERE `citas_agend`.`status` = '{0}' AND `citas_agend`.`fecha` > '{1}' ORDER BY `citas_agend`.`numcita` DESC""".format(status, fecmin)

            cursor.execute(sql)
            row = cursor.fetchall()

            return row

        except Exception as ex:
            raise Exception(ex)

        # Consulta sin estado y con fecmin y fecmax
    @classmethod
    def concitfec_staff(self, db, fecmin, fecmax):
        try:
            cursor = db.connection.cursor()

            if fecmin and fecmax != None:
                if (datetime.strptime(fecmin,'%Y/%m/%d')) > (datetime.strptime(fecmax,'%Y/%m/%d')):
                    aux = fecmax
                    fecmax = fecmin
                    fecmin = aux
                
                sql = """SELECT `citas_agend`.`numcita`, `citas_agend`.`fecha`, `citas_agend`.`tipexam`, `user_data`.`fullname`, `citas_agend`.`numsolic`, `citas_agend`.`status`
                         FROM `citas_agend`
	                        LEFT JOIN `user_data` ON `citas_agend`.`iduser` = `user_data`.`iduser` WHERE `citas_agend`.`fecha` BETWEEN '{0}' AND '{1}' ORDER BY `citas_agend`.`numcita` DESC""".format(fecmin, fecmax)
            else:
                if fecmin is None:
                    sql = """SELECT `citas_agend`.`numcita`, `citas_agend`.`fecha`, `citas_agend`.`tipexam`, `user_data`.`fullname`, `citas_agend`.`numsolic`, `citas_agend`.`status`
                             FROM `citas_agend`
	                            LEFT JOIN `user_data` ON `citas_agend`.`iduser` = `user_data`.`iduser` WHERE `citas_agend`.`fecha` < '{}' ORDER BY `citas_agend`.`numcita` DESC""".format(fecmax)
                else:
                    sql = """SELECT `citas_agend`.`numcita`, `citas_agend`.`fecha`, `citas_agend`.`tipexam`, `user_data`.`fullname`, `citas_agend`.`numsolic`, `citas_agend`.`status`
                             FROM `citas_agend`
	                            LEFT JOIN `user_data` ON `citas_agend`.`iduser` = `user_data`.`iduser` WHERE `citas_agend`.`fecha` > '{}' ORDER BY `citas_agend`.`numcita` DESC""".format(fecmin)

            cursor.execute(sql)
            row = cursor.fetchall()

            return row

        except Exception as ex:
            raise Exception(ex)

    
        #2- Ingresar
    
    @classmethod
    def addcit_staff(self, db, idpac, solicitud, tipo, fecha):
        try:
            cursor = db.connection.cursor()

            sql = "INSERT INTO citas_agend (fecha, iduser, numsolic, status, tipexam) VALUES ('{0}', '{1}', '{2}', '1', '{3}')".format(fecha, idpac, solicitud, tipo)

            cursor.execute(sql)
            cursor.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    #Sub bloque de consultas 
        #Solicitudes recientes
    @classmethod
    def consultrensol_cit_staff(self, db):
        try:
            cursor = db.connection.cursor()

            sql = """SELECT `citas_solic`.`numsolic` , `user_data`.`fullname` , `citas_solic`.`fecha_solic` , `citas_solic`.`tipexam` , `citas_solic`.`acotaci_solic`
                     FROM `citas_solic`
	                    LEFT JOIN `user_data` ON `citas_solic`.`iduser` = `user_data`.`iduser` 
    	                    WHERE `citas_solic`.`statusnamesolic` = '2' ORDER BY `citas_solic`.`fecha_solic` ASC"""

            cursor.execute(sql)
            row = cursor.fetchall()

            return row
        except Exception as ex:
            raise Exception(ex)

        #Pacientes con solicitudes sin completar
    @classmethod
    def consultpacsol_cit_staff(self, db):
        try:
            cursor = db.connection.cursor()

            sql = """SELECT `citas_solic`.`iduser` , `user_data`.`fullname`
                     FROM `citas_solic`
	                    LEFT JOIN `user_data` ON `citas_solic`.`iduser` = `user_data`.`iduser` 
    	                    WHERE `citas_solic`.`statusnamesolic` = '2'"""

            cursor.execute(sql)
            row = cursor.fetchall()

            return row
        except Exception as ex:
            raise Exception(ex)

        #Fechas ocupadas por citas
    @classmethod
    def fecdisabled_cit_staff(self, db):
        try:
            cursor = db.connection.cursor()

            sql = "SELECT fecha FROM citas_agend WHERE status = '1'"

            cursor.execute(sql)
            row = cursor.fetchall()

            return row
        except Exception as ex:
            raise Exception(ex)
        

        #3- Editar

    @classmethod
    def updtcit_cit_staff(self, db, numcita, fecha, iduser, numsolic, status, tipexam):
        try:
            cursor = db.connection.cursor()

            sql = "UPDATE citas_agend SET fecha = '{0}', iduser = '{1}', numsolic = '{2}', status = '{3}', tipexam = '{4}' WHERE numcita = '{5}'".format(fecha, iduser, numsolic, status, tipexam, numcita)

            cursor.execute(sql)
            cursor.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    
    #Sub bloque de consultas

        #cita a editar
    @classmethod
    def consultcitedit_cit_staff(self, db, numcit):
        try:
            cursor = db.connection.cursor()

            sql = """SELECT `citas_agend`.`numcita`, `user_data`.`iduser`, `user_data`.`fullname`, `citas_agend`.`numsolic`, `citas_agend`.`tipexam`, `citas_agend`.`fecha`, `citas_agend`.`status`
                     FROM `citas_agend`
	                    LEFT JOIN `user_data` ON `citas_agend`.`iduser` = `user_data`.`iduser`
                        WHERE `citas_agend`.`numcita` = '{}'""".format(numcit)


            cursor.execute(sql)
            row = cursor.fetchone()

            return row
        except Exception as ex:
            raise Exception(ex)

        #solicitud de esa cita
    @classmethod
    def consulteditsol_cit_staff(self, db, numsol):
        try:
            cursor = db.connection.cursor()

            sql = """SELECT `citas_solic`.`numsolic` , `user_data`.`fullname` , `citas_solic`.`fecha_solic` , `citas_solic`.`tipexam` , `citas_solic`.`acotaci_solic`
                     FROM `citas_solic`
	                    LEFT JOIN `user_data` ON `citas_solic`.`iduser` = `user_data`.`iduser` 
    	                    WHERE `citas_solic`.`numsolic` = '{}' ORDER BY `citas_solic`.`fecha_solic`""".format(numsol)

            cursor.execute(sql)
            row = cursor.fetchone()

            return row
        except Exception as ex:
            raise Exception(ex)

    
        #Fechas ocupadas por citas excluyendo la que se editara
    @classmethod
    def fecdisablededit_cit_staff(self, db, numcit):
        try:
            cursor = db.connection.cursor()

            sql = "SELECT fecha FROM citas_agend WHERE status = '1' AND numcita <> '{}'".format(numcit)

            cursor.execute(sql)
            row = cursor.fetchall()

            return row
        except Exception as ex:
            raise Exception(ex)



        #4- Borrar
    @classmethod
    def delcit_cit_staff(self, db, numcita):
        try:
            cursor = db.connection.cursor()

            sql = "DELETE FROM citas_agend WHERE numcita = '{}'".format(numcita)

            cursor.execute(sql)
            cursor.connection.commit()
        except Exception as ex:
            raise Exception(ex)


        #5- Checkear cita
    @classmethod
    def checkcit_cit_staff(self, db, numcita):
        try:
            cursor = db.connection.cursor()

            sql = " UPDATE citas_agend SET status = '2' WHERE = '{}'".format(numcita)

            cursor.execute(sql)
            cursor.connection.commit()
        except Exception as ex:
            raise Exception(ex)



# -- Usuarios

    #Sub bloque de consultas

        #Correo ya registrado
    @classmethod
    def checkemail_admin(self, db, correo, iduser):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT iduser, username, email FROM user_data WHERE email = '{0}' AND iduser != '{1}'".format(correo, iduser)

            cursor.execute(sql)
            row = cursor.fetchone()

            if row == None:
                return '1'
            else:
                return '0'
        except Exception as ex:
            raise Exception(ex)

        #Username ya registrado
    @classmethod
    def checkuser_admin(self, db, user, iduser):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT username FROM user_data WHERE username = '{0}' AND iduser != '{1}'".format(user, iduser)

            cursor.execute(sql)
            row = cursor.fetchone()

            if row == None:
                return '1'
            else:
                return '0'
        except Exception as ex:
            raise Exception(ex)

        #Users para table
    @classmethod
    def consultusers_table(self, db):
        try:
            cursor = db.connection.cursor()
            
            sql = """SELECT `user_privilege`.`privilege`, `user_data`.`iduser`, `user_data`.`username`, `user_data`.`fullname`, `user_data`.`email`, `user_data`.`address`, `user_data`.`cellphone`
                     FROM `user_data` LEFT JOIN `user_privilege` ON `user_data`.`iduser` = `user_privilege`.`iduser` 
                        WHERE `user_privilege`.`privilege` = '3' OR `user_privilege`.`privilege` = '2';"""

            cursor.execute(sql)
            row = cursor.fetchall()

            return row
        except Exception as ex:
            raise Exception(ex)

        #User data para Modal
    @classmethod
    def consultdatauser(self, db, iduser):
        try:
            cursor = db.connection.cursor()

            sql = """SELECT `user_privilege`.`privilege`, `user_data`.`iduser`, `user_data`.`username`, `user_data`.`fullname`, `user_data`.`email`, `user_data`.`address`, `user_data`.`cellphone`
                     FROM `user_data` LEFT JOIN `user_privilege` ON `user_data`.`iduser` = `user_privilege`.`iduser` WHERE `user_data`.`iduser` = '{}'""".format(iduser)

            cursor.execute(sql)
            row = cursor.fetchall()

            return row
        except Exception as ex:
            raise Exception(ex)

    #Modificar

        #Permisos
    @classmethod
    def updtprivilege_admin(self, db, iduser, privilege):
        try:
            cursor = db.connection.cursor()

            sql = "UPDATE user_privilege SET privilege = '{0}' WHERE iduser = '{1}'".format(privilege, iduser)

            cursor.execute(sql)
            cursor.connection.commit()
        except Exception as ex:
            raise Exception(ex)

        #Datos
    @classmethod
    def updtdata_admin(self, db, iduser, username, nombre, correo, direccion, celular):
        try:
            cursor = db.connection.cursor()

            sql = "UPDATE user_data SET username = '{0}', fullname = '{1}', email = '{2}', address = '{3}', cellphone = '{4}' WHERE iduser = '{5}'".format(username, nombre, correo, direccion, celular, iduser)

            cursor.execute(sql)
            cursor.connection.commit()
        except Exception as ex:
            raise Exception(ex)


    #Borrar
    @classmethod
    def deleteuserdata_admin(self, db, iduser):
        try:
            cursor = db.connection.cursor()

            sql = "DELETE FROM citas_solic WHERE iduser = '{}'".format(iduser)
            cursor.execute(sql)

            sql = "DELETE FROM citas_agend WHERE iduser = '{}'".format(iduser)
            cursor.execute(sql)

            sql = "DELETE FROM examenes WHERE iduser = '{}'".format(iduser)
            cursor.execute(sql)

            sql = "DELETE FROM user_privilege WHERE iduser = '{}'".format(iduser)
            cursor.execute(sql)

            sql = "DELETE FROM user_data WHERE iduser = '{}'".format(iduser)
            cursor.execute(sql)

            cursor.connection.commit()

        except Exception as ex:
            raise Exception(ex)


    #Ingresar

        #Datos
    @classmethod
    def gestuseradd_data_admin(self, db, username, password, fullname, email, address, genre, cellphone, profile_pic):
        try:
            cursor = db.connection.cursor()

            sql = "INSERT INTO user_data (username, password, fullname, email, address, genre, cellphone, profile_pic) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"


            cursor.execute(sql, (username, password, fullname, email, address, genre, cellphone, profile_pic))

            cursor.connection.commit()
        except Exception as ex:
            raise Exception(ex)

        #Privilegio
    @classmethod
    def gestuseradd_privilege_admin(self, db, iduser, privilegio):
        try:
            cursor = db.connection.cursor()

            sql = "INSERT INTO user_privilege (iduser, privilege) VALUES ('{0}', '{1}')".format(iduser, privilegio)


            cursor.execute(sql)

            cursor.connection.commit()
        except Exception as ex:
            raise Exception(ex)


    # Sub-bloque de consultas

        #Usuario recien ingresado
    @classmethod
    def checkuser_addtwo_admin(self, db, username):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT iduser FROM user_data WHERE username = '{}'".format(username)

            cursor.execute(sql)
            row = cursor.fetchone()

            return row
        except Exception as ex:
            raise Exception(ex)


        #Chequeo de correo
    @classmethod
    def checkemail_add_admin(self, db, correo):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT iduser, username, email FROM user_data WHERE email = '{}'".format(correo)

            cursor.execute(sql)
            row = cursor.fetchone()

            if row == None:
                return '1'
            else:
                return '0'
        except Exception as ex:
            raise Exception(ex)

        #Username ya registrado
    @classmethod
    def checkuser_add_admin(self, db, username):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT username FROM user_data WHERE username = '{}'".format(username)

            cursor.execute(sql)
            row = cursor.fetchone()

            if row == None:
                return '1'
            else:
                return '0'
        except Exception as ex:
            raise Exception(ex)

        