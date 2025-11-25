import sqlite3 as sq
from datetime import datetime
import time



def criar_tabela():
    conexao = sq.connect('forge.db')
    cursor = conexao.cursor()


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            tema TEXT,
            inicio TEXT,
            fim TEXT,
            duracao TEXT,
            nota_ia INTEGER
        )
        ''')
    
    conexao.commit()
    conexao.close()

def iniciar_sessao(usuario_id, tema):
    data_atual = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
 
    conexao = sq.connect('forge.db')
    cursor = conexao.cursor() 

    cursor.execute('INSERT INTO sessoes (usuario_id, tema, inicio ) VALUES (?, ?, ?)', (usuario_id, tema, data_atual))
    
    conexao.commit()

    id_gerado = cursor.lastrowid

    conexao.close()

    return id_gerado

def encerrar_sessao(id_sessao):
    data_fim = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    conexao = sq.connect('forge.db')
    cursor = conexao.cursor() 

  
    cursor.execute('SELECT inicio FROM sessoes Where id = ?', (id_sessao,))
    resultado = cursor.fetchone()

   
    if resultado is None:
        print("Erro: Sessão não encontrada ou ID inválido!")
        conexao.close()
        return None

    inicio_string = resultado[0]

    formato = '%d/%m/%Y %H:%M:%S'
    t_inicio = datetime.strptime(inicio_string, formato)
    t_fim = datetime.strptime(data_fim, formato)

    duracao = t_fim - t_inicio
    
   
    duracao_str = str(duracao).split('.')[0]

    
    cursor.execute('''
        UPDATE sessoes
        SET fim = ?, duracao = ?
        WHERE id = ?
    ''', (data_fim, duracao_str, id_sessao))
    
    conexao.commit()
    conexao.close()
    
    return duracao_str

def ler_historico():
    
    conexao = sq.connect('forge.db')
    cursor = conexao.cursor()
 
    cursor.execute('SELECT * FROM sessoes ORDER BY id DESC')
   
    lista_sessoes = cursor.fetchall()
    conexao.close()

    return lista_sessoes


def del_sessao(usuario_id):
    conexao = sq.connect('forge.db')
    cursor = conexao.cursor()

    cursor.execute('''
DELETE FROM sessoes WHERE id = (SELECT MAX(id) FROM sessoes WHERE usuario_id = ?)
''',(usuario_id,))
    
    conexao.commit()
    conexao.close()