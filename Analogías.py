from psychopy import visual, core, event, gui, data
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Configuración de la ventana
win = visual.Window(size=(1200, 800), color='white', units='pix')

# Datos del evaluado
info = gui.Dlg(title="Datos del Evaluado")
info.addField('Edad:', '')
info.addField('ID:', '')
info.show()

if info.OK:
    edad = int(info.data[0])
    id_evaluado = info.data[1]
else:
    core.quit()

# Determinar ítem de inicio según edad
if edad in [6, 7]:
    item_inicio = 1
elif 8 <= edad <= 11:
    item_inicio = 5
elif 12 <= edad <= 16:
    item_inicio = 8
else:
    item_inicio = 1  # Por defecto

# Base de datos de ítems
items = {
    1: {
        'pregunta': '¿En qué se parece una manzana y un plátano?',
        'respuestas_2p': ['frutas', 'frutos'],
        'respuestas_1p': ['comida', 'cosas que comes', 'comestibles', 'vienen de semillas', 
                         'tienen semillas', 'tienen cáscara', 'crecen en la naturaleza', 
                         'vienen de la naturaleza', 'nutritiva', 'saludable', 
                         'buenos para uno', 'tienen vitaminas', 'tienen minerales',
                         'postres', 'almuerzos', 'desayunos', 'dulces',
                         'se pueden hacer jugo', 'jugos', 'tienen un sabor rico',
                         'tienen un sabor dulce', 'tienen un sabor delicioso'],
        'retroalimentacion': 'La manzana y el plátano son frutas.'
    },
    2: {
        'pregunta': '¿En qué se parece una muñeca y una pelota?',
        'respuestas_2p': ['juguetes'],
        'respuestas_1p': ['juegos', 'sirven para jugar', 'para jugar', 'para divertirse',
                         'para entretenerse', 'son divertidos', 'son entretenidos'],
        'retroalimentacion': 'La muñeca y la pelota son juguetes.'
    },
    3: {
        'pregunta': '¿En qué se parece una camisa y un zapato?',
        'respuestas_2p': ['prenda', 'prenda de vestir', 'vestimenta', 'ropa', 'vestuario'],
        'respuestas_1p': ['se ponen', 'para abrigarse', 'para cubrirse', 'para protegerse',
                         'para vestir', 'para vestirse'],
        'retroalimentacion': 'La camisa y el zapato son prendas de vestir.'
    },
    # ... agregar los demás ítems de manera similar
    12: {
        'pregunta': '¿En qué se parece el codo y la rodilla?',
        'respuestas_2p': ['articulaciones', 'partes del cuerpo que se doblan',
                         'partes del cuerpo que se flexionan', 'donde se unen los huesos'],
        'respuestas_1p': ['partes del cuerpo', 'están en tu cuerpo', 'se doblan', 
                         'se flexionan', 'ayudan a moverte'],
        'retroalimentacion': 'El codo y la rodilla son articulaciones.'
    },
    18: {
        'pregunta': '¿En qué se parece el invierno y el verano?',
        'respuestas_2p': ['estaciones', 'estaciones del año', 'épocas', 'épocas del año',
                         'temporadas', 'temporadas del año'],
        'respuestas_1p': ['climas', 'tiempo', 'periodo del año con diferente clima',
                         'periodo del año con diferente temperatura', 'partes del año'],
        'retroalimentacion': 'El invierno y el verano son estaciones.'
    },
    23: {
        'pregunta': '¿En qué se parece el tiempo y el espacio?',
        'respuestas_2p': ['dimensiones', 'parte de un continuo', 'constantes',
                         'el material del universo', 'nos ayudan a definir el universo'],
        'respuestas_1p': ['cosas que nos limitan', 'son limitadas', 'se pueden acabar',
                         'inevitables', 'no se pueden controlar', 'no se pueden cambiar',
                         'se miden', 'medidas', 'infinitas', 'nunca terminan'],
        'retroalimentacion': 'El tiempo y el espacio son dimensiones.'
    }
}

# Elementos visuales
instrucciones = visual.TextStim(win, text='', color='black', height=24, wrapWidth=1000)
pregunta_text = visual.TextStim(win, text='', color='black', height=28, pos=(0, 100), wrapWidth=1100)
respuesta_input = visual.TextBox2(win, pos=(0, -50), size=(800, 100), color='black', 
                                lineColor='blue', text='', placeholder='Escriba su respuesta aquí...')
continuar_text = visual.TextStim(win, text='Presione ENTER para continuar', color='black', 
                               height=20, pos=(0, -150))
puntaje_text = visual.TextStim(win, text='', color='black', height=20, pos=(0, -100))

# Función para calcular puntaje
def calcular_puntaje(respuesta, item):
    respuesta = respuesta.lower().strip()
    
    # Verificar respuestas de 2 puntos
    for palabra in items[item]['respuestas_2p']:
        if palabra in respuesta:
            return 2
    
    # Verificar respuestas de 1 punto
    for palabra in items[item]['respuestas_1p']:
        if palabra in respuesta:
            return 1
    
    return 0

# Función para administrar ítems de práctica
def administrar_practica():
    practica_items = [
        ("¿En qué se parece el tres y el cuatro?", "números", "El tres y el cuatro son números."),
        ("¿En qué se parece la jirafa y el elefante?", "animales", "La jirafa y el elefante son animales.")
    ]
    
    for pregunta, respuesta_correcta, retro in practica_items:
        pregunta_text.text = pregunta
        respuesta_input.text = ''
        
        while True:
            pregunta_text.draw()
            respuesta_input.draw()
            continuar_text.draw()
            win.flip()
            
            keys = event.getKeys()
            if 'return' in keys and respuesta_input.text.strip():
                break
        
        respuesta = respuesta_input.text.lower()
        if respuesta_correcta in respuesta:
            instrucciones.text = f"Eso es correcto. {retro}"
        else:
            instrucciones.text = f"Eso no es correcto. {retro}"
        
        instrucciones.draw()
        win.flip()
        core.wait(3)

# Administrar prueba
def administrar_prueba():
    resultados = []
    item_actual = item_inicio
    ceros_consecutivos = 0
    
    # Ítems de práctica
    instrucciones.text = "Vamos a comenzar con algunos ejemplos de práctica."
    instrucciones.draw()
    win.flip()
    core.wait(2)
    
    administrar_practica()
    
    instrucciones.text = "Ahora comenzaremos con la prueba principal."
    instrucciones.draw()
    win.flip()
    core.wait(2)
    
    # Prueba principal
    while item_actual <= 23 and ceros_consecutivos < 3:
        pregunta_text.text = items[item_actual]['pregunta']
        respuesta_input.text = ''
        puntaje_text.text = ''
        
        while True:
            pregunta_text.draw()
            respuesta_input.draw()
            continuar_text.draw()
            puntaje_text.draw()
            win.flip()
            
            keys = event.getKeys()
            if 'return' in keys and respuesta_input.text.strip():
                break
            if 'escape' in keys:
                return resultados
        
        respuesta = respuesta_input.text
        puntaje = calcular_puntaje(respuesta, item_actual)
        
        # Mostrar retroalimentación si es ítem de aprendizaje
        if item_actual in [1, 2, 5, 6, 8, 9] and puntaje < 2:
            puntaje_text.text = items[item_actual]['retroalimentacion']
            puntaje_text.draw()
            win.flip()
            core.wait(2)
        
        resultados.append({
            'item': item_actual,
            'respuesta': respuesta,
            'puntaje': puntaje
        })
        
        # Control de suspensión
        if puntaje == 0:
            ceros_consecutivos += 1
        else:
            ceros_consecutivos = 0
        
        item_actual += 1
    
    return resultados

# Función para mostrar gráfico de resultados
def mostrar_grafico(resultados):
    items_num = [r['item'] for r in resultados]
    puntajes = [r['puntaje'] for r in resultados]
    
    plt.figure(figsize=(12, 6))
    
    # Gráfico de barras
    plt.subplot(1, 2, 1)
    colors = ['red' if p == 0 else 'yellow' if p == 1 else 'green' for p in puntajes]
    plt.bar(items_num, puntajes, color=colors, alpha=0.7)
    plt.xlabel('Ítems')
    plt.ylabel('Puntaje')
    plt.title('Puntaje por Ítem')
    plt.ylim(0, 2.5)
    plt.grid(True, alpha=0.3)
    
    # Gráfico de progreso acumulado
    plt.subplot(1, 2, 2)
    acumulado = np.cumsum(puntajes)
    plt.plot(items_num, acumulado, 'b-o', linewidth=2, markersize=6)
    plt.xlabel('Ítems')
    plt.ylabel('Puntaje Acumulado')
    plt.title('Progreso del Puntaje Acumulado')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Guardar gráfico
    plt.savefig(f'resultados_analogias_{id_evaluado}.png')
    
    # Mostrar en PsychoPy
    imagen = visual.ImageStim(win, image=f'resultados_analogias_{id_evaluado}.png')
    imagen.draw()
    win.flip()
    
    # Esperar para continuar
    event.waitKeys(keyList=['space'])
    
    # Mostrar resumen
    total_puntos = sum(puntajes)
    instrucciones.text = f"Prueba finalizada\n\nPuntaje total: {total_puntos}/46\n\nPresione ESPACIO para salir"
    instrucciones.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

# Ejecutar prueba
try:
    # Mostrar instrucciones iniciales
    instrucciones.text = """ANALOGÍAS

En esta prueba, le voy a decir dos palabras y usted debe decirme en qué se parecen.

Por ejemplo: ¿En qué se parecen un perro y un gato?
Respuesta: Son animales.

Presione ESPACIO para comenzar."""
    instrucciones.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    
    # Administrar prueba
    resultados = administrar_prueba()
    
    # Mostrar resultados
    if resultados:
        mostrar_grafico(resultados)
    
except Exception as e:
    print(f"Error: {e}")
finally:
    win.close()
    core.quit()
