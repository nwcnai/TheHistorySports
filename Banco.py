import sqlite3
conexao = sqlite3.connect('banco.db')
cursor = conexao.cursor()
cursor.execute(
    'CREATE TABLE IF NOT EXISTS Usuarios('
    'id INTEGER PRIMARY KEY AUTOINCREMENT,'
    'Email TEXT NOT NULL,'
    'Senha TEXT NOT NULL,'
    'DataRegistro DATE NOT NULL)'
)