import hashlib
import sys
import sqlite3 as sql

def hash_a_file(file):
    with open(file, 'rb') as f:
        binary = f.read()

    sha256 = hashlib.sha256()
    sha256.update(binary)

    return sha256.hexdigest()

def add_file_db(file):
    try:
        connection = sql.connect('hash.db')
    
        cursor = connection.cursor()

        insert_query = "INSERT INTO hash_table (name, hash) VALUES(?, ?)"

        hash_file = hash_a_file(file)

        data_tuple = (file, hash_file)

        cursor.execute(insert_query, data_tuple)

        print(f"{file} adicionado!")
        connection.commit()
        cursor.close()
    except sql.Error as erro:
        print(f"Erro ao inserir o hash {erro}")
    finally:
        if connection:
            connection.close()



def verifica_integridade(file):
    try:
        connection = sql.connect('hash.db')
        
        cursor = connection.cursor()

        query = "SELECT * FROM hash_table WHERE name = ?"

        cursor.execute(query, (file,))

        data = cursor.fetchone()

        if not data:
            print("Arquivo não existe no banco de dados")
        else:
            hash_file = hash_a_file(file)


            if hash_file == data[1]:
                print(f"O arquivo {data[0]} OK")
            else:
                print(f"Hash de arquivo {data[0]} foi alterado")
        cursor.close()
    except sql.Error as erro:
        print(f"Erro {erro}")
    finally:
        if connection:
            connection.close()


if sys.argv[1] == "adiciona":
    add_file_db(sys.argv[2])
elif sys.argv[1] == "verifica":
    verifica_integridade(sys.argv[2])


#RODE ASSIM: py hash.py adiciona ou verifica [NOMEDOARQUIVO]

    


    







