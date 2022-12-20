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
    return render_template('home.html')

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
                flash("Vaya.... Password invalido.             #ff0000")
                return redirect(url_for('login'))
        else:
            flash("Vaya.... Usuario no encontrado.         #ff0000")
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

    # Ruta Principal de Logeo.
@app.route('/login')
def login():
    return render_template('login.html')

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
        address = request.form['address']
        genre = request.form['genre']
        cellphone = request.form['suffix'] + '-' + request.form['cellphone']

        # Comprobacion de los valores. (Correctos.)

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
                flash("Vaya...  Usuario no permitido. No puede contener caracteres especiales.")
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
                    flash('Bien!    Se ha registrado correctamente.#2DE94F')
                    return redirect(url_for('login'))
                else:
                    flash('Vaya...  Email ya registrado, usa otro.')
                    return redirect(url_for('register'))
            else:
                flash('Vaya...  Usuario ya registrado, intenta con otro.')
                return redirect(url_for('register'))
        else:
            flash("Vaya.... Usuario no permitido. Debe tener entre 4 y 12 caracteres.")
            return (redirect(url_for('register')))
    else:
        return (redirect(url_for('register')))

    # Ruta principal De Registro.
@app.route('/register')
def register():
    return render_template('register.html')





# -- Rutas a partir del login (PROTEGER RUTAS UNA VEZ FINALIZADO SU DISEÑO)

    # -- Usuario
        # --Home 
@app.route('/home')
def homeuser():
    #Comprobacion de Permisos
    userprivilege = ModelUser.checkprivilege(db, current_user.get_id())

    #Renderizado de acuerdo a privilegios.
    if userprivilege[1] == 3:
        #Renderizado de plantilla Paciente.
        return render_template("home-user.html")
    elif userprivilege[1] == 2:
        #Renderizado de plantilla secretaria o Staff.
        return render_template("home-staff.html")
    else:
        #Renderizado de plantilla Admin.
        return 'Admin papa'

    #1 -- Gestionar Examenes
@app.route('/labtest', methods=['GET', 'POST'])
def labtest():
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
        return render_template('labtest.html', exams = examenes)
    
    # 2 -- Solicitar citas
@app.route('/requestdate', methods=['GET', 'POST'])
def requestdate():
    if request.method == 'POST':
        return "<h1>entraste por el metodo post</h1>"
    else:
        citas = ModelUser.consultsolictable(db, current_user.get_id())
        return render_template('requestdate.html', solcitas = citas)

        #Bloque de acciones para la vista Solicitar CItas.
        #Agregar
@app.route('/addsolic', methods=['POST'])
def addsolic():
    if request.method == 'POST':
        ModelUser.newsolic(db, current_user.get_id(), request.form['type'], request.form['fecha'], request.form['acotaciones'], 2)
        flash("Bien!    Solicitud de Cita añadida correctamente")
        return (redirect(url_for('requestdate')))
    else:
        return (redirect(url_for('requestdate')))

        #Borrar
@app.route('/deletesolic/<string:numsolic>')
def deletesolic(numsolic):
    ModelUser.deletesolic(db, numsolic, current_user.get_id())
    flash("Bien!    Solicitud de Cita borrada correctamente.")
    return (redirect(url_for('requestdate')))

        #Editar e Ingresar valores
@app.route('/editsolic/<string:numsolic>')
def editsolic(numsolic):
    solicitud = ModelUser.consultsolicedit(db, numsolic, current_user.get_id())
    citas = ModelUser.consultsolictable(db, current_user.get_id())
    return render_template('requestdate-modify.html', solicitudUpdate = solicitud, solcitas = citas)

        #Actualizar 
@app.route('/update/<numsolic>', methods=['POST'])
def update(numsolic):
    if request.method == 'POST':
        ModelUser.updatesolic(db, request.form['type'], request.form['fecha'], request.form['acotaciones'], numsolic, current_user.get_id())
        flash("Bien!    Solicitud de Cita actualizada correctamente.")
        return (redirect(url_for('requestdate')))
    else:
        return (redirect(url_for('requestdate')))

    #3 -- Ver citas agendadas
@app.route('/status')
def status():
    citasagend = ModelUser.citasagendConsult(db, current_user.get_id())
    return render_template('status.html', citas = citasagend)





# -- Rutas de utilidades Vista staff.

# 1 -- Vista solicitudes 
@app.route('/gestsolic')
def gestsolic():
    solicitudes = ModelUser.consultsolicstaff(db)
    return render_template('gestsolic.html', solic = solicitudes)

    # -- Editar
        #Editar solicitudes (escoger e ingresar valores)
@app.route('/gestsolic/edit', methods = ['GET','POST'])
def gestsolicedit():
    if request.method == 'POST':
        valor = request.form['numero']
        citaEdit = ModelUser.consultsolicstaffus(db, valor)
        usuarios = ModelUser.consultusersolic(db)
        return render_template('gestsolic-edit.html', users = usuarios, citaparticular = citaEdit)
    else:
        solicitudes = ModelUser.consultsolicstaff(db)
        return render_template('gestsolic-modify.html', solic = solicitudes)

        #Editar solicitudes (update)
@app.route('/updatesolic/<numsolic>', methods = ['POST'])
def updatesolic(numsolic):
    if request.method == 'POST':
        ModelUser.updatesolicStaff(db, request.form['tipoE'], request.form['fecha'], request.form['acotaciones'], numsolic, request.form['solicit'])
        flash("Bien!    Solicitud de Cita actualizada correctamente.")
        return (redirect(url_for('gestsolic')))
    else:
        return (redirect(url_for('gestsolic')))


    # -- Agregar
@app.route('/gestsolic/add', methods = ['GET', 'POST'])
def gestsolicadd():
    if request.method == 'POST':
        ModelUser.newsolic(db, request.form['solicit'], request.form['tipoE'], request.form['fecha'], request.form['acotaciones'], 2)
        flash("Bien!    Solicitud de Cita añadida correctamente")
        return (redirect(url_for('gestsolic')))
    else:
        usuarios = ModelUser.consultusersolic(db)
        return render_template('gestsolic-add.html', users = usuarios)

    # -- Borrar
@app.route('/gestsolic/del', methods = ['GET', 'POST'])
def gestsolicdel():
    if request.method == 'POST':
        ModelUser.delsolic(db, request.form['solicitud'])
        flash("Bien!    Solicitud de Cita borrada correctamente.")
        return (redirect(url_for('gestsolic')))
    else:
        solicitudes = ModelUser.consultsolicstaff(db)
        return render_template('gestsolic-del.html', solic = solicitudes)

    # -- Checkear
@app.route('/checksolic/<numsolic>')
def checksolic(numsolic):
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
    form = UploadFileForm()
    if request.method == 'POST':
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
        examenes = ModelUser.consultexam_staff(db)
        usuarios = ModelUser.consultusers_staff(db)
        return render_template('gestexam.html', exams = examenes, users = usuarios, form = form)

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
    form = UploadFileForm()
    if request.method == 'POST':
        if form.validate_on_submit():

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

            # return "muchacho argentina Campeooooon"
    else:
        usuarios = ModelUser.consultpacexam_staff(db)
        citas = ModelUser.consultcitexam_staff(db)
        return render_template('gestexam-add.html', users = usuarios, cits = citas, form=form)



    # Borrar
@app.route('/gestexam/del' , methods = ['GET' , 'POST'])
def gestexamdel():
    form = UploadFileForm()
    if request.method == 'POST':
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
        examenes = ModelUser.consultexam_staff(db)
        usuarios = ModelUser.consultusers_staff(db)
        return render_template('gestexam-del.html', exams = examenes, users = usuarios, form = form)

@app.route('/delexam' , methods = ['GET', 'POST'])
def delexam():
    if request.method == 'POST':
        numexam = request.form['numDel']
        ModelUser.delexam_staff(db, numexam)
        flash("Bien!    Examen borrado correctamente.")
        return (redirect(url_for('gestexam')))
    else:
        return (redirect(url_for('gestexam')))


    
    #Editar
@app.route('/gestexam/edit', methods = ['GET' , 'POST'])
def gestexamedit():
    form = UploadFileForm()
    if request.method == 'POST':
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
        examenes = ModelUser.consultexam_staff(db)
        usuarios = ModelUser.consultusers_staff(db)
        return render_template('gestexam-modify.html', exams = examenes, users = usuarios, form = form)

@app.route('/gestexam/edit/t', methods = ['POST' , 'GET'])
def updtexam():
    form = UploadFileForm()
    if request.method == 'POST':
        numexam = request.form['numEdit']
        citEdit = ModelUser.consultexamedit_staff(db, numexam)
        usuarios = ModelUser.consultpacexam_staff(db)
        citas = ModelUser.consultcitcomp_staff(db)
        return render_template('gestexam-edit.html', cits = citas, users = usuarios, citEdit = citEdit, form = form)
    else:
        return redirect(url_for('gestexam'))


@app.route('/edtexam/<numexam>', methods = ['POST' , 'GET'])
def edtexam(numexam):
    form = UploadFileForm()
    if request.method == 'POST':
        if form.validate_on_submit():
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

            if len(file_name.read()) == 0:
                ModelUser.updtexam_doc_staff(db, )
                doc_id = ModelUser.consultdocexam_staff(db, file_name.filename, file_name.read())
                ModelUser.updtexam_valores_staff(db, numexam, idpac, tipo, cita, fecha, gr, gb, emoglobina, hematocritos, plaquetas, vcm, hcm, chcm, doc_id)
            else:
                doc_id = None
                ModelUser.updtexam_valores_staff(db, numexam, idpac, tipo, cita, fecha, gr, gb, emoglobina, hematocritos, plaquetas, vcm, hcm, chcm, doc_id)
            
            flash("Bien!    Examen actualizado correctamente.")
            return (redirect(url_for('gestexam')))
    else:
        return redirect(url_for('gestexam'))



# 3 -- Vista Citas

    # Consulta
@app.route('/gestcit', methods = ['POST' , 'GET'])
def gestcit():
    if request.method == 'POST':
        return "vista post"
    else:
        return "vista get"




#Vistas para Errores
    #url protegida
def status_401(error):
    return redirect(url_for('login'))

    #url inexistente
def status_404(error):
    return "<h1>Pagina no encontrada.</h1>" , 404




# -- Ruta para propositos de testeos.
@app.route('/test', methods = ['GET' , 'POST'])
def test():
    form = UploadFileForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            file_data = form.file.data
            file_data.filename = 'Examen{0}_{1}_{2}'.format('1', secure_filename('Maribel Rondon'), '2022-12-04')

            ModelUser.updtexam_doc_staff(db, '1', file_data.filename, file_data.read())
            flash("Bien!    Examen actualizado correctamente.")
            return redirect(url_for('test'))
    else:
        return render_template('test.html', form = form)

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
