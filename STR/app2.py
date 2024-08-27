from flask import Flask, render_template, request, redirect, url_for, session
import pymongo
from bson.objectid import ObjectId  

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

users = {
    'PneusVisa': {'password': 'Abacate123', 'role': 'admin'},
}

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["PneusVisa"]
collection = db["Cadastros"]

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username]['password'] == password:
        session['username'] = username
        session['role'] = users[username]['role']
        return redirect(url_for('index'))
    else:
        return "Login falhou. Verifique seu nome de usuário e senha."

@app.route('/index')
def index():
    message = session.pop('message', None)
    return render_template('index.html', message=message)

@app.route('/submit_checklist', methods=['POST'])
def submit_checklist():
    cadastro = {
        'responsible': request.form['responsible'],
        'username': request.form['username'],
        'password': request.form['password'],
        'email': request.form['email'],
        'last_cleaning': request.form['last_cleaning'],
        'cidade': request.form['cidade']
    }
    collection.insert_one(cadastro)
    
    session['message'] = 'Novo cadastro criado com sucesso!'
    
    return redirect(url_for('index'))

@app.route('/itumbiara')
def itumbiara():
    usuarios = collection.find({'cidade': 'itumbiara'})
    return render_template('itumbiara.html', usuarios=usuarios)

@app.route('/edeia')
def edeia():
    usuarios = collection.find({'cidade': 'edeia'})
    return render_template('edeia.html', usuarios=usuarios)

@app.route('/rioverde')
def rioverde():
    usuarios = collection.find({'cidade': 'rioverde'})
    return render_template('rioverde.html', usuarios=usuarios)

@app.route('/goiatuba')
def goiatuba():
    usuarios = collection.find({'cidade': 'goiatuba'})
    return render_template('goiatuba.html', usuarios=usuarios)

@app.route('/editar_usuario/<id>', methods=['GET', 'POST'])
def editar_usuario(id):
    if request.method == 'GET':
        usuario = collection.find_one({'_id': ObjectId(id)})
        return render_template('editar_usuario.html', usuario=usuario)
    
    if request.method == 'POST':
        dados_atualizados = {
            'responsible': request.form['responsible'],
            'username': request.form['username'],
            'password': request.form['password'],
            'email': request.form['email'],
            'last_cleaning': request.form['last_cleaning'],
            'cidade': request.form['cidade']
        }
        collection.update_one({'_id': ObjectId(id)}, {'$set': dados_atualizados})
        return redirect(url_for('itumbiara'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
