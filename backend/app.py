from flask import Flask, request
import mysql.connector

# Crea una instancia de Flask
app = Flask(__name__)

# app.debug = True


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


# Crea una conexión con la base de datos
class DBManager:
    def __init__(self, database='example', host="db", user="root", password=None):
        
        self.connection = mysql.connector.connect(
            user=user,
            password=password,
            host=host,  # name of the mysql service as set in the docker compose file
            database=database,
            auth_plugin='mysql_native_password'
        )

        self.cursor = self.connection.cursor()
        self.cursor.execute("Create table IF NOT EXISTS clientes(id int(11) PRIMARY KEY AUTO_INCREMENT, nombre varchar(150) NOT NULL, celular varchar(14) NOT NULL, correo varchar(150) NOT NULL);")
        self.connection.commit()

    def insert_clientes(self, clientes):
        self.cursor.executemany('INSERT INTO clientes (nombre, celular, correo) VALUES (%s, %s, %s);', [(clientes[i]["nombre"], clientes[i]["celular"], clientes[i]["correo"]) for i in range(0, len(clientes))])
        self.connection.commit()

    def list_clientes(self):
        self.cursor.execute('SELECT * FROM clientes')
        rows = dictfetchall(self.cursor)
        return rows

    def eliminar_cliente(self, client_id):
        for cliente in client_id:
            print("DELETE FROM clientes WHERE id={cliente}".format(cliente=cliente))
            self.cursor.execute("DELETE FROM clientes WHERE id={cliente}".format(cliente=cliente))
            self.connection.commit()


cnx = DBManager(password='db-78n9n')


@app.route('/api/agregar_cliente', methods=['POST'])
def agregar_cliente():
    # Obtiene los datos del formulario
    cnx.insert_clientes([{
        "nombre": request.form.get('nombre'),
        "correo": request.form.get('correo'),
        "celular": request.form.get('celular')
    }])

    clientes = cnx.list_clientes()
    return clientes


@app.route('/api/agregar_clientes', methods=['POST'])
def agregar_clientes():
    clientes_data = request.get_json()["clientes"]
    print(clientes_data)
    cnx.insert_clientes(clientes_data)
    clientes = cnx.list_clientes()
    return clientes


@app.route('/api/clientes', methods=['GET'])
def list_clientes():
    clientes = cnx.list_clientes()
    return clientes


@app.route('/api/eliminar_cliente', methods=['POST'])
def eliminar_cliente():
    cliente_id = request.form.get('id').split(',')
    print(cliente_id)
    cnx.eliminar_cliente(cliente_id)
    clientes = cnx.list_clientes()
    return clientes

