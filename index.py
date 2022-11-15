from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required

from config import config

# Herramienta para Imagenes y Comprobaciones.
import cv2

# Modelos
from models.ModelUser import ModelUser
# Entidades
from models.entities.User import User, NewUser, ConsultUser, ConsultEmail




app = Flask(__name__)

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
                return redirect(url_for('test'))
            else:
                flash("Vaya.... Password invalido.             #ff0000")
                return redirect(url_for('testlogin'))
        else:
            flash("Vaya.... Usuario no encontrado.         #ff0000")
            return redirect(url_for('testlogin'))
    else:
        return redirect(url_for('testlogin'))

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
                return redirect(url_for('testregister'))

            # Si llego hasta aca significa que no tiene caracteres especiales y cumple en longitud.
                # Comprobando si existe ya en la base de datos
            user = ConsultUser(username)
            checkvalue = ModelUser.checkuser(db, user) 

            # Si retorna un 1 es que no existe el username, si retorna un 0 si existe.
            if checkvalue == '1':
                #--email
                    #Comprobacion de que el email no existe en la BD.
                email = ConsultEmail(email)
                checkvalue = ModelUser.checkemail(db, email)

                # Si retorna un 1 es que no existe el email, si retorna un 0 si existe.
                if checkvalue == '1':
                    print("Llegue hasta aquix2")
                    profile_pic = cv2.imread('static/img/98681.jfif')
                    user = NewUser(0, username, password, fullname, email, address, genre, cellphone, profile_pic)
                    ModelUser.register(db, user)
                    flash('Bien!    Se ha registrado correctamente.#2DE94F')
                    return redirect(url_for('testlogin'))
                else:
                    flash('Vaya...  Email ya registrado, usa otro.')
                    return redirect(url_for('testregister'))
            else:
                flash('Vaya...  Usuario ya registrado, intenta con otro.')
                return redirect(url_for('testregister'))
        else:
            flash("Vaya.... Usuario no permitido. Debe tener entre 4 y 12 caracteres.")
            return (redirect(url_for('testregister')))
    else:
        return (redirect(url_for('testregister')))

    # Ruta principal De Registro.
@app.route('/register')
def register():
    return render_template('register.html')







# -- Ruta para propositos de testeos.
@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/testlogin')
def testlogin():
    return render_template('testlogin.html')


@app.route('/testregister')
def testregister():
    return render_template('testregister.html')


@app.route('/protected')
@login_required
def protected():
    return "<h1>Vista protegida, solo para usuarios autentificados</h1>"


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(debug=True)
