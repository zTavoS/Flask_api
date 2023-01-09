from flask import Flask, request
import mysql.connector

# Crea una instancia de Flask
app = Flask(__name__)

# Crea una conexión con la base de datos
cnx = mysql.connector.connect(user='tu_usuario', password='tu_contraseña',
                              host='localhost', database='tu_base_de_datos')

# Crea un cursor para realizar consultas
cursor = cnx.cursor()


# Crea una ruta para la API
@app.route('/api/agregar_dato', methods=['POST'])
def agregar_dato():
    # Obtiene los datos del formulario
    dato1 = request.form['dato1']
    dato2 = request.form['dato2']

    # Crea una consulta para insertar los datos
    query = 'INSERT INTO tabla (campo1, campo2) VALUES (%s, %s)'
    values = (dato1, dato2)

    # Ejecuta la consulta
    cursor.execute(query, values)
    cnx.commit()

    # Devuelve un mensaje de éxito
    return 'Dato agregado exitosamente'
