from flask import Flask,render_template, redirect, url_for,session,logging, request, flash
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators,BooleanField, IntegerField
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'

app.config['MYSQL_PASSWORD'] = 'hola123'
app.config['MYSQL_DB'] = 'ravenclaw'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template('about.html')

class RegisterFormUser(Form):
    rut = StringField('Rut', validators=[validators.Length(min=11, max=12)])
    nombre = StringField('Nombre Completo', validators=[validators.Length(min=4, max=200)])

    password = PasswordField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirmar',message='La clave no coincide')
    ])
    confirmar = PasswordField('Confirme su clave')
    telefono = IntegerField('Telefono', validators=[validators.Length(min=9,max=9)])

@app.route('/registerclientes',methods=['GET','POST'])
def registerUser():
    form = RegisterFormUser(request.form)
    if request.method  == 'POST' and form.validate():
        rut = form.rut.data
        nombre = form.nombre.data
        telefono = form.telefono.data
        cant_libros = '0'
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO clientes(rut,nombre,telefono,password,cant_libros) VALUES(%s, %s, %s, %s, %s)", (rut,nombre,telefono,password,cant_libros))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('Genial ahora estas registrado y puedes ingresar a la pagina', 'success')

        return redirect(url_for('index'))
    return render_template('registerClientes.html', form = form)

@app.route('/loginClientes',methods=['GET','POST'])
def loginUser():
    if request.method == 'POST':

        rut = request.form['rut']
        password_candidate = request.form['password']

        cur = mysql.connection.cursor()

        result = cur.execute("SELECT * FROM clientes WHERE rut = %s",[rut])

        if result > 0:
            data = cur.fetchone()
            password = data['password']

            if sha256_crypt.verify(password_candidate,password):
                # app.logger.info('clave correcta')
                session['logeado_C'] = True
                session['rut'] = rut

                flash('ahora te encuentras logeado','success')

            else:
                error = 'clave incorrecta'
                return render_template('loginClientes.html', error=error)

        else:
            error = 'Usuario no encontrado'
            return render_template('loginClientes.html', error=error)

    return render_template('loginClientes.html')

@app.route('/logoutClientes')
def logoutUser():
    session.clear()
    return redirect(url_for('index'))

def is_logged_inC(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logeado_C' in session:
            return f(*args, **kwargs)
        else:
            flash('acceso denegado,por favor inicia sesion o registrate','danger')
            return redirect(url_for('logoutUser'))
    return wrap

class RegisterFormAdmin(Form):
    rut = StringField('rut', validators=[validators.Length(min=10, max=11)])
    nombre = StringField('Nombre Completo', validators=[validators.Length(min=4, max=200)])
    password = PasswordField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirmar',message='La clave no coincide')
    ])
    confirmar = PasswordField('Confirme su clave')
@app.route('/registerempleados',methods=['GET','POST'])
def registerAdmin():
    form = RegisterFormAdmin(request.form)
    if request.method  == 'POST' and form.validate():
        rut = form.rut.data
        nombre = form.nombre.data
        password = sha256_crypt.encrypt(str(form.password.data))


        cur = mysql.connection.cursor()


        cur.execute("INSERT INTO empleados(rut,nombre,password) VALUES(%s, %s, %s)",(rut,nombre,password))

        mysql.connection.commit()

        cur.close()

        flash('Genial ahora estas registrado y puedes ingresar a la pagina', 'success')

        return redirect(url_for('index'))
    return render_template('registerEmpleados.html', form = form)



@app.route('/loginEmpleados',methods=['GET','POST'])
def loginAdmin():
    if request.method == 'POST':

        rut = request.form['rut']
        password_candidate = request.form['password']

        cur = mysql.connection.cursor()

        result = cur.execute("SELECT * FROM empleados WHERE rut = %s",[rut])

        if result > 0:
            data = cur.fetchone()
            password = data['password']

            if sha256_crypt.verify(password_candidate,password):
                # app.logger.info('clave correcta')
                session['logeado_E'] = True
                session['rut'] = rut

                flash('ahora te encuentras logeado','success')
                return redirect(url_for(''))
            else:
                error = 'clave incorrecta'
                return render_template('loginEmpleados.html', error=error)

        else:
            error = 'Usuario no encontrado'
            return render_template('loginEmpleados.html', error=error)

    return render_template('loginEmpleados.html')

@app.route('/logoutEmpleados')
def logoutAdmin():
    session.clear()
    return redirect(url_for('index'))

def is_logged_inC(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logeado_E' in session:
            return f(*args, **kwargs)
        else:
            flash('acceso denegado,por favor inicia sesion o registrate','danger')
            return redirect(url_for('loginAdmin'))
    return wrap

@app.route('/dashboard')
@is_logged_inC
def dashboardR():
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM repisas")
    return render_template('dashboard.html')

class RegisterFormBook(Form):
    id = IntegerField('id', validators=[validators.Length(min=1,max=200000)])
    nombre = StringField('nombre', validators=[validators.Length(min=4, max=2000)])
    autor = StringField('autor', validators=[validators.Length(min=4, max=2000)])
    prestado = BooleanField('prestado', default=True)


@app.route('/dashboardB')
@is_logged_inC
def dashboardBooks():
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM libros")
    return render_template('dashboardB.html')


@app.route('/registerB')
def add_Book():
    form = RegisterFormBook(request.form)
    if request.method == 'POST' and form.validate():
        id = id.form.data
        nombre = nombre.form.data
        autor = autor.form.data
        prestado = prestado.form.data


        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO libros(id,nombre,autor,prestado,id_repisa) VALUES(%s, %s, %s, %s, %s)",(id,nombre,autor,prestado,session['id']))

        mysql.connection.commit()

        cur.close()


@app.route('/dashboardR')
@is_logged_inC
def dashboardR():
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM repisas")
    return render_template('dashboardR.html')

class RegisterFormR(Form):
    id = IntegerField('id', validators=[validators.Length(min=1,max=200000)])
    categoria = StringField('categoria', validators=[validators.Length(min=4, max=2000)])

@app.route('/add_Repisa', methods=['GET','POST'])
def add_Repisa():
    form = RegisterFormR(request.form)
    if request.method == 'POST' and form.validate():
        id = id.form.data
        categoria = categoria.form.data

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO repisas(id,categoria) VALUES(%s, %s)",(id,categoria))

        mysql.connection.commit()

        cur.close()


if __name__ == "__main__":
    app.secret_key = 'secret123'
    app.run(debug=True)
