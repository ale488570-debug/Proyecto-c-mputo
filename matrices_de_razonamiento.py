from psychopy import visual, core, event, gui, data
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Configuración de la ventana
win = visual.Window(size=(1200, 800), color='white', units='pix')

# Datos del evaluado
info = gui.Dlg(title="Datos del Evaluado - Matrices de Razonamiento")
info.addField('Edad:', '')
info.addField('ID:', '')
info.show()

if info.OK:
    edad = int(info.data[0])
    id_evaluado = info.data[1]
else:
    core.quit()

# Determinar ítem de inicio según edad
if 6 <= edad <= 8:
    item_inicio = 1
elif 9 <= edad <= 11:
    item_inicio = 5
elif 12 <= edad <= 16:
    item_inicio = 9
else:
    item_inicio = 1  # Por defecto

# Respuestas correctas para los ítems
respuestas_correctas = {
    # Práctica
    'PA': 3, 'PB': 1,
    # Ítems principales
    1: 3, 2: 4, 3: 4, 4: 3, 5: 5, 6: 2, 7: 2, 8: 1, 9: 5, 10: 5,
    11: 1, 12: 2, 13: 4, 14: 1, 15: 5, 16: 2, 17: 3, 18: 2, 19: 1,
    20: 5, 21: 3, 22: 4, 23: 5, 24: 2, 25: 1, 26: 3, 27: 3, 28: 4,
    29: 3, 30: 1, 31: 5, 32: 4
}

# Descripciones de los ítems (para mostrar en lugar de imágenes reales)
descripciones_items = {
    'PA': "MATRIZ: Filas - círculo azul, círculo rojo; Columnas - círculo azul, círculo rojo",
    'PB': "SERIE: Cuadrado pequeño, cuadrado mediano, cuadrado grande",
    1: "MATRIZ: Patrón simple de formas y colores",
    2: "MATRIZ: Patrón de figuras geométricas",
    3: "MATRIZ: Secuencia de formas en matriz 2x2",
    # ... continuar con descripciones para todos los ítems
    32: "MATRIZ: Patrón complejo 3x3 con múltiples atributos"
}

# Elementos visuales
instrucciones = visual.TextStim(win, text='', color='black', height=24, wrapWidth=1000)
pregunta_text = visual.TextStim(win, text='', color='black', height=22, pos=(0, 200), wrapWidth=1100)
opciones_text = visual.TextStim(win, text='', color='black', height=20, pos=(0, 0), wrapWidth=1100)
temporizador_text = visual.TextStim(win, text='', color='red', height=18, pos=(0, -150))
continuar_text = visual.TextStim(win, text='Presione 1-5 para seleccionar respuesta | ESC para salir', 
                               color='black', height=18, pos=(0, -200))

# Función para administrar ítem de práctica A (matriz)
def administrar_practica_A():
    instrucciones.text = "ÍTEM DE PRÁCTICA A - MATRIZ"
    instrucciones.draw()
    win.flip()
    core.wait(2)
    
    pregunta_text.text = descripciones_items['PA']
    opciones_text.text = "Opciones:\n1. Círculo azul pequeño\n2. Círculo rojo pequeño\n3. Círculo rojo\n4. Círculo azul grande\n5. Cuadrado rojo"
    
    # Dibujar elementos
    pregunta_text.draw()
    opciones_text.draw()
    continuar_text.draw()
    win.flip()
    
    # Esperar respuesta
    timer = core.Clock()
    respuesta = None
    
    while timer.getTime() < 30:  # 30 segundos máximo
        keys = event.getKeys(keyList=['1', '2', '3', '4', '5', 'escape'])
        
        if keys:
            if keys[0] == 'escape':
                return None
            else:
                respuesta = int(keys[0])
                break
        
        # Actualizar temporizador
        temporizador_text.text = f"Tiempo: {30 - int(timer.getTime())}s"
        pregunta_text.draw()
        opciones_text.draw()
        temporizador_text.draw()
        continuar_text.draw()
        win.flip()
    
    # Verificar respuesta
    if respuesta == respuestas_correctas['PA']:
        instrucciones.text = "¡Eso es correcto! El círculo rojo es la única que funciona horizontal y verticalmente. No tienes que mirar en diagonal."
    else:
        instrucciones.text = "Eso no es correcto. El círculo rojo es la única que funciona horizontal y verticalmente. No tienes que mirar en diagonal."
    
    instrucciones.draw()
    win.flip()
    core.wait(3)
    
    return respuesta

# Función para administrar ítem de práctica B (serie)
def administrar_practica_B():
    instrucciones.text = "ÍTEM DE PRÁCTICA B - SERIE"
    instrucciones.draw()
    win.flip()
    core.wait(2)
    
    pregunta_text.text = descripciones_items['PB']
    opciones_text.text = "Opciones:\n1. Cuadrado grande\n2. Cuadrado pequeño\n3. Círculo grande\n4. Triángulo mediano\n5. Cuadrado mediano"
    
    # Dibujar elementos
    pregunta_text.draw()
    opciones_text.draw()
    continuar_text.draw()
    win.flip()
    
    # Esperar respuesta
    timer = core.Clock()
    respuesta = None
    
    while timer.getTime() < 30:  # 30 segundos máximo
        keys = event.getKeys(keyList=['1', '2', '3', '4', '5', 'escape'])
        
        if keys:
            if keys[0] == 'escape':
                return None
            else:
                respuesta = int(keys[0])
                break
        
        # Actualizar temporizador
        temporizador_text.text = f"Tiempo: {30 - int(timer.getTime())}s"
        pregunta_text.draw()
        opciones_text.draw()
        temporizador_text.draw()
        continuar_text.draw()
        win.flip()
    
    # Verificar respuesta
    if respuesta == respuestas_correctas['PB']:
        instrucciones.text = "¡Eso es correcto! El cuadrado grande debería ir a continuación en la secuencia."
    else:
        instrucciones.text = "Eso no es correcto. El cuadrado grande debería ir a continuación en la secuencia."
    
    instrucciones.draw()
    win.flip()
    core.wait(3)
    
    return respuesta

# Función para administrar un ítem principal
def administrar_item(item_num):
    instrucciones.text = f"Ítem {item_num}"
    instrucciones.draw()
    win.flip()
    core.wait(1)
    
    # Descripción del ítem (en lugar de imagen real)
    pregunta_text.text = f"{descripciones_items.get(item_num, 'Patrón de matriz/serie')}\n\n¿Cuál opción completa el patrón?"
    
    # Opciones genéricas (en una implementación real, aquí irían las imágenes específicas)
    opciones_text.text = "Opciones de respuesta:\n1. Opción 1\n2. Opción 2\n3. Opción 3\n4. Opción 4\n5. Opción 5"
    
    # Dibujar elementos
    pregunta_text.draw()
    opciones_text.draw()
    continuar_text.draw()
    win.flip()
    
    # Esperar respuesta
    timer = core.Clock()
    respuesta = None
    tiempo_respuesta = 0
    
    while timer.getTime() < 30:  # 30 segundos máximo
        keys = event.getKeys(keyList=['1', '2', '3', '4', '5', 'escape'])
        
        if keys:
            if keys[0] == 'escape':
                return None, 0
            else:
                respuesta = int(keys[0])
                tiempo_respuesta = timer.getTime()
                break
        
        # Actualizar temporizador
        tiempo_restante = 30 - int(timer.getTime())
        temporizador_text.text = f"Tiempo: {tiempo_restante}s"
        pregunta_text.draw()
        opciones_text.draw()
        temporizador_text.draw()
        continuar_text.draw()
        win.flip()
    
    # Si no respondió en 30 segundos
    if respuesta is None:
        instrucciones.text = "¿Tienes alguna respuesta?"
        instrucciones.draw()
        win.flip()
        
        # Dar 5 segundos adicionales
        timer_adicional = core.Clock()
        while timer_adicional.getTime() < 5:
            keys = event.getKeys(keyList=['1', '2', '3', '4', '5', 'escape'])
            if keys:
                if keys[0] == 'escape':
                    return None, 0
                else:
                    respuesta = int(keys[0])
                    tiempo_respuesta = timer.getTime() + timer_adicional.getTime()
                    break
    
    # Calificar respuesta
    puntaje = 1 if respuesta == respuestas_correctas.get(item_num, 0) else 0
    
    return puntaje, tiempo_respuesta

# Función para mostrar gráfico de resultados
def mostrar_grafico(resultados):
    if not resultados:
        return
    
    items_num = [r['item'] for r in resultados]
    puntajes = [r['puntaje'] for r in resultados]
    tiempos = [r['tiempo'] for r in resultados]
    
    plt.figure(figsize=(15, 8))
    
    # Gráfico 1: Puntaje por ítem
    plt.subplot(2, 2, 1)
    colors = ['red' if p == 0 else 'green' for p in puntajes]
    bars = plt.bar(items_num, puntajes, color=colors, alpha=0.7)
    plt.xlabel('Ítems')
    plt.ylabel('Puntaje (0-1)')
    plt.title('Puntaje por Ítem')
    plt.ylim(0, 1.2)
    plt.grid(True, alpha=0.3)
    
    # Agregar valores en las barras
    for bar, puntaje in zip(bars, puntajes):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, 
                f'{puntaje}', ha='center', va='bottom')
    
    # Gráfico 2: Progreso acumulado
    plt.subplot(2, 2, 2)
    acumulado = np.cumsum(puntajes)
    plt.plot(items_num, acumulado, 'b-o', linewidth=2, markersize=6)
    plt.xlabel('Ítems')
    plt.ylabel('Puntaje Acumulado')
    plt.title('Progreso del Puntaje Acumulado')
    plt.grid(True, alpha=0.3)
    
    # Gráfico 3: Tiempo de respuesta
    plt.subplot(2, 2, 3)
    plt.plot(items_num, tiempos, 'g-s', linewidth=2, markersize=4)
    plt.xlabel('Ítems')
    plt.ylabel('Tiempo (segundos)')
    plt.title('Tiempo de Respuesta por Ítem')
    plt.grid(True, alpha=0.3)
    
    # Gráfico 4: Resumen general
    plt.subplot(2, 2, 4)
    categorias = ['Correctas', 'Incorrectas']
    valores = [sum(puntajes), len(puntajes) - sum(puntajes)]
    colores = ['green', 'red']
    plt.pie(valores, labels=categorias, colors=colores, autopct='%1.1f%%', startangle=90)
    plt.title('Distribución de Respuestas')
    
    plt.tight_layout()
    
    # Guardar gráfico
    filename = f'matrices_resultados_{id_evaluado}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    
    # Mostrar en PsychoPy
    try:
        imagen = visual.ImageStim(win, image=filename)
        imagen.draw()
        win.flip()
        
        instrucciones.text = "Presione ESPACIO para continuar"
        instrucciones.draw()
        win.flip()
        event.waitKeys(keyList=['space'])
    except:
        print("No se pudo cargar la imagen del gráfico")

# Función principal para administrar la prueba
def administrar_prueba():
    resultados = []
    item_actual = item_inicio
    ceros_consecutivos = 0
    
    # Mostrar instrucciones iniciales
    instrucciones.text = """MATRICES DE RAZONAMIENTO

En esta prueba, verás matrices o series de figuras incompletas.
Debes seleccionar la opción que completa correctamente el patrón.

Usa las teclas 1-5 para seleccionar tu respuesta.
Tienes aproximadamente 30 segundos por ítem.

Presiona ESPACIO para comenzar con los ejemplos de práctica."""
    instrucciones.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    
    # Ítems de práctica
    practica_A = administrar_practica_A()
    if practica_A is None:
        return resultados
    
    practica_B = administrar_practica_B()
    if practica_B is None:
        return resultados
    
    # Prueba principal
    instrucciones.text = "Ahora comenzaremos con la prueba principal.\n\nPresiona ESPACIO para continuar."
    instrucciones.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    
    # Administrar ítems principales
    while item_actual <= 32 and ceros_consecutivos < 3:
        puntaje, tiempo = administrar_item(item_actual)
        
        if puntaje is None:  # Usuario presionó ESC
            break
        
        resultados.append({
            'item': item_actual,
            'puntaje': puntaje,
            'tiempo': tiempo,
            'correcto': puntaje == 1
        })
        
        # Control de suspensión
        if puntaje == 0:
            ceros_consecutivos += 1
        else:
            ceros_consecutivos = 0
        
        # Secuencia inversa para edades 9-16
        if 9 <= edad <= 16 and item_actual in [item_inicio, item_inicio + 1] and puntaje == 0:
            # Implementar secuencia inversa (simplificada)
            instrucciones.text = "Continuaremos con ítems más fáciles."
            instrucciones.draw()
            win.flip()
            core.wait(2)
        
        item_actual += 1
        
        # Mensaje entre ítems
        if item_actual <= 32 and ceros_consecutivos < 3:
            instrucciones.text = "Intentemos otro más.\n\nPresiona ESPACIO para continuar."
            instrucciones.draw()
            win.flip()
            event.waitKeys(keyList=['space'])
    
    return resultados

# Ejecutar prueba
try:
    resultados = administrar_prueba()
    
    # Mostrar resumen final
    if resultados:
        total_puntos = sum(r['puntaje'] for r in resultados)
        total_items = len(resultados)
        porcentaje = (total_puntos / total_items) * 100 if total_items > 0 else 0
        
        instrucciones.text = f"""PRUEBA FINALIZADA

Resultados:
- Ítems respondidos: {total_items}
- Puntaje total: {total_puntos}/32
- Porcentaje de aciertos: {porcentaje:.1f}%

Presiona ESPACIO para ver el gráfico de resultados."""
        instrucciones.draw()
        win.flip()
        event.waitKeys(keyList=['space'])
        
        # Mostrar gráfico
        mostrar_grafico(resultados)
        
        # Guardar datos
        df = pd.DataFrame(resultados)
        df.to_csv(f'matrices_datos_{id_evaluado}.csv', index=False)
        
    else:
        instrucciones.text = "Prueba interrumpida. No se registraron resultados."
        instrucciones.draw()
        win.flip()
        core.wait(3)
        
except Exception as e:
    print(f"Error durante la prueba: {e}")
    instrucciones.text = f"Error: {e}\n\nPresiona cualquier tecla para salir."
    instrucciones.draw()
    win.flip()
    event.waitKeys()
finally:
    win.close()
    core.quit()
