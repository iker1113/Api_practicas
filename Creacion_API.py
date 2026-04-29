from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from flask import render_template
from cryptography.fernet import Fernet

app = Flask(__name__)
CORS(app)

CLAVE_MAESTRA = b'Nfg779UgPJbucDOwLKDbdc3H8jksw6W3vJ-1eA7H7uE=' 
cipher_suite = Fernet(CLAVE_MAESTRA)

def conectar_db():
    return mysql.connector.connect(
        host="172.31.1.205", 
        user="api.user", 
        password="api_password",
        database="apihospitalprueba",
        auth_plugin='mysql_native_password'
    )

@app.route('/')
def home():

    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    datos = request.json
    db = conectar_db()
    cursor = db.cursor(dictionary=True)
    

    query = "SELECT * FROM login WHERE usuario = %s"
    cursor.execute(query, (datos.get('usuario'),))
    user = cursor.fetchone()
    db.close()

    if user:
        try:
            
            pass_en_db_encriptada = user['contraseña'].encode()
            pass_desencriptada_bytes = cipher_suite.decrypt(pass_en_db_encriptada)
            pass_final = pass_desencriptada_bytes.decode()

            
            if pass_final == datos.get('password'):
                return jsonify({"autorizado": True}), 200
        except Exception:
            
            return jsonify({"autorizado": False}), 401

    return jsonify({"autorizado": False}), 401 #

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
        
        pass_plana = datos.get('pass').encode()
        pass_encriptada = cipher_suite.encrypt(pass_plana).decode() 

        db = conectar_db()
        cursor = db.cursor()
        query = "INSERT INTO login (usuario, contraseña) VALUES (%s, %s)"
        cursor.execute(query, (datos.get('usuario'), pass_encriptada))
        
        db.commit()
        db.close()
        return jsonify({"mensaje": "Usuario creado"}), 201
    except Exception as err:
        return jsonify({"error": str(err)}), 400 #
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,)

   
