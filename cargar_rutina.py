import sqlite3

def cargar_datos():
    conexion = sqlite3.connect('gimnasio.db')
    cursor = conexion.cursor()

    ejercicios = [
        ('Sentadillas hack', 'Cuadriceps'), ('Prensa', 'Cuadriceps'),
        ('Sillón de cuádriceps', 'Cuadriceps'), ('Bulgaras', 'Cuadriceps'),
        ('Gemelos', 'Gemelos'), ('Jalón al pecho en polea', 'Espalda'),
        ('Remo T', 'Espalda'), ('Pull over con soga/trenza', 'Espalda'),
        ('Remo con barra en smith', 'Espalda'), ('Remo bajo', 'Espalda'),
        ('Polea con barra', 'Biceps'), ('Press inclinado en smith', 'Pecho'),
        ('Press con mancuerna inclinado', 'Pecho'), ('Apertura banco plano', 'Pecho'),
        ('Vuelos laterales mancuernas', 'Hombro'), ('Maquina de hombros', 'Hombro'),
        ('Polea con barra triceps', 'Triceps'), ('Abdominales', 'Core'),
        ('Peso muerto rumano', 'Femorales'), ('Camilla de femorales', 'Femorales'),
        ('Sillón de femoral', 'Femorales'), ('Hip thrust', 'Gluteos'),
        ('Maquina de abductores', 'Gluteos'), ('Vuelos laterales parado', 'Hombro'),
        ('Vuelos laterales en polea', 'Hombro'), ('Vuelos posteriores con mancuerna', 'Hombro posterior'),
        ('Press militar en smith sentado', 'Hombro'), ('Barra w parado', 'Biceps'),
        ('Soga transnuca', 'Triceps'), ('Curl con rotación sentado', 'Biceps'),
        ('Triceps en polea con manija', 'Triceps'),
        ('Pec deck', 'Pecho'),
        ('Remo con mancuernas', 'Espalda'),
        ('Remo con barra libre', 'Espalda'),
        ('Press militar con mancuernas', 'Hombro'),
        ('Pec deck invertido', 'Hombro posterior'),
        ('Fondos en paralelas', 'Pecho')
    ]
    cursor.executemany('INSERT INTO ejercicios (nombre, grupo_muscular) VALUES (?, ?)', ejercicios)

    rutina = [
        ('Lunes', 1, 5, '8', '2 series de aproximacion: 20 y 15 reps', 1, 1),
        ('Lunes', 2, 4, '10', 'Pies juntos lo mas abajo posible', 0, 2),
        ('Lunes', 3, 4, '12', '', 0, 3),
        ('Lunes', 4, 3, '8', '', 0, 4),
        ('Lunes', 5, 4, '15', '', 0, 5),
        ('Martes', 6, 4, '6 a 8', '2 series de aproximacion: 20 y 12 reps', 1, 1),
        ('Martes', 7, 4, '8 a 10', 'Agarre neutro', 0, 2),
        ('Martes', 8, 3, '15', '', 0, 3),
        ('Martes', 9, 4, '12', '', 0, 4),
        ('Martes', 10, 3, '15', 'Con triangulo', 0, 5),
        ('Martes', 11, 4, '12', '', 0, 6),
        ('Miercoles', 12, 4, '6 a 8', '2 series de aproximacion: 20 y 12 reps', 1, 1),
        ('Miercoles', 13, 4, '8 a 10', '', 0, 2),
        ('Miercoles', 14, 4, '12 a 15', '', 0, 3),
        ('Miercoles', 37, 3, '10 a 12', 'Enfoque en pecho, inclinar cuerpo', 0, 4),
        ('Miercoles', 15, 4, '12 a 15', '', 0, 5),
        ('Miercoles', 16, 3, '15', '', 0, 6),
        ('Miercoles', 17, 4, '12', '', 0, 7),
        ('Miercoles', 18, 4, '25', '', 0, 8),
        ('Jueves', 19, 4, '8', '2 series de aproximacion: 20 y 12 reps', 1, 1),
        ('Jueves', 20, 4, '12', '', 0, 2),
        ('Jueves', 21, 4, '15', '', 0, 3),
        ('Jueves', 22, 4, '8 a 10', '', 0, 4),
        ('Jueves', 23, 4, '15', 'Abrir piernas', 0, 5),
        ('Jueves', 5, 4, '15', '', 0, 6),
        ('Viernes', 24, 4, '12 a 15', '2 series de aprox: 20 y 12 reps. No mucho peso', 1, 1),
        ('Viernes', 25, 4, '15', '', 0, 2),
        ('Viernes', 26, 4, '12', '', 0, 3),
        ('Viernes', 27, 3, '6 a 8', '', 0, 4),
        ('Viernes', 28, 4, '15', 'Biserie con soga transnuca', 0, 5),
        ('Viernes', 29, 4, '15', 'Biserie con barra w parado', 0, 6),
        ('Viernes', 30, 3, '10 a 12', 'Biserie con polea con manija', 0, 7),
        ('Viernes', 31, 3, '12', 'Biserie con curl rotacion', 0, 8)
    ]
    cursor.executemany('''
        INSERT INTO rutina_dias 
        (dia, ejercicio_id, series_objetivo, reps_rango, notas, es_calentamiento, orden) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', rutina)

    def vincular(original, variante):
        cursor.execute('SELECT id FROM ejercicios WHERE nombre = ?', (original,))
        orig_id = cursor.fetchone()[0]
        cursor.execute('SELECT id FROM ejercicios WHERE nombre = ?', (variante,))
        var_id = cursor.fetchone()[0]
        cursor.execute('INSERT INTO variantes (ejercicio_id, variante_id) VALUES (?, ?)', (orig_id, var_id))

    vincular('Remo con barra en smith', 'Remo con mancuernas')
    vincular('Remo con barra en smith', 'Remo con barra libre')
    vincular('Apertura banco plano', 'Pec deck')
    vincular('Vuelos posteriores con mancuerna', 'Pec deck invertido')
    vincular('Press militar en smith sentado', 'Press militar con mancuernas')

    conexion.commit()
    conexion.close()
    print("Datos cargados correctamente")

if __name__ == '__main__':
    cargar_datos()