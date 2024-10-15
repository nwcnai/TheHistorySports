from flask import Flask, render_template, g, request, redirect
import sqlite3
from flask_cors import CORS
from datetime import datetime
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

def ligar_banco():
    banco = g._database = sqlite3.connect('banco.db')
    return banco
@app.route('/')
def login():
    return render_template('login.html', titulo='Login - THS')

@app.route('/registro')
def registro():
    return render_template('registro.html', titulo='Registro - THS')


@app.route('/home/<email>')
def home(email):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT Nome FROM Usuarios WHERE Email = ?;', (email,))
    usuario = cursor.fetchone()

    if usuario:
        nome = usuario[0]
    else:
        nome = 'Usuário'

    return render_template('home.html', titulo='The History Of Sports', estilo='home', nome=nome, email=email)

@app.route('/futebolamericano/<email>')
def futebolamericano(email):
    return render_template('futebolamericano.html', titulo='Futebol Americano - THS', estilo='futebolamericano', email=email)

@app.route('/futebol/<email>')
def futebol(email):
    return render_template('futebol.html', titulo='Futebol - THS', estilo='futebol', email=email)

@app.route('/basquete/<email>')
def basquete(email):
    return render_template('basquete.html', titulo='Basquete - THS', estilo='basquete', email=email)

@app.route('/voleibol/<email>')
def voleibol(email):
    return render_template('voleibol.html', titulo='Voleibol - THS', estilo='voleibol', email=email)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    email = request.form['email']
    senha = request.form['senha']

    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT Senha FROM Usuarios WHERE Email = ?;',(email,))
    usuario = cursor.fetchone()

    if usuario and usuario[0] == senha:
        return redirect(f'/home/{email}')
    else:
        return render_template('Login.html', mensagem='Usuário ou senha incorretos, tente novamente.')

@app.route('/cadusuario', methods=['GET', 'POST'])
def cadusuario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        datanasc = request.form['datanasc']

        lista_erros = []
        banco = ligar_banco()
        cursor = banco.cursor()

        cursor.execute("SELECT COUNT(*) FROM Usuarios WHERE Email = ?", (email,))
        resultado = cursor.fetchone()

        if resultado[0] > 0:
            lista_erros.append('O e-mail já esta em uso por outra conta.')

        data_nasc = datetime.strptime(datanasc, '%Y-%m-%d')
        idade = (datetime.now() - data_nasc).days // 365

        if idade < 16:
            lista_erros.append("Idade mínima: 16+ anos.")

        if lista_erros:
            quantidade_erros = len(lista_erros)
            banco.close()
            return render_template('registro.html', mensagememail=lista_erros, quantidade_erros=quantidade_erros)

        cursor.execute('INSERT INTO Usuarios (Nome, Email, Senha, DataRegistro) VALUES (?, ?, ?, ?)',
                       (nome, email, senha, datanasc))
        banco.commit()
        banco.close()

        return render_template('registro.html')
    return render_template('registro.html')

@app.route('/editarusuario/<email>', methods=['GET', 'POST'])
def editarusuario(email):
    banco = ligar_banco()
    cursor = banco.cursor()

    if request.method == 'POST':
        botaoeditar = request.form['botaoeditar']

        if botaoeditar == 'salvar':
            nome = request.form['nome']
            senha = request.form['senha']
            datanasc = request.form['datanasc']

            lista_erros = []

            data_nasc = datetime.strptime(datanasc, '%Y-%m-%d')
            idade = (datetime.now() - data_nasc).days // 365

            if idade < 16:
                lista_erros.append("Idade mínima: 16+ anos.")

            if lista_erros:
                quantidade_erros = len(lista_erros)
                banco.close()
                return render_template('editarusuario.html', titulo='Editar Conta - THS', nome=nome, email=email, senha=senha, datanasc=datanasc, mensagememail=lista_erros, quantidade_erros=quantidade_erros)

            cursor.execute('UPDATE Usuarios SET Nome = ?, Senha = ?, DataRegistro = ? WHERE Email = ?', (nome, senha, datanasc, email))
            banco.commit()
            banco.close()

            return redirect(f'/home/{email}')

        elif botaoeditar == 'excluir':
            cursor.execute('DELETE FROM Usuarios WHERE Email = ?', (email,))
            banco.commit()
            banco.close()

            return redirect('/')

    cursor.execute('SELECT Nome, Email, Senha, DataRegistro FROM Usuarios WHERE Email = ?', (email,))
    usuario = cursor.fetchone()

    if usuario:
        nome, email, senha, datanasc = usuario
        return render_template('editarusuario.html', titulo='Editar Conta - THS', nome=nome, email=email, senha=senha, datanasc=datanasc)
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run()