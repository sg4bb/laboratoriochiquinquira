from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect

from config import config

# Herramienta para Imagenes y Comprobaciones.
import cv2

# Herramienta pa subir archivos.
from wtforms import FileField, SubmitField
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from io import BytesIO

# Herramienta para contraseñas
from werkzeug.security import check_password_hash, generate_password_hash

#Herramienta para convertir Dates a String
from datetime import datetime

#Herramienta para convertir tuplas
from functools import reduce

#Herramienta para convertir a JSON
import json

# Modelos
from models.ModelUser import ModelUser
# Entidades
from models.entities.User import User, NewUser, ConsultUser, ConsultEmail




app = Flask(__name__)

#CSRF Token
csrf = CSRFProtect()

# -- Configuraciones
db = MySQL(app)

# login manager
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(iduser):
    return ModelUser.get_by_id(db, iduser)




# -- Ruta Principal.
@app.route('/')
def home():
    return render_template('home-test.html')

# -- Rutas de Decoracion.
    # -- Ruta Acerca de
@app.route('/about')
def about():
    return render_template('about.html')

    # Ruta de Membresias




# -- Ruta para logearse
@app.route('/check_user', methods=['GET', 'POST'])
def check_user():
    if request.method == 'POST':
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)

        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('homeuser'))
            else:
                flash("Vaya.... Password invalido.", "danger")
                return redirect(url_for('login'))
        else:
            flash("Vaya.... Usuario no encontrado.", "danger")
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

    # Ruta Principal de Logeo.
@app.route('/login')
def login():
    return render_template('login-test.html')

    # Ruta de logout.
@app.route('/logout')
def logout():
    logout_user()
    return (redirect(url_for('home')))


# -- Ruta de redireccion para registro de nuevos usuarios
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':

        # Obtencion de las variables
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['firstname'] + ' ' + request.form['lastname']
        email = request.form['email']
        address  = request.form['ciudad'] + ', ' + request.form['sector'] + ', ' + request.form['calle']
        genre = request.form['genre']
        cellphone = request.form['suffix'] + '-' + request.form['cellphone']

        # Comprobacion de los valores. (Correctos.)

        # - Email

            # Formato correcto
        if email[email.find("@"):] not in ['@gmail.com', '@hotmail.com', '@outlook.com', '@hotmail.es']:
            flash("Vaya.... El email no está permitido.", 'danger')
            return redirect(url_for('register'))

        # --Username
        # Comprobando si tiene la longitud correcta.
        if (len(username) >= 4) and (len(username) <= 12):
            # Comprobando si existe en el username un caracter especial.
            # for i in username:
            #     if i in string.punctuation:
            #         flash("Vaya... Usuario no permitido. No puede contener caracteres especiales.")
            #         redirect(url_for('testregister'))
            tvalue = ModelUser.special_char(username)

            if tvalue is True:
                flash("Vaya...  Usuario no puede contener caracteres especiales.", "danger")
                return redirect(url_for('register'))

            # Si llego hasta aca significa que no tiene caracteres especiales y cumple en longitud.
                # Comprobando si existe ya en la base de datos
            user = ConsultUser(username)
            checkvalue = ModelUser.checkuser(db, user) 

            # Si retorna un 1 es que no existe el username, si retorna un 0 si existe.
            if checkvalue == '1':
                #--email
                    #Comprobacion de que el email no existe en la BD.
                emailt = ConsultEmail(email)
                checkvalue2 = ModelUser.checkemail(db, emailt)

                # Si retorna un 1 es que no existe el email, si retorna un 0 si existe.
                if checkvalue2 == '1':
                    profile_pic = cv2.imread('static/img/98681.jfif')
                    user = NewUser(0, username, password, fullname, email, address, genre, cellphone, profile_pic)
                    ModelUser.register(db, user)
                    ModelUser.regprivilege(db, ModelUser.consultidForPrivilege(db, user.username)[0])
                    flash('Bien!    Se ha registrado correctamente.', 'success')
                    return redirect(url_for('login'))
                else:
                    flash('Vaya...  Email ya registrado, usa otro.', 'danger')
                    return redirect(url_for('register'))
            else:
                flash('Vaya...  Usuario ya existente, intenta con otro.', 'danger')
                return redirect(url_for('register'))
        else:
            flash("Vaya.... Usuario no permitido. Debe tener entre 4 y 12 caracteres.", 'danger')
            return (redirect(url_for('register')))
    else:
        return (redirect(url_for('register')))

    # Ruta principal De Registro.
@app.route('/register')
def register():
    return render_template('register-test.html')





# -- Rutas a partir del login (PROTEGER RUTAS UNA VEZ FINALIZADO SU DISEÑO)

        # --Home 
@app.route('/home')
def homeuser():
    #Comprobacion de Permisos
    userprivilege = ModelUser.checkprivilege(db, current_user.get_id())

    #Renderizado de acuerdo a privilegios.

    if userprivilege[1] == 3:
        #Renderizado de plantilla Paciente.
        return render_template("home-user-test.html")
    elif userprivilege[1] == 2:
        #Renderizado de plantilla secretaria o Staff.
        return render_template("home-staff.html")
    else:
        #Renderizado de plantilla Admin.
        return render_template('home-admin.html')


    #Usuario

    #1 -- Gestionar Examenes
@app.route('/labtest', methods=['GET', 'POST'])
def labtest():
    form = UploadFileForm()

    if request.method == 'POST':
        # Metodo post para filtrado.

            #Obtencion del item que desea filtrar
        valor = request.form['filteroption']
        filtervalue = ModelUser.consultvalor(db, valor, current_user.get_id())

            #Obtener valores para la grafica.
                #Listas para la grafica.
        tablavaluex = []
        tablavaluey = []
        
                #Registrar valores en las listas.
        for i in filtervalue:
            tablavaluex.append(i[0].strftime('%d/%m/%Y'))
            tablavaluey.append(i[1])

        return render_template('labtest-filter.html', filters = filtervalue, valore = valor, 
        valoresX = json.dumps(tablavaluex), valoresY = json.dumps(tablavaluey)
        )
    else:
        examenes = ModelUser.consultexam(db, current_user.get_id())
        return render_template('labtest-test.html', exams = examenes, form = form)


        #1.1 - Filtrado

    # Globulos Rojos
@app.route('/labtest/gr')
def labtestfiltergr():
    form = UploadFileForm()

    examenes = ModelUser.consultexam(db, current_user.get_id())

    # Metodo post para filtrado.

        #Obtencion del item que desea filtrar
    valor = '1'
    valmax = ['6000000', '6000000']
    valmin = ['4000000', '4000000']
    val  = ' Globulos Rojos'
    filtervalue = ModelUser.consultvalor(db, valor, current_user.get_id())

        #Obtener valores para la grafica.
            #Listas para la grafica.
    tablavaluex = []
    tablavaluey = []
        
            #Registrar valores en las listas.
    for i in filtervalue:
        tablavaluex.append(i[0].strftime('%d/%m/%Y'))
        tablavaluey.append(i[1])

    return render_template('labtest-filter-test.html', exams = examenes, filters = filtervalue, valore = valor, valoresX = json.dumps(tablavaluex), valoresY = json.dumps(tablavaluey), valmin = json.dumps(valmin), valmax = json.dumps(valmax) , valors = json.dumps(val) , form = form)

    # Globulos Blancos
@app.route('/labtest/gb')
def labtestfiltergb():
    form = UploadFileForm()

    examenes = ModelUser.consultexam(db, current_user.get_id())

    # Metodo post para filtrado.

        #Obtencion del item que desea filtrar
    valor = '2'
    valmax = ['10000', '10000']
    valmin = ['4000', '4000']
    val  = ' Globulos Blancos'
    filtervalue = ModelUser.consultvalor(db, valor, current_user.get_id())

        #Obtener valores para la grafica.
            #Listas para la grafica.
    tablavaluex = []
    tablavaluey = []
        
            #Registrar valores en las listas.
    for i in filtervalue:
        tablavaluex.append(i[0].strftime('%d/%m/%Y'))
        tablavaluey.append(i[1])

    return render_template('labtest-filter-test.html', exams = examenes, filters = filtervalue, valore = valor, valoresX = json.dumps(tablavaluex), valoresY = json.dumps(tablavaluey), valmin = json.dumps(valmin), valmax = json.dumps(valmax) , valors = json.dumps(val) , form = form)

    # Hemoglobina
@app.route('/labtest/hmgb')
def labtestfilterhmgb():
    form = UploadFileForm()

    examenes = ModelUser.consultexam(db, current_user.get_id())

    # Metodo post para filtrado.

        #Obtencion del item que desea filtrar
    valor = '3'
    valmax = ['16', '16']
    valmin = ['12', '12']
    val  = ' Hemoglobina'
    filtervalue = ModelUser.consultvalor(db, valor, current_user.get_id())

        #Obtener valores para la grafica.
            #Listas para la grafica.
    tablavaluex = []
    tablavaluey = []
        
            #Registrar valores en las listas.
    for i in filtervalue:
        tablavaluex.append(i[0].strftime('%d/%m/%Y'))
        tablavaluey.append(i[1])

    return render_template('labtest-filter-test.html', exams = examenes, filters = filtervalue, valore = valor, valoresX = json.dumps(tablavaluex), valoresY = json.dumps(tablavaluey), valmin = json.dumps(valmin), valmax = json.dumps(valmax) , valors = json.dumps(val) , form = form)

    # Hematocritos
@app.route('/labtest/hmtc')
def labtestfilterhmtc():
    form = UploadFileForm()

    examenes = ModelUser.consultexam(db, current_user.get_id())

    # Metodo post para filtrado.

        #Obtencion del item que desea filtrar
    valor = '4'
    valmax = ['46', '46']
    valmin = ['36', '36']
    val  = ' Hematocritos (%)'
    filtervalue = ModelUser.consultvalor(db, valor, current_user.get_id())

        #Obtener valores para la grafica.
            #Listas para la grafica.
    tablavaluex = []
    tablavaluey = []
        
            #Registrar valores en las listas.
    for i in filtervalue:
        tablavaluex.append(i[0].strftime('%d/%m/%Y'))
        tablavaluey.append(i[1])

    return render_template('labtest-filter-test.html', exams = examenes, filters = filtervalue, valore = valor, valoresX = json.dumps(tablavaluex), valoresY = json.dumps(tablavaluey), valmin = json.dumps(valmin), valmax = json.dumps(valmax) , valors = json.dumps(val) , form = form)

    # Plaquetas
@app.route('/labtest/plqt')
def labtestfilterplqt():
    form = UploadFileForm()

    examenes = ModelUser.consultexam(db, current_user.get_id())

    # Metodo post para filtrado.

        #Obtencion del item que desea filtrar
    valor = '5'
    valmax = ['450000', '450000']
    valmin = ['150000', '150000']
    val  = ' Plaquetas'
    filtervalue = ModelUser.consultvalor(db, valor, current_user.get_id())

        #Obtener valores para la grafica.
            #Listas para la grafica.
    tablavaluex = []
    tablavaluey = []
        
            #Registrar valores en las listas.
    for i in filtervalue:
        tablavaluex.append(i[0].strftime('%d/%m/%Y'))
        tablavaluey.append(i[1])

    return render_template('labtest-filter-test.html', exams = examenes, filters = filtervalue, valore = valor, valoresX = json.dumps(tablavaluex), valoresY = json.dumps(tablavaluey), valmin = json.dumps(valmin), valmax = json.dumps(valmax) , valors = json.dumps(val) , form = form)

    # VCM
@app.route('/labtest/vcm')
def labtestfiltervcm():
    form = UploadFileForm()

    examenes = ModelUser.consultexam(db, current_user.get_id())

    # Metodo post para filtrado.

        #Obtencion del item que desea filtrar
    valor = '6'
    valmax = ['100', '100']
    valmin = ['80', '80']
    val  = ' Volumen Corpuscular Medio'
    filtervalue = ModelUser.consultvalor(db, valor, current_user.get_id())

        #Obtener valores para la grafica.
            #Listas para la grafica.
    tablavaluex = []
    tablavaluey = []
        
            #Registrar valores en las listas.
    for i in filtervalue:
        tablavaluex.append(i[0].strftime('%d/%m/%Y'))
        tablavaluey.append(i[1])

    return render_template('labtest-filter-test.html', exams = examenes, filters = filtervalue, valore = valor, valoresX = json.dumps(tablavaluex), valoresY = json.dumps(tablavaluey), valmin = json.dumps(valmin), valmax = json.dumps(valmax) , valors = json.dumps(val) , form = form)

    # HCM
@app.route('/labtest/hcm')
def labtestfilterhcm():
    form = UploadFileForm()

    examenes = ModelUser.consultexam(db, current_user.get_id())

    # Metodo post para filtrado.

        #Obtencion del item que desea filtrar
    valor = '7'
    valmax = ['32', '32']
    valmin = ['27', '27']
    val  = ' Hemoglobina Corpuscular Media'
    filtervalue = ModelUser.consultvalor(db, valor, current_user.get_id())

        #Obtener valores para la grafica.
            #Listas para la grafica.
    tablavaluex = []
    tablavaluey = []
        
            #Registrar valores en las listas.
    for i in filtervalue:
        tablavaluex.append(i[0].strftime('%d/%m/%Y'))
        tablavaluey.append(i[1])

    return render_template('labtest-filter-test.html', exams = examenes, filters = filtervalue, valore = valor, valoresX = json.dumps(tablavaluex), valoresY = json.dumps(tablavaluey), valmin = json.dumps(valmin), valmax = json.dumps(valmax) , valors = json.dumps(val) , form = form)

    # CHCM
@app.route('/labtest/chcm')
def labtestfilterchcm():
    form = UploadFileForm()

    examenes = ModelUser.consultexam(db, current_user.get_id())

    # Metodo post para filtrado.

        #Obtencion del item que desea filtrar
    valor = '8'
    valmax = ['36', '36']
    valmin = ['31', '31']
    val  = ' Hemoglobina Corpuscular Media'
    filtervalue = ModelUser.consultvalor(db, valor, current_user.get_id())

        #Obtener valores para la grafica.
            #Listas para la grafica.
    tablavaluex = []
    tablavaluey = []
        
            #Registrar valores en las listas.
    for i in filtervalue:
        tablavaluex.append(i[0].strftime('%d/%m/%Y'))
        tablavaluey.append(i[1])

    return render_template('labtest-filter-test.html', exams = examenes, filters = filtervalue, valore = valor, valoresX = json.dumps(tablavaluex), valoresY = json.dumps(tablavaluey), valmin = json.dumps(valmin), valmax = json.dumps(valmax) , valors = json.dumps(val) , form = form)







    # 2 -- Solicitar citas
@app.route('/requestdate', methods=['GET', 'POST'])
def requestdate():
    if request.method == 'POST':
        return "<h1>entraste por el metodo post</h1>"
    else:
        citas = ModelUser.consultsolictable(db, current_user.get_id())
        return render_template('requestdate-test.html', solcitas = citas)


    #Insertar
@app.route('/requestdate/add' , methods = ['GET' , 'POST'])
def requestdateadd():
    if request.method == 'POST':
        fecha = request.form['fecha']
        tipo  = request.form['tipo']
        acota = request.form['acotaciones']

        ModelUser.newsolic(db, current_user.get_id(), tipo, fecha, acota, 2)
        
        flash("Bien!    Solicitud agregada correctamente.", "success")
        return (redirect(url_for('requestdate')))
    else:
        return render_template('requestdate-add.html')

    #Editar
@app.route('/requestdate/edit' , methods = ['GET' , 'POST'])
def requestdatedit():
    if request.method == 'POST':
        valEdit = request.form['numero']

        solicitud = ModelUser.consultsolicedit(db, valEdit, current_user.get_id())
        return render_template('requestdate-edit.html', solicitudUpdate = solicitud)
    else:
        citas = ModelUser.consultsolictable(db, current_user.get_id())
        return render_template('requestdate-modify.html', solcitas = citas)

        #Actualizar 
@app.route('/update/<numsolic>', methods=['POST'])
def update(numsolic):
    if request.method == 'POST':
        fecha = request.form['fecha']
        tipo  = request.form['tipo']
        acota = request.form['acotaciones']
        ModelUser.updatesolic(db, tipo, fecha, acota, numsolic, current_user.get_id())
        flash("Bien!    Solicitud de Cita actualizada correctamente.", "success")
        return (redirect(url_for('requestdate')))
    else:
        return (redirect(url_for('requestdate')))



        #Borrar
@app.route('/deletesolic/<string:numsolic>')
def deletesolic(numsolic):
    ModelUser.deletesolic(db, numsolic, current_user.get_id())
    flash("Bien!    Solicitud de cita borrada correctamente.", "success")
    return (redirect(url_for('requestdate')))



        #Bloque de acciones para la vista Solicitar Citas.
        #Agregar
# @app.route('/addsolic', methods=['POST'])
# def addsolic():
#     if request.method == 'POST':
#         ModelUser.newsolic(db, current_user.get_id(), request.form['type'], request.form['fecha'], request.form['acotaciones'], 2)
#         flash("Bien!    Solicitud de Cita añadida correctamente")
#         return (redirect(url_for('requestdate')))
#     else:
#         return (redirect(url_for('requestdate')))

        

        #Editar e Ingresar valores
# @app.route('/editsolic/<string:numsolic>')
# def editsolic(numsolic):
#     solicitud = ModelUser.consultsolicedit(db, numsolic, current_user.get_id())
#     citas = ModelUser.consultsolictable(db, current_user.get_id())
#     return render_template('requestdate-modify.html', solicitudUpdate = solicitud, solcitas = citas)

        


    #3 -- Ver citas agendadas
@app.route('/status')
def status():
    citasagend = ModelUser.citasagendConsult(db, current_user.get_id())

    cardexam = ModelUser.examlastpac(db, current_user.get_id())



    examen1 = []
    examen2 = []
    examen3 = []

    for i in range(0, len(cardexam)):
        if (i == 0):
            for j in cardexam[0]:
                examen1.append(j)

        if (i == 1):
            for k in cardexam[1]:
                examen2.append(k)

        if (i == 2):
            for z in cardexam[2]:
                examen3.append(z)


    # print(cardexam)
    return render_template('status.html', citas = citasagend, examen1 = examen1, examen2 = examen2, examen3 = examen3)





# -- Rutas de utilidades Vista staff y Admin

# 1 -- Vista solicitudes 
@app.route('/gestsolic')
def gestsolic():
    #Comprobacion de Permisos
    userprivilege = ModelUser.checkprivilege(db, current_user.get_id())

    #Renderizado de acuerdo a privilegios.

    if userprivilege[1] == 3:
        #Renderizado de plantilla Paciente.
        return "<h1>Página no encontrada</h1>"

    elif userprivilege[1] == 2:
        #Renderizado de plantilla secretaria o Staff.
        solicitudes = ModelUser.consultsolicstaff(db)
        return render_template('gestsolic.html', solic = solicitudes)
    else:
        #Renderizado de plantilla Admin.
        solicitudes = ModelUser.consultsolicstaff(db)
        return render_template('gestsolic-admin.html', solic = solicitudes)
    

    

    # -- Editar
        #Editar solicitudes (escoger e ingresar valores)
@app.route('/gestsolic/edit', methods = ['GET','POST'])
def gestsolicedit():
    #Comprobacion de Permisos
    userprivilege = ModelUser.checkprivilege(db, current_user.get_id())
    print(userprivilege)


    if request.method == 'POST':
            #Renderizado de acuerdo a privilegios.

        if userprivilege[1] == 3:
            #Renderizado de plantilla Paciente.
            return "<h1>Página no encontrada</h1>"

        elif userprivilege[1] == 2:
            #Renderizado de plantilla secretaria o Staff.
            valor = request.form['numero']
            citaEdit = ModelUser.consultsolicstaffus(db, valor)
            usuarios = ModelUser.consultusersolic(db)
            return render_template('gestsolic-edit.html', users = usuarios, citaparticular = citaEdit)
        else:
            #Renderizado de plantilla Admin.
            valor = request.form['numero']
            citaEdit = ModelUser.consultsolicstaffus(db, valor)
            usuarios = ModelUser.consultusersolic(db)
            return render_template('gestsolic-edit-admin.html', users = usuarios, citaparticular = citaEdit)
    else:

            #Renderizado de acuerdo a privilegios.

        if userprivilege[1] == 3:
            #Renderizado de plantilla Paciente.
            return "<h1>Página no encontrada</h1>"

        elif userprivilege[1] == 2:
            #Renderizado de plantilla secretaria o Staff.
            solicitudes = ModelUser.consultsolicstaff(db)
            return render_template('gestsolic-modify.html', solic = solicitudes)
        else:
            #Renderizado de plantilla Admin.
            solicitudes = ModelUser.consultsolicstaff(db)
            return render_template('gestsolic-modify-admin.html', solic = solicitudes)
        
        

        #Editar solicitudes (update)
@app.route('/edtsolic/<numsolic>', methods = ['POST'])
def updatesolic(numsolic):
    #Comprobacion de Permisos
    userprivilege = ModelUser.checkprivilege(db, current_user.get_id())
    

    if request.method == 'POST':
        ModelUser.updatesolicStaff(db, request.form['tipoE'], request.form['fecha'], request.form['acotaciones'], numsolic, request.form['solicit'])
        flash("Bien!    Solicitud de Cita actualizada correctamente.")
        return (redirect(url_for('gestsolic')))
    else:
        #Renderizado de acuerdo a privilegios.

        if userprivilege[1] == 3:
            #Redireccionado de plantilla Paciente.
            return "<h1>Página no encontrada</h1>"
        else:
            #Redireccionado de plantilla Admin y Staff
            return (redirect(url_for('gestsolic')))

    # -- Agregar
@app.route('/gestsolic/add', methods = ['GET', 'POST'])
def gestsolicadd():
    #Comprobacion de Permisos
    userprivilege = ModelUser.checkprivilege(db, current_user.get_id())

    if request.method == 'POST':
        ModelUser.newsolic(db, request.form['solicit'], request.form['tipoE'], request.form['fecha'], request.form['acotaciones'], 2)
        flash("Bien!    Solicitud de Cita añadida correctamente")
        return (redirect(url_for('gestsolic')))
    else:
            #Renderizado de acuerdo a privilegios.

        if userprivilege[1] == 3:
            #Renderizado de plantilla Paciente.
            return "<h1>Página no encontrada</h1>"

        elif userprivilege[1] == 2:
            #Renderizado de plantilla secretaria o Staff.
            usuarios = ModelUser.consultusersolic(db)
            return render_template('gestsolic-add.html', users = usuarios)
        else:
            #Renderizado de plantilla Admin.
            usuarios = ModelUser.consultusersolic(db)
            return render_template('gestsolic-add-admin.html', users = usuarios)

    # -- Borrar
@app.route('/gestsolic/del', methods = ['GET', 'POST'])
def gestsolicdel():
    #Comprobacion de Permisos
    userprivilege = ModelUser.checkprivilege(db, current_user.get_id())

    if request.method == 'POST':
        ModelUser.delsolic(db, request.form['solicitud'])
        flash("Bien!    Solicitud de Cita borrada correctamente.")
        return (redirect(url_for('gestsolic')))
    else:
        #Renderizado de acuerdo a privilegios.

        if userprivilege[1] == 3:
            #Renderizado de plantilla Paciente.
            return "<h1>Página no encontrada</h1>"

        elif userprivilege[1] == 2:
            #Renderizado de plantilla secretaria o Staff.
            solicitudes = ModelUser.consultsolicstaff(db)
            return render_template('gestsolic-del.html', solic = solicitudes)
        else:
            #Renderizado de plantilla Admin.
            solicitudes = ModelUser.consultsolicstaff(db)
            return render_template('gestsolic-del-admin.html', solic = solicitudes)

    # -- Checkear
@app.route('/checksolic/<numsolic>')
def checksolic(numsolic):
    #Comprobacion de Permisos
    userprivilege = ModelUser.checkprivilege(db, current_user.get_id())

    #Renderizado de acuerdo a privilegios.

    if userprivilege[1] == 3:
        #Renderizado de plantilla Paciente.
        return "<h1>Página no encontrada</h1>"
    else:
        ModelUser.checksolic(db, numsolic)
        flash("Bien!    Solicitud de Cita completada correctamente.")
        return (redirect(url_for('gestsolic')))






# 2 -- Vista examenes


    # Funcion para guardar file y descargar
class UploadFileForm(FlaskForm):
    file = FileField("file")
    submit = SubmitField("Continuar")
    download = SubmitField("Descargar")


# Consulta de examenes [post filtrado , Get sin filtrar]
@app.route('/gestexam', methods = ['POST', 'GET'])
def gestexam():
    #Comprobacion de Permisos
    userprivilege = ModelUser.checkprivilege(db, current_user.get_id())
    form = UploadFileForm()

    if request.method == 'POST':
        #Renderizado de acuerdo a privilegios.

        if userprivilege[1] == 3:
            #Renderizado de plantilla Paciente.
            return "<h1>Página no encontrada</h1>"

        elif userprivilege[1] == 2:
            #Renderizado de plantilla secretaria o Staff.
            usuario = request.form['user']
            fecmin  = request.form['fecMin']
            fecmax  = request.form['fecMax']

            if len(usuario) == 0:
                usuario = None

            if len(fecmin) == 0:
                fecmin  = None

            if len(fecmax) == 0:
                fecmax  = None

            if usuario != None:
                if fecmin is None and fecmax is None:
                    examenes = ModelUser.consultcituser_staff(db, usuario)
                    usuarios = ModelUser.consultusers_staff(db)
                    return render_template('gestexam.html', exams = examenes, users = usuarios, form = form)

                examenes = ModelUser.consultcitfecU_staff(db, usuario, fecmin, fecmax)
                usuarios = ModelUser.consultusers_staff(db)
                return render_template('gestexam.html', exams = examenes, users = usuarios, form = form)
            else:
                if fecmin is None and fecmax is None:
                    return (redirect(url_for('gestexam')))
                else:
                    examenes = ModelUser.consultcitfec_staff(db, fecmin, fecmax)
                    print(examenes)
                    usuarios = ModelUser.consultusers_staff(db)
                    return render_template('gestexam.html', exams = examenes, users = usuarios, form = form)
        else:
            #Renderizado de plantilla Admin.
            usuario = request.form['user']
            fecmin  = request.form['fecMin']
            fecmax  = request.form['fecMax']

            if len(usuario) == 0:
                usuario = None

            if len(fecmin) == 0:
                fecmin  = None

            if len(fecmax) == 0:
                fecmax  = None

            if usuario != None:
                if fecmin is None and fecmax is None:
                    examenes = ModelUser.consultcituser_staff(db, usuario)
                    usuarios = ModelUser.consultusers_staff(db)
                    return render_template('gestexam-admin.html', exams = examenes, users = usuarios, form = form)

                examenes = ModelUser.consultcitfecU_staff(db, usuario, fecmin, fecmax)
                usuarios = ModelUser.consultusers_staff(db)
                return render_template('gestexam-admin.html', exams = examenes, users = usuarios, form = form)
            else:
                if fecmin is None and fecmax is None:
                    return (redirect(url_for('gestexam')))
                else:
                    examenes = ModelUser.consultcitfec_staff(db, fecmin, fecmax)
                    print(examenes)
                    usuarios = ModelUser.consultusers_staff(db)
                    return render_template('gestexam-admin.html', exams = examenes, users = usuarios, form = form)
    else:
            #Renderizado de acuerdo a privilegios.

        if userprivilege[1] == 3:
            #Renderizado de plantilla Paciente.
            return "<h1>Página no encontrada</h1>"

        elif userprivilege[1] == 2:
            #Renderizado de plantilla secretaria o Staff.
            examenes = ModelUser.consultexam_staff(db)
            usuarios = ModelUser.consultusers_staff(db)
            return render_template('gestexam.html', exams = examenes, users = usuarios, form = form)
        else:
            #Renderizado de plantilla Admin.
            examenes = ModelUser.consultexam_staff(db)
            usuarios = ModelUser.consultusers_staff(db)
            return render_template('gestexam-admin.html', exams = examenes, users = usuarios, form = form)


        

    # Ruta para descarga de archivos
@app.route('/download/<numdoc>', methods = ['POST', 'GET'])
def download(numdoc):

    form = UploadFileForm()

    if request.method == 'POST':
        doc_file = ModelUser.consultdocs_staff(db, numdoc)
        return send_file(BytesIO(doc_file[1]), mimetype="text/pdf", download_name='{}.pdf'.format(doc_file[0]), as_attachment=True)
        # return "m uchachoooo no volvimo a ilsuionar"
    else:
        examenes = ModelUser.consultexam_staff(db)
        usuarios = ModelUser.consultusers_staff(db)
        return render_template('gestexam.html', exams = examenes, users = usuarios, form = form)

    # Ruta para modal con carga automatica.
@app.route('/modalexam', methods = ['POST', 'GET'])
def modalexam():
    if request.method == 'POST':
        idcita = request.form['idcita']
        citaV = ModelUser.consultcitas_staff(db, idcita)
    return jsonify({'htmlresponse': render_template('gestexam-response.html', detcita = citaV)})




    # Agregar
@app.route('/gestexam/add', methods = ['POST' , 'GET'])
def gestexamadd():
    #Comprobacion de Permisos
    userprivilege = ModelUser.checkprivilege(db, current_user.get_id())
    form = UploadFileForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            #Excepcion si es paciente
            if userprivilege[1] == 3:
                #Renderizado de plantilla Paciente.
                return "<h1>Página no encontrada</h1>"

            #recibir datos referentes a la data del examen
            cita  = request.form['cita']
            tipo  = request.form['tipoE']
            fecha = request.form['fecha']

            #recibir datos del paciente
            pac = request.form['paciente']
            fullnamepac = pac[ pac.find(",")+1 : ]
            idpac = pac[ : pac.find(",") ]

            #recibir el documento y cambiar el nombre
            file_name = form.file.data
            file_name.filename = 'Examen_{0}_{1}'.format(secure_filename(fullnamepac), fecha)
                
            #recibir datos de los valores el examen
            gr = request.form['gr']
            gb = request.form['gb']
            emoglobina = request.form['emoglobina']
            hematocritos = request.form['hematocritos']
            plaquetas = request.form['plaquetas']
            vcm = request.form['vcm']
            hcm = request.form['hcm']
            chcm = request.form['chcm']

            ModelUser.adddocexam_staff(db, file_name.filename, file_name.read())
            doc_id = ModelUser.consultdocexam_staff(db, file_name.filename)
            ModelUser.addexam_staff(db, idpac, tipo, cita, fecha, gr, gb, emoglobina, hematocritos, plaquetas, vcm, hcm, chcm, doc_id)

            flash("Bien!    Examen agregado correctamente.")
            return (redirect(url_for('gestexam')))
    else:
        #Renderizado de acuerdo a privilegios.

        if userprivilege[1] == 3:
            #Renderizado de plantilla Paciente.
            return "<h1>Página no encontrada</h1>"

        elif userprivilege[1] == 2:
            #Renderizado de plantilla secretaria o Staff.
            usuarios = ModelUser.consultpacexam_staff(db)
            citas = ModelUser.consultcitexam_staff(db)
            return render_template('gestexam-add.html', users = usuarios, cits = citas, form=form)
        else:
            #Renderizado de plantilla Admin.
            usuarios = ModelUser.consultpacexam_staff(db)
            citas = ModelUser.consultcitexam_staff(db)
            return render_template('gestexam-add-admin.html', users = usuarios, cits = citas, form=form)

        



    # Borrar
@app.route('/gestexam/del' , methods = ['GET' , 'POST'])
def gestexamdel():
    #Comprobacion de Permisos
    userprivilege = ModelUser.checkprivilege(db, current_user.get_id())
    form = UploadFileForm()
    
    if request.method == 'POST':

        if userprivilege[1] == 3:
            #Renderizado de plantilla Paciente.
            return "<h1>Página no encontrada</h1>"

        elif userprivilege[1] == 2:
            #Renderizado plantilla Staff
            usuario = request.form['user']
            fecmin  = request.form['fecMin']
            fecmax  = request.form['fecMax']

            if len(usuario) == 0:
                usuario = None

            if len(fecmin) == 0:
                fecmin  = None

            if len(fecmax) == 0:
                fecmax  = None

            if usuario != None:
                if fecmin is None and fecmax is None:
                    examenes = ModelUser.consultcituser_staff(db, usuario)
                    usuarios = ModelUser.consultusers_staff(db)
                    return render_template('gestexam-del.html', exams = examenes, users = usuarios, form = form)

                examenes = ModelUser.consultcitfecU_staff(db, usuario, fecmin, fecmax)
                usuarios = ModelUser.consultusers_staff(db)
                return render_template('gestexam-del.html', exams = examenes, users = usuarios, form = form)
            else:
                if fecmin is None and fecmax is None:
                    return (redirect(url_for('gestexamdel')))
                else:
                    examenes = ModelUser.consultcitfec_staff(db, fecmin, fecmax)
                    usuarios = ModelUser.consultusers_staff(db)
                    return render_template('gestexam-del.html', exams = examenes, users = usuarios, form = form)
        else:
            #Renderizado de plantilla Admin.
            usuario = request.form['user']
            fecmin  = request.form['fecMin']
            fecmax  = request.form['fecMax']

            if len(usuario) == 0:
                usuario = None

            if len(fecmin) == 0:
                fecmin  = None

            if len(fecmax) == 0:
                fecmax  = None

            if usuario != None:
                if fecmin is None and fecmax is None:
                    examenes = ModelUser.consultcituser_staff(db, usuario)
                    usuarios = ModelUser.consultusers_staff(db)
                    return render_template('gestexam-del-admin.html', exams = examenes, users = usuarios, form = form)

                examenes = ModelUser.consultcitfecU_staff(db, usuario, fecmin, fecmax)
                usuarios = ModelUser.consultusers_staff(db)
                return render_template('gestexam-del-admin.html', exams = examenes, users = usuarios, form = form)
            else:
                if fecmin is None and fecmax is None:
                    return (redirect(url_for('gestexamdel')))
                else:
                    examenes = ModelUser.consultcitfec_staff(db, fecmin, fecmax)
                    usuarios = ModelUser.consultusers_staff(db)
                    return render_template('gestexam-del-admin.html', exams = examenes, users = usuarios, form = form)
    else:
        #Renderizado de acuerdo a privilegios.

        if userprivilege[1] == 3:
            #Renderizado de plantilla Paciente.
            return "<h1>Página no encontrada</h1>"

        elif userprivilege[1] == 2:
            #Renderizado de plantilla secretaria o Staff.
            examenes = ModelUser.consultexam_staff(db)
            usuarios = ModelUser.consultusers_staff(db)
            return render_template('gestexam-del.html', exams = examenes, users = usuarios, form = form)
        else:
            #Renderizado de plantilla Admin.
            examenes = ModelUser.consultexam_staff(db)
            usuarios = ModelUser.consultusers_staff(db)
            return render_template('gestexam-del-admin.html', exams = examenes, users = usuarios, form = form)

        

@app.route('/delexam' , methods = ['GET', 'POST'])
def delexam():
    userprivilege = ModelUser.checkprivilege(db, current_user.get_id())
    if request.method == 'POST':
        if userprivilege[1] == 3:
            #Renderizado de plantilla Paciente.
            return "<h1>Página no encontrada</h1>"

        numexam = request.form['numDel']
        ModelUser.delexam_staff(db, numexam)
        flash("Bien!    Examen borrado correctamente.")
        return (redirect(url_for('gestexam')))
    else:
        if userprivilege[1] == 3:
            #Renderizado de plantilla Paciente.
            return "<h1>Página no encontrada</h1>"

        return (redirect(url_for('gestexam')))


    
    #Editar
@app.route('/gestexam/edit', methods = ['GET' , 'POST'])
def gestexamedit():
    #Comprobacion de Permisos
    userprivilege = ModelUser.checkprivilege(db, current_user.get_id())
    form = UploadFileForm()

    if request.method == 'POST':
        #Renderizado de acuerdo a privilegios.

        if userprivilege[1] == 3:
            #Renderizado de plantilla Paciente.
            return "<h1>Página no encontrada</h1>"

        elif userprivilege[1] == 2:
            #Renderizado de plantilla secretaria o Staff.
            usuario = request.form['user']
            fecmin  = request.form['fecMin']
            fecmax  = request.form['fecMax']

            if len(usuario) == 0:
                usuario = None

            if len(fecmin) == 0:
                fecmin  = None

            if len(fecmax) == 0:
                fecmax  = None

            if usuario != None:
                if fecmin is None and fecmax is None:
                    examenes = ModelUser.consultcituser_staff(db, usuario)
                    usuarios = ModelUser.consultusers_staff(db)
                    return render_template('gestexam-modify.html', exams = examenes, users = usuarios, form = form)

                examenes = ModelUser.consultcitfecU_staff(db, usuario, fecmin, fecmax)
                usuarios = ModelUser.consultusers_staff(db)
                return render_template('gestexam-modify.html', exams = examenes, users = usuarios, form = form)
            else:
                if fecmin is None and fecmax is None:
                    return (redirect(url_for('gestexamedit')))
                else:
                    examenes = ModelUser.consultcitfec_staff(db, fecmin, fecmax)
                    usuarios = ModelUser.consultusers_staff(db)
                    return render_template('gestexam-modify.html', exams = examenes, users = usuarios, form = form)
        else:
            #Renderizado de plantilla Admin.
            usuario = request.form['user']
            fecmin  = request.form['fecMin']
            fecmax  = request.form['fecMax']

            if len(usuario) == 0:
                usuario = None

            if len(fecmin) == 0:
                fecmin  = None

            if len(fecmax) == 0:
                fecmax  = None

            if usuario != None:
                if fecmin is None and fecmax is None:
                    examenes = ModelUser.consultcituser_staff(db, usuario)
                    usuarios = ModelUser.consultusers_staff(db)
                    return render_template('gestexam-modify-admin.html', exams = examenes, users = usuarios, form = form)

                examenes = ModelUser.consultcitfecU_staff(db, usuario, fecmin, fecmax)
                usuarios = ModelUser.consultusers_staff(db)
                return render_template('gestexam-modify-admin.html', exams = examenes, users = usuarios, form = form)
            else:
                if fecmin is None and fecmax is None:
                    return (redirect(url_for('gestexamedit')))
                else:
                    examenes = ModelUser.consultcitfec_staff(db, fecmin, fecmax)
                    usuarios = ModelUser.consultusers_staff(db)
                    return render_template('gestexam-modify-admin.html', exams = examenes, users = usuarios, form = form)
    else:
        #Renderizado de acuerdo a privilegios.

        if userprivilege[1] == 3:
            #Renderizado de plantilla Paciente.
            return "<h1>Página no encontrada</h1>"

        elif userprivilege[1] == 2:
            #Renderizado de plantilla secretaria o Staff.
            examenes = ModelUser.consultexam_staff(db)
            usuarios = ModelUser.consultusers_staff(db)
            return render_template('gestexam-modify.html', exams = examenes, users = usuarios, form = form)
        else:
            #Renderizado de plantilla Admin.
            examenes = ModelUser.consultexam_staff(db)
            usuarios = ModelUser.consultusers_staff(db)
            return render_template('gestexam-modify-admin.html', exams = examenes, users = usuarios, form = form)

        

@app.route('/gestexam/edit/t', methods = ['POST' , 'GET'])
def updtexam():
    #Comprobacion de Permisos
    userprivilege = ModelUser.checkprivilege(db, current_user.get_id())
    form = UploadFileForm()

    if request.method == 'POST':
        #Renderizado de acuerdo a privilegios.

        if userprivilege[1] == 3:
            #Renderizado de plantilla Paciente.
            return "<h1>Página no encontrada</h1>"

        elif userprivilege[1] == 2:
            #Renderizado de plantilla secretaria o Staff.
            numexam = request.form['numEdit']
            citEdit = ModelUser.consultexamedit_staff(db, numexam)
            usuarios = ModelUser.consultpacexam_staff(db)
            citas = ModelUser.consultcitcomp_staff(db)
            return render_template('gestexam-edit.html', cits = citas, users = usuarios, citEdit = citEdit, form = form)
        else:
            #Renderizado de plantilla Admin.
            numexam = request.form['numEdit']
            citEdit = ModelUser.consultexamedit_staff(db, numexam)
            usuarios = ModelUser.consultpacexam_staff(db)
            citas = ModelUser.consultcitcomp_staff(db)
            return render_template('gestexam-edit-admin.html', cits = citas, users = usuarios, citEdit = citEdit, form = form)
    else:
        if userprivilege[1] == 3:
            #Renderizado de plantilla Paciente.
            return "<h1>Página no encontrada</h1>"

        return redirect(url_for('gestexam'))


@app.route('/edtexam/<numexam>', methods = ['POST' , 'GET'])
def edtexam(numexam):
    #Comprobacion de Permisos
    userprivilege = ModelUser.checkprivilege(db, current_user.get_id())
    form = UploadFileForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            if userprivilege[1] == 3:
                #Renderizado de plantilla Paciente.
                return "<h1>Página no encontrada</h1>"


            #recibir datos referentes a la data del examen
            cita  = request.form['cita']
            tipo  = request.form['tipoE']
            fecha = request.form['fecha']

            #recibir datos del paciente
            pac = request.form['paciente']
            fullnamepac = pac[ pac.find(",")+1 : ]
            idpac = pac[ : pac.find(",") ]

            #recibir el documento y cambiar el nombre
            file_name = form.file.data
            file_name.filename = 'Examen_{0}_{1}'.format(secure_filename(fullnamepac), fecha)
            
            #recibir datos de los valores el examen
            gr = request.form['gr']
            gb = request.form['gb']
            emoglobina = request.form['emoglobina']
            hematocritos = request.form['hematocritos']
            plaquetas = request.form['plaquetas']
            vcm = request.form['vcm']
            hcm = request.form['hcm']
            chcm = request.form['chcm']


            if len(file_name.read()) != 0:
                file_name.seek(0)
                
                #Insertando el nuevo
                ModelUser.adddocexam_staff(db, file_name.filename, file_name.read())
                doc_id = ModelUser.consultdocexam_staff(db, file_name.filename)
                print(doc_id[0])

                #Consultando doc anterior antes de eliminarlo
                doctodel_id = ModelUser.consultnumdoc_staff(db, numexam)

                #Actualizandolo
                ModelUser.updtexam_valores_staff(db, numexam, idpac, tipo, cita, fecha, gr, gb, emoglobina, hematocritos, plaquetas, vcm, hcm, chcm, doc_id[0])

                #Borrando el viejo
                print(doctodel_id)
                ModelUser.delold_doc_staff(db, doctodel_id[0])
                
            else:
                file_name.seek(0)
                
                doc_id = None
                ModelUser.updtexam_valores_staff(db, numexam, idpac, tipo, cita, fecha, gr, gb, emoglobina, hematocritos, plaquetas, vcm, hcm, chcm, doc_id)
            
            flash("Bien!    Examen actualizado correctamente.")
            return (redirect(url_for('gestexam')))
    else:
        if userprivilege[1] == 3:
            #Renderizado de plantilla Paciente.
            return "<h1>Página no encontrada</h1>"

        return redirect(url_for('gestexam'))



# 3 -- Vista Citas

    # Consulta
@app.route('/gestcit', methods = ['POST' , 'GET'])
def gestcit():
    #Comprobacion de Permisos
    userprivilege = ModelUser.checkprivilege(db, current_user.get_id())

    if request.method == 'POST':
        #Renderizado de acuerdo a privilegios.

        if userprivilege[1] == 3:
            #Renderizado de plantilla Paciente.
            return "<h1>Página no encontrada</h1>"

        elif userprivilege[1] == 2:
            #Renderizado de plantilla secretaria o Staff.
            estado = request.form['estado']
            fecmin = request.form['fecMin']
            fecmax = request.form['fecMax']

            if len(estado) == 0:
                estado = None

            if len(fecmin) == 0:
                fecmin  = None

            if len(fecmax) == 0:
                fecmax  = None

            if estado != None:
                if fecmin is None and fecmax is None:
                    citas = ModelUser.concitS_staff(db, estado)
                    return render_template('gestcit.html', cits = citas)

                citas = ModelUser.concitfecS_staff(db, estado, fecmin, fecmax)
                return render_template('gestcit.html', cits = citas)
            else:
                if fecmin is None and fecmax is None:
                    return (redirect(url_for('gestcit')))
                else:
                    citas = ModelUser.concitfec_staff(db, fecmin, fecmax)
                    return render_template('gestcit.html', cits = citas)
        else:
            #Renderizado de plantilla Admin.
            estado = request.form['estado']
            fecmin = request.form['fecMin']
            fecmax = request.form['fecMax']

            if len(estado) == 0:
                estado = None

            if len(fecmin) == 0:
                fecmin  = None

            if len(fecmax) == 0:
                fecmax  = None

            if estado != None:
                if fecmin is None and fecmax is None:
                    citas = ModelUser.concitS_staff(db, estado)
                    return render_template('gestcit-admin.html', cits = citas)

                citas = ModelUser.concitfecS_staff(db, estado, fecmin, fecmax)
                return render_template('gestcit-admin.html', cits = citas)
            else:
                if fecmin is None and fecmax is None:
                    return (redirect(url_for('gestcit')))
                else:
                    citas = ModelUser.concitfec_staff(db, fecmin, fecmax)
                    return render_template('gestcit-admin.html', cits = citas)
    else:
        #Renderizado de acuerdo a privilegios.

        if userprivilege[1] == 3:
            #Renderizado de plantilla Paciente.
            return "<h1>Página no encontrada</h1>"

        elif userprivilege[1] == 2:
            #Renderizado de plantilla secretaria o Staff.
            citas = ModelUser.consultcit_staff(db)
            return render_template('gestcit.html', cits = citas)
        else:
            #Renderizado de plantilla Admin.
            citas = ModelUser.consultcit_staff(db)
            return render_template('gestcit-admin.html', cits = citas)

        

        #Ruta modal
@app.route('/modalsolic', methods = ['POST', 'GET'])
def modalsolic():
    if request.method == 'POST':
        idsolic = request.form['idsolic']
        solicV = ModelUser.consultsolicmodal_staff(db, idsolic)
    return jsonify({'htmlresponse': render_template('gestcit-response.html', detsolic = solicV)})




    # Agregar
@app.route('/gestcit/add', methods = ['POST', 'GET'])
def gestcitadd():
    #Comprobacion de Permisos
    userprivilege = ModelUser.checkprivilege(db, current_user.get_id())

    if request.method == 'POST':
        if userprivilege[1] == 3:
            #Renderizado de plantilla Paciente.
            return "<h1>Página no encontrada</h1>"

        #---
        #Paciente
        paciente = request.form['paciente']
        idpac = paciente[ : paciente.find(",") ]

        #Datos cita
        solicitud = request.form['solicitud']
        tipo = request.form['tipoE']
        fecha = request.form['fecha']

        ModelUser.addcit_staff(db, idpac, solicitud, tipo, fecha)
        flash("Bien!    Cita agregada correctamente.")
        return redirect(url_for('gestcit'))
    else:
        #Renderizado de acuerdo a privilegios.

        if userprivilege[1] == 3:
            #Renderizado de plantilla Paciente.
            return "<h1>Página no encontrada</h1>"

        elif userprivilege[1] == 2:
            #Renderizado de plantilla secretaria o Staff.
            solicitudes = ModelUser.consultrensol_cit_staff(db)
            pacientes   = ModelUser.consultpacsol_cit_staff(db)
            fechasdisabled = ModelUser.fecdisabled_cit_staff(db)

            #listas separadas Hora y Fecha
            fechasDisbFirst = []
            fechasDisbSecond = []

            #comprobacion en las horas
            for i in fechasdisabled:
                fechasDisbFirst.append(str(datetime.strftime(i[0], '%m/%d/%Y %H:%M:%S'))[:10])

                if int(str(datetime.strftime(i[0], '%m/%d/%Y %H:%M:%S'))[11:13]) < 10:
                    fechasDisbSecond.append(str(datetime.strftime(i[0], '%m/%d/%Y %H:%M:%S'))[12:13])
                else:
                    fechasDisbSecond.append(str(datetime.strftime(i[0], '%m/%d/%Y %H:%M:%S'))[11:13])

            #Lista para fechas ocupadas
            fechasDisbld = []

            #Registrar las fechas y horas en la lista
            for i in range(len(fechasDisbFirst)):
                fechasDisbld.append(fechasDisbFirst[i] + ':' + fechasDisbSecond[i])


            return render_template('gestcit-add.html', solts = solicitudes, pacs = pacientes, fechsDis = json.dumps(fechasDisbld))
        else:
            #Renderizado de plantilla Admin.
            solicitudes = ModelUser.consultrensol_cit_staff(db)
            pacientes   = ModelUser.consultpacsol_cit_staff(db)
            fechasdisabled = ModelUser.fecdisabled_cit_staff(db)

            #listas separadas Hora y Fecha
            fechasDisbFirst = []
            fechasDisbSecond = []

            #comprobacion en las horas
            for i in fechasdisabled:
                fechasDisbFirst.append(str(datetime.strftime(i[0], '%m/%d/%Y %H:%M:%S'))[:10])

                if int(str(datetime.strftime(i[0], '%m/%d/%Y %H:%M:%S'))[11:13]) < 10:
                    fechasDisbSecond.append(str(datetime.strftime(i[0], '%m/%d/%Y %H:%M:%S'))[12:13])
                else:
                    fechasDisbSecond.append(str(datetime.strftime(i[0], '%m/%d/%Y %H:%M:%S'))[11:13])

            #Lista para fechas ocupadas
            fechasDisbld = []

            #Registrar las fechas y horas en la lista
            for i in range(len(fechasDisbFirst)):
                fechasDisbld.append(fechasDisbFirst[i] + ':' + fechasDisbSecond[i])


            return render_template('gestcit-add-admin.html', solts = solicitudes, pacs = pacientes, fechsDis = json.dumps(fechasDisbld))

        
    

    #Editar
@app.route('/gestcit/edit', methods = ['POST', 'GET'])
def gestcitedit():
    #Comprobacion de Permisos
    userprivilege = ModelUser.checkprivilege(db, current_user.get_id())

    if request.method == 'POST':
        return "hola"
    else:
        #Renderizado de acuerdo a privilegios.

        if userprivilege[1] == 3:
            #Renderizado de plantilla Paciente.
            return "<h1>Página no encontrada</h1>"

        elif userprivilege[1] == 2:
            #Renderizado de plantilla secretaria o Staff.
            citas = ModelUser.consultcit_staff(db)
            return render_template('gestcit-modify.html', cits = citas)
        else:
            #Renderizado de plantilla Admin.
            citas = ModelUser.consultcit_staff(db)
            return render_template('gestcit-modify-admin.html', cits = citas)
        

        #Ingresar y recibir valores.
@app.route('/gestcit/edit/t', methods = ['POST', 'GET'])
def updtcit():
    #Comprobacion de Permisos
    userprivilege = ModelUser.checkprivilege(db, current_user.get_id())

    if request.method == 'POST':
        #Renderizado de acuerdo a privilegios.

        if userprivilege[1] == 3:
            #Renderizado de plantilla Paciente.
            return "<h1>Página no encontrada</h1>"

        elif userprivilege[1] == 2:
            #Renderizado de plantilla secretaria o Staff.
            #---
            #Requesteando el numero de cita a editar
            citEdit = request.form['numEdit']

            #Consultas para el template
            citaEdit = ModelUser.consultcitedit_cit_staff(db, citEdit)
            solEditData = ModelUser.consulteditsol_cit_staff(db, citaEdit[3])
            solicitudes = ModelUser.consultrensol_cit_staff(db)
            pacientes   = ModelUser.consultpacsol_cit_staff(db)

            #Consultar fechas a deshabilitar
            fechasdisabled = ModelUser.fecdisablededit_cit_staff(db, citaEdit[0])

            #listas separadas Hora y Fecha
            fechasDisbFirst = []
            fechasDisbSecond = []

            #comprobacion en las horas
            for i in fechasdisabled:
                fechasDisbFirst.append(str(datetime.strftime(i[0], '%m/%d/%Y %H:%M:%S'))[:10])

                if int(str(datetime.strftime(i[0], '%m/%d/%Y %H:%M:%S'))[11:13]) < 10:
                    fechasDisbSecond.append(str(datetime.strftime(i[0], '%m/%d/%Y %H:%M:%S'))[12:13])
                else:
                    fechasDisbSecond.append(str(datetime.strftime(i[0], '%m/%d/%Y %H:%M:%S'))[11:13])

            #Lista para fechas ocupadas
            fechasDisbld = []

            #Registrar las fechas y horas en la lista
            for i in range(len(fechasDisbFirst)):
                fechasDisbld.append(fechasDisbFirst[i] + ':' + fechasDisbSecond[i])

            return render_template('gestcit-edit.html', solts = solicitudes, pacs = pacientes, fechsDis = json.dumps(fechasDisbld), citaEdit = citaEdit, solEdit = solEditData)
        else:
            #Renderizado de plantilla Admin.
            #---
            #Requesteando el numero de cita a editar
            citEdit = request.form['numEdit']

            #Consultas para el template
            citaEdit = ModelUser.consultcitedit_cit_staff(db, citEdit)
            solEditData = ModelUser.consulteditsol_cit_staff(db, citaEdit[3])
            solicitudes = ModelUser.consultrensol_cit_staff(db)
            pacientes   = ModelUser.consultpacsol_cit_staff(db)

            #Consultar fechas a deshabilitar
            fechasdisabled = ModelUser.fecdisablededit_cit_staff(db, citaEdit[0])

            #listas separadas Hora y Fecha
            fechasDisbFirst = []
            fechasDisbSecond = []

            #comprobacion en las horas
            for i in fechasdisabled:
                fechasDisbFirst.append(str(datetime.strftime(i[0], '%m/%d/%Y %H:%M:%S'))[:10])

                if int(str(datetime.strftime(i[0], '%m/%d/%Y %H:%M:%S'))[11:13]) < 10:
                    fechasDisbSecond.append(str(datetime.strftime(i[0], '%m/%d/%Y %H:%M:%S'))[12:13])
                else:
                    fechasDisbSecond.append(str(datetime.strftime(i[0], '%m/%d/%Y %H:%M:%S'))[11:13])

            #Lista para fechas ocupadas
            fechasDisbld = []

            #Registrar las fechas y horas en la lista
            for i in range(len(fechasDisbFirst)):
                fechasDisbld.append(fechasDisbFirst[i] + ':' + fechasDisbSecond[i])

            return render_template('gestcit-edit-admin.html', solts = solicitudes, pacs = pacientes, fechsDis = json.dumps(fechasDisbld), citaEdit = citaEdit, solEdit = solEditData)
    else:
        if userprivilege[1] == 3:
            #Renderizado de plantilla Paciente.
            return "<h1>Página no encontrada</h1>"

        return redirect(url_for('gestcit'))


@app.route('/edtcit/<numcita>', methods = ['POST' , 'GET'])
def edtcit(numcita):
    #Comprobacion de Permisos
    userprivilege = ModelUser.checkprivilege(db, current_user.get_id())

    if request.method == 'POST':
        if userprivilege[1] == 3:
            #Renderizado de plantilla Paciente.
            return "<h1>Página no encontrada</h1>"

        print('cita numero: {}'.format(numcita))

        #Paciente
        paciente = request.form['paciente']
        idpac = paciente[ : paciente.find(",") ]

        #Datos cita
        solicitud = request.form['solicitud']
        tipo = request.form['tipoE']
        fecha = request.form['fecha']
        status = request.form['status']

        ModelUser.updtcit_cit_staff(db, numcita, fecha, idpac, solicitud, status, tipo)


        flash("Bien!    Cita actualizado correctamente.")
        return redirect(url_for('gestcit'))
    else:
        if userprivilege[1] == 3:
            #Renderizado de plantilla Paciente.
            return "<h1>Página no encontrada</h1>"

        return redirect(url_for('gestcit'))



    #Borrar
@app.route('/gestcit/del', methods = ['POST', 'GET'])
def gestcitdel():
    #Comprobacion de Permisos
    userprivilege = ModelUser.checkprivilege(db, current_user.get_id())

    if request.method == 'POST':
        if userprivilege[1] == 3:
            #Renderizado de plantilla Paciente.
            return "<h1>Página no encontrada</h1>"

        numCita = request.form['numDel']

        ModelUser.delcit_cit_staff(db, numCita)
        flash("Bien!    Cita borrada correctamente.")
        return redirect(url_for('gestcit'))
    else:
        #Renderizado de acuerdo a privilegios.

        if userprivilege[1] == 3:
            #Renderizado de plantilla Paciente.
            return "<h1>Página no encontrada</h1>"

        elif userprivilege[1] == 2:
            #Renderizado de plantilla secretaria o Staff.
            citas = ModelUser.consultcit_staff(db)
            return render_template('gestcit-del.html', cits = citas)
        else:
            #Renderizado de plantilla Admin.
            citas = ModelUser.consultcit_staff(db)
            return render_template('gestcit-del-admin.html', cits = citas)

        

    #Checkear
@app.route('/checkcit/<numcita>')
def checkcit(numcita):
    ModelUser.checksolic(db, numcita)
    flash("Bien!    Cita completada correctamente.")
    return (redirect(url_for('gestcit')))




#4 -- Vista Usuarios

    #Consulta y Edit
@app.route('/gestuser' , methods = ['POST' , 'GET'])
def gestuser():
    #Comprobacion de Permisos
    userprivilege = ModelUser.checkprivilege(db, current_user.get_id())

    if request.method == 'POST':
        #Renderizando por permisos

        if userprivilege[1] == 3:
            #Renderizado de plantilla Paciente.
            return "<h1>Página no encontrada</h1>"
        elif userprivilege[1] == 2:
            #Renderizado de plantilla secretaria o Staff.
            return "<h1>Página no encontrada</h1>"

        #Privilegio
        privilegi = request.form['privilegio']
        privilegio = privilegi[:privilegi.find(",")]

        #Id
        iduser = privilegi[privilegi.find(",")+1:]

        #Datos
        username = request.form['username']
        nombre = request.form['fullname']
        correo = request.form['email']
        direccion = request.form['address']
        celular = request.form['cellphone']

            #Comprobaciones

        # - Email

            # Formato correcto
        if correo[correo.find("@"):] not in ['@gmail.com', '@hotmail.com', '@outlook.com', '@hotmail.es']:
            flash("Vaya.... El email no esta permitido.", 'danger')
            return redirect(url_for('gestuser'))

            # Existencia
        checkvalue2 = ModelUser.checkemail_admin(db, correo, iduser)
        print(checkvalue2)
        if checkvalue2 == '0':
            flash('Vaya...  Email ya registrado, usa otro.', 'danger')
            return redirect(url_for('gestuser'))
            
        # - Username
        if (len(username) >= 4) and (len(username) <= 12):
            #Caracteres especiales
            tvalue = ModelUser.special_char(username)

            if tvalue is True:
                flash("Vaya...  Usuario no puede contener caracteres especiales.", "danger")
                return redirect(url_for('gestuser'))

            #Si ya existe
            checkvalue = ModelUser.checkuser_admin(db, username, iduser) 

                #Si checkuser retorna uno no existe, si retorna cero si existe.
            if checkvalue == '1':
                ModelUser.updtprivilege_admin(db, iduser, privilegio)
                ModelUser.updtdata_admin(db, iduser, username, nombre, correo, direccion, celular)

                flash("Bien!    Actualización de usuario realizada.", "success")
                return redirect(url_for('gestuser'))
            else:
                flash('Vaya...  Usuario ya existente, intenta con otro.', 'danger')
                return redirect(url_for('gestuser'))
        else:
            flash("Vaya.... Usuario no permitido. Debe tener entre 4 y 12 caracteres.", 'danger')
            return (redirect(url_for('gestuser')))
    else:
        if userprivilege[1] == 3:
            #Renderizado de plantilla Paciente.
            return "<h1>Página no encontrada</h1>"
        elif userprivilege[1] == 2:
            #Renderizado de plantilla secretaria o Staff.
            return "<h1>Página no encontrada</h1>"

        user = ModelUser.consultusers_table(db)
        return render_template('gestuser.html', users = user)

    # Modal
@app.route('/modalusers', methods = ['POST', 'GET'])
def modalusers():
    if request.method == 'POST':
        iduser = request.form['iduser']
        print(iduser)
        userdata = ModelUser.consultdatauser(db , iduser)
        return jsonify({'htmlresponse': render_template('gestuser-response.html', user = userdata)})


    # -- Utilidades

    # Borrar
@app.route('/gestuser/del', methods = ['POST' , 'GET'])
def gestuserdel():
    if request.method == 'POST':
        ModelUser.deleteuserdata_admin(db, request.form['numDel'])

        flash("Bien!    Usuario borrado correctamente.", "success")
        return redirect(url_for('gestuser'))
    else:
        user = ModelUser.consultusers_table(db)
        return render_template('gestuser-del.html', users = user)



    #Agregar
@app.route('/gestuser/add', methods = ['POST', 'GET'])
def gestuseradd():
    if request.method == 'POST':

        #Obteniendo datos
        username = request.form['username']
        genero   = request.form['genero']
        password = generate_password_hash(request.form['password'])
        fullname = request.form['nombre'] + ' ' + request.form['apellido']
        correo   = request.form['correo']
        address  = request.form['ciudad'] + ', ' + request.form['sector'] + ', ' + request.form['calle']
        celular  = request.form['prefijo'] + request.form['sufijo']
        privilegio = request.form['privilegio']

        #corta

        #Comprobaciones

        # - Email

            # Formato correcto
        if correo[correo.find("@"):] not in ['@gmail.com', '@hotmail.com', '@outlook.com', '@hotmail.es']:
            flash("Vaya.... El email no esta permitido.", 'danger')
            return redirect(url_for('gestuseradd'))

            # Existencia
        checkvalue2 = ModelUser.checkemail_add_admin(db, correo)
        if checkvalue2 == '0':
            flash('Vaya...  Email ya registrado, usa otro.', 'danger')
            return redirect(url_for('gestuseradd'))
            
        # - Username
        if (len(username) >= 4) and (len(username) <= 12):
            #Caracteres especiales
            tvalue = ModelUser.special_char(username)

            if tvalue is True:
                flash("Vaya...  Usuario no puede contener caracteres especiales.", "danger")
                return redirect(url_for('gestuseradd'))

            #Si ya existe
            checkvalue = ModelUser.checkuser_add_admin(db, username) 

                #Si checkuser retorna uno no existe, si retorna cero si existe.
            if checkvalue == '1':

                    #Imagen
                profile_pic = cv2.imread('static/img/98681.jfif')

                #Ingresando datos
                ModelUser.gestuseradd_data_admin(db, username, password, fullname, correo, address, genero, celular, profile_pic)

                #Consultando usuario ingresado
                iduser = ModelUser.checkuser_addtwo_admin(db, username)

                print(iduser[0])

                #Ingresando privilegio
                ModelUser.gestuseradd_privilege_admin(db, iduser[0], privilegio)

                flash("Bien!    Usuario ingresado correctamente con el ID #{}".format(iduser), "success")
                return redirect(url_for('gestuser'))
            else:
                flash('Vaya...  Usuario ya existente, intenta con otro.', 'danger')
                return redirect(url_for('gestuseradd'))
        else:
            flash("Vaya.... Usuario no permitido. Debe tener entre 4 y 12 caracteres.", 'danger')
            return (redirect(url_for('gestuseradd')))

        #corta
    else:
        return render_template('gestuser-add.html')





#Vistas para Errores
    #url protegida
def status_401(error):
    return redirect(url_for('login'))

    #url inexistente
def status_404(error):
    return "<h1>Pagina no encontrada.</h1>" , 404




# -- Ruta para propositos de testeos.
@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/protected')
@login_required
def protected():
    return "<h1>Vista protegida, solo para usuarios autentificados</h1>"


if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(debug=True)
