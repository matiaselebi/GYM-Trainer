from flask import Flask, jsonify, render_template, request
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('gimnasio.db')
    conn.row_factory = sqlite3.Row
    return conn

def obtener_fecha_dia(nombre_dia, semanas_atras):
    dias_map = {'Lunes': 0, 'Martes': 1, 'Miercoles': 2, 'Jueves': 3, 'Viernes': 4}
    ahora = datetime.now()
    if ahora.hour < 4:
        ahora -= timedelta(days=1)
        
    lunes_actual = ahora - timedelta(days=ahora.weekday())
    lunes_objetivo = lunes_actual - timedelta(weeks=semanas_atras)
    fecha_exacta = lunes_objetivo + timedelta(days=dias_map[nombre_dia])
    
    return fecha_exacta.strftime('%Y-%m-%d')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/rutina/<dia>/<int:semanas_atras>')
def get_rutina(dia, semanas_atras):
    fecha_calculada = obtener_fecha_dia(dia, semanas_atras)
    conn = get_db_connection()
    
    rutina = conn.execute('''
        SELECT r.ejercicio_id, e.nombre, r.series_objetivo, r.reps_rango, r.notas, r.orden
        FROM rutina_dias r
        JOIN ejercicios e ON r.ejercicio_id = e.id
        WHERE r.dia = ? ORDER BY r.orden
    ''', (dia,)).fetchall()
    
    historial = conn.execute('''
        SELECT ejercicio_id, numero_serie, repeticiones, peso 
        FROM historial WHERE fecha = ?
    ''', (fecha_calculada,)).fetchall()
    conn.close()
    
    return jsonify({
        'rutina': [dict(ix) for ix in rutina],
        'historial': [dict(ix) for ix in historial],
        'fecha_sesion': fecha_calculada
    })

@app.route('/guardar_serie', methods=['POST'])
def guardar_serie():
    data = request.json
    conn = get_db_connection()
    try:
        conn.execute('''
            INSERT INTO historial (fecha, ejercicio_id, numero_serie, repeticiones, peso)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(fecha, ejercicio_id, numero_serie) 
            DO UPDATE SET repeticiones=excluded.repeticiones, peso=excluded.peso
        ''', (data['fecha'], data['ejercicio_id'], data['numero_serie'], data['reps'], data['peso']))
        conn.commit()
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)