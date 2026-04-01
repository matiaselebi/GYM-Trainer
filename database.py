import sqlite3

def crear_tablas():
    conexion = sqlite3.connect('gimnasio.db')
    cursor = conexion.cursor()

    cursor.execute('DROP TABLE IF EXISTS variantes')
    cursor.execute('DROP TABLE IF EXISTS rutina_dias')
    cursor.execute('DROP TABLE IF EXISTS historial')
    cursor.execute('DROP TABLE IF EXISTS ejercicios')

    cursor.execute('''
        CREATE TABLE ejercicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            grupo_muscular TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE rutina_dias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dia TEXT,
            ejercicio_id INTEGER,
            series_objetivo INTEGER,
            reps_rango TEXT,
            notas TEXT,
            es_calentamiento BOOLEAN,
            orden INTEGER,
            FOREIGN KEY(ejercicio_id) REFERENCES ejercicios(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE historial (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATE,
            ejercicio_id INTEGER,
            numero_serie INTEGER,
            repeticiones INTEGER,
            peso REAL,
            UNIQUE(fecha, ejercicio_id, numero_serie),
            FOREIGN KEY(ejercicio_id) REFERENCES ejercicios(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE variantes (
            ejercicio_id INTEGER,
            variante_id INTEGER,
            FOREIGN KEY(ejercicio_id) REFERENCES ejercicios(id),
            FOREIGN KEY(variante_id) REFERENCES ejercicios(id),
            PRIMARY KEY (ejercicio_id, variante_id)
        )
    ''')

    conexion.commit()
    conexion.close()
    print("Estructura de tablas creada perfectamente.")

if __name__ == '__main__':
    crear_tablas()