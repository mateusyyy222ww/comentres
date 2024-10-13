from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('comments.db')
    conn.row_factory = sqlite3.Row
    return conn

# Inicializa o banco de dados
def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS comments (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, comment TEXT)')
    conn.commit()
    conn.close()

# Rota para a página principal
@app.route('/')
def index():
    conn = get_db_connection()
    comments = conn.execute('SELECT * FROM comments').fetchall()
    conn.close()
    return render_template('index.html', comments=comments)

# Rota para adicionar um novo comentário
@app.route('/add_comment', methods=['POST'])
def add_comment():
    name = request.form['name']
    comment = request.form['comment']
    
    conn = get_db_connection()
    conn.execute('INSERT INTO comments (name, comment) VALUES (?, ?)', (name, comment))
    conn.commit()
    conn.close()
    
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
