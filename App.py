from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# Conexión con MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'vladimir'
app.config['MYSQL_PASSWORD'] = 'Abcd2467'
app.config['MYSQL_DB'] = 'informesc3'
mysql = MySQL(app)

# Sesión
app.secret_key = 'mysecretkey' # para decirle como se protegerá la sesión

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('select id,nombres,grupo,correo from responsable')
    data = cur.fetchall() # para tener todos los datos
    #print(data)
    return render_template('index.html', responsables = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        nombres = request.form['nombres']
        grupo = request.form['grupo']
        correo = request.form['correo']
        
        cur = mysql.connection.cursor()
        cur.execute('insert into responsable (nombres, grupo, correo) values (%s, %s, %s)',
        (nombres, grupo,correo))
        mysql.connection.commit()
        flash('Técnico guardado')
        return redirect(url_for('Index'))

@app.route('/edit/<id>')
def get_responsable(id):
    cur = mysql.connection.cursor()
    cur.execute('select id,nombres,grupo,correo from responsable where id = {0}'.format(id))
    data = cur.fetchall() # para tener todos los datos
    return render_template('edit_respons.html', tecnico = data[0])
  #  return render_template('edit_respons.html', tecnico = data[0]) # en la variable "tecnico" se van los datos a la otra vista

@app.route('/update/<id>', methods = ['POST'])
def updateRespons(id):
    if request.method == 'POST':
        nombres = request.form['nombres']
        grupo = request.form['grupo']
        correo = request.form['correo']
        cur = mysql.connection.cursor()
        cur.execute("""
        update responsable
        set nombres = %s,
            grupo = %s,
            correo = %s
        where id = %s
    """,(nombres, grupo, correo, id))
    mysql.connection.commit()
    flash('Responsable actualizado')
    return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_responsable(id):
    #return id
    cur = mysql.connection.cursor()
    cur.execute('delete from responsable where id = {0}'.format(id))
    mysql.connection.commit()
    flash('Técnico eliminado')
    return redirect(url_for('Index'))

if __name__== '__main__':
    app.run(port = 3000, debug = True)


