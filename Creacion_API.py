from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

def conectar_db():
    return mysql.connector.connect(
        host="172.31.1.204", 
        user="Iker.Puya", 
        password="11132007",
        database="apihospitalprueba"
    )

@app.route('/login', methods=['POST'])
def login():
    datos = request.json
    db = conectar_db()
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM login WHERE usuario = %s AND contraseña = %s"
    cursor.execute(query, (datos.get('usuario'), datos.get('password')))
    user = cursor.fetchone()
    db.close()
    if user:
        return jsonify({"autorizado": True}), 200
    return jsonify({"autorizado": False}), 401

@app.route('/citas', methods=['GET'])
def obtener_citas():

    usuario_logueado = request.args.get('usuario')
    db = conectar_db()
    cursor = db.cursor(dictionary=True)
    
    
    query = "SELECT paciente, hora, especialidad, descripcion FROM cita WHERE doctor_asignado = %s"
    cursor.execute(query, (usuario_logueado,))
    
    filas = cursor.fetchall()
    db.close()
    for f in filas: f['hora'] = str(f['hora']) 
    return jsonify(filas)

@app.route('/citas', methods=['POST'])
def crear_cita():
    d = request.json
    db = conectar_db()
    cursor = db.cursor()
    sql = "INSERT INTO cita (paciente, hora, especialidad, descripcion, doctor_asignado) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (d.get('paciente'), d.get('hora'), d.get('especialidad'), d.get('descripcion'), d.get('doctor')))
    db.commit()
    db.close()
    return jsonify({"mensaje": "OK"}), 201

@app.route('/citas/<nombre>', methods=['DELETE'])
def eliminar_cita(nombre):
    db = conectar_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM cita WHERE paciente = %s", (nombre,))
    db.commit()
    db.close()
    return jsonify({"mensaje": "Borrado"}), 200

@app.route('/registro', methods=['POST'])
def registro():
    datos = request.json
    try:
        db = conectar_db()
        cursor = db.cursor()
        
        
        query = "INSERT INTO login (usuario, contraseña) VALUES (%s, %s)"
        cursor.execute(query, (datos.get('usuario'), datos.get('pass')))
        
        db.commit()
        db.close()
        return jsonify({"mensaje": "Usuario creado"}), 201
    except mysql.connector.Error as err:
        
        return jsonify({"error": str(err)}), 400
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,)
   
