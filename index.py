from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect

from config import config

# Herramienta para Imagenes y Comprobaciones.
import cv2

#Herramienta para convertir Dates a String
import datetime

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





# -- Rutas a partir del login (FAVOR PROTEGER RUTAS UNA VEZ FINALIZADO SU DISEÑO)

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
        return 'Secretaria che'
    else:
        #Renderizado de plantilla Admin.
        return 'Admin papa'
    

    # -- Rutas de utilidades Vista usuario.
        # -- Gestionar Examenes
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
    
    
    # -- Solicitar citas
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
        ModelUser.newsolic(db, current_user.get_id(), request.form['tipo'], request.form['fecha'], request.form['acotaciones'], 2)
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
        ModelUser.updatesolic(db, request.form['tipo'], request.form['fecha'], request.form['acotaciones'], numsolic, current_user.get_id())
    
        flash("Bien!    Solicitud de Cita actualizada correctamente.")
        return (redirect(url_for('requestdate')))
    else:
        return (redirect(url_for('requestdate')))




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
