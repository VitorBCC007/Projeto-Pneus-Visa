from flask import Flask, render_template, request, redirect, url_for, session
import pymongo
from bson.objectid import ObjectId  # Importa para manipular ObjectId do MongoDB

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Substitua por uma chave secreta real

# Dados de login para os usuários
users = {
    'PneusVisa': {'password': 'Abacate123', 'role': 'admin'},
}

# Configuração do MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["PneusVisa"]
collection = db["Cadastros"]

# Rota para a página de login
@app.route('/')
def login():
    return render_template('login.html')

# Rota para processar o login
@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']

    # Verifica se o usuário existe e a senha está correta
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
    # Lógica para processar o checklist
    # Exemplo de inserção no MongoDB
    cadastro = {
        'responsible': request.form['responsible'],
        'username': request.form['username'],
        'password': request.form['password'],
        'email': request.form['email'],
        'last_cleaning': request.form['last_cleaning'],
        'cidade': request.form['cidade']
    }
    collection.insert_one(cadastro)
    
    # Define a mensagem de sucesso na sessão
    session['message'] = 'Novo cadastro criado com sucesso!'
    
    return redirect(url_for('index'))

@app.route('/itumbiara')
def itumbiara():
    # Consulta para encontrar usuários na cidade de Itumbiara
    usuarios = collection.find({'cidade': 'Itumbiara'})
    return render_template('itumbiara.html', usuarios=usuarios)

@app.route('/editar_usuario/<id>', methods=['GET', 'POST'])
def editar_usuario(id):
    # Se for uma solicitação GET, exibe o formulário de edição com dados do usuário
    if request.method == 'GET':
        usuario = collection.find_one({'_id': ObjectId(id)})
        return render_template('editar_usuario.html', usuario=usuario)
    
    # Se for uma solicitação POST, atualiza os dados do usuário
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
