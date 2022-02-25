from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'your_mysql_host' 
app.config['MYSQL_USER'] = 'your_mysql_user'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'your_mysql_db'

mysql = MySQL(app)

app.secret_key = "secret_key"

@app.route('/')
def get_notes():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM notes')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', notes = data)

@app.route('/add_note', methods=['POST'])
def add_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO notes (title, content) VALUES (%s,%s)", (title, content))
        mysql.connection.commit()
        flash('Note Added')
        return redirect(url_for('get_notes'))

@app.route('/edit_note/<id>', methods = ['POST', 'GET'])
def get_note(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM notes WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-note.html', note = data[0])

@app.route('/update_note/<id>', methods=['POST'])
def update_user(id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE notes
            SET title = %s,
                content = %s
            WHERE id = %s
        """, (title, content, id))
        flash('Note Updated')
        mysql.connection.commit()
        return redirect(url_for('get_notes'))

@app.route('/delete_note/<string:id>', methods = ['POST','GET'])
def delete_note(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM notes WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Note Removed')
    return redirect(url_for('get_notes'))

if __name__ == "__main__":
    app.run(port=3000, debug=True)