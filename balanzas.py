from psychopy import visual, core, event, gui, data
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

# Configuración de la ventana
win = visual.Window(size=(1200, 800), color='white', units='pix')

# Datos del evaluado
info = gui.Dlg(title="Datos del Evaluado - Balanzas")
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
    practica_tipo = 'A'
elif 9 <= edad <= 16:
    item_inicio = 4
    practica_tipo = 'B'
else:
    item_inicio = 1
    practica_tipo = 'A'

# Respuestas correctas
respuestas_correctas = {
    'PA': 2, 'PB': 2,
    1: 3, 2: 1, 3: 4, 4: 5, 5: 3, 6: 3, 7: 4, 8: 4, 9: 1, 10: 3,
    11: 4, 12: 5, 13: 2, 14: 2, 15: 3, 16: 1, 17: 5, 18: 2, 19: 3,
    20: 4, 21: 4, 22: 2, 23: 1, 24: 5, 25: 2, 26: 1, 27: 5, 28: 3,
    29: 5, 30: 1, 31: 4, 32: 1, 33: 4, 34: 5
}

# Tiempos límite por ítem
tiempos_limite = {}
for item in range(1, 19):
    tiempos_limite[item] = 20  # 20 segundos para ítems 1-18
for item in range(19, 35):
    tiempos_limite[item] = 30  # 30 segundos para ítems 19-34

# Descripciones de los ítems (en lugar de imágenes reales)
descripciones_items = {
    'PA': "PRÁCTICA A: 1 balanza - Círculo rojo vs ¿? (Opciones: 1. Círculo azul, 2. Círculo rojo, 3. Cuadrado rojo, 4. Triángulo azul, 5. Dos círculos rojos)",
    'PB': "PRÁCTICA B: 2 balanzas - Círculo amarillo = Cuadrado amarillo; Cuadrado amarillo vs ¿? (Opciones: 1. Círculo azul, 2. Círculo amarillo, 3. Cuadrado azul, 4. Triángulo amarillo, 5. Dos círculos amarillos)",
    1: "1 balanza - Círculo azul vs ¿?",
    2: "1 balanza - Cuadrado rojo vs ¿?",
    3: "1 balanza - Triángulo amarillo vs ¿?",
    4: "2 balanzas - Patrón simple",
    5: "2 balanzas - Patrón simple",
    # ... continuar con descripciones para todos los ítems
    27: "3 BALANZAS - Patrón complejo con tres balanzas",
    34: "3 balanzas - Patrón complejo final"
}

# Elementos visuales
instrucciones = visual.TextStim(win, text='', color='black', height=24, wrapWidth=1000)
balanza_text = visual.TextStim(win, text='', color='blue', height=20, pos=(0, 150), wrapWidth=1100)
opciones_text = visual.TextStim(win, text='', color='black', height=18, pos=(0, 0), wrapWidth=1100)
temporizador_text = visual.TextStim(win, text='', color='red', height=22, pos=(0, -100))
continuar_text = visual.TextStim(win, text='Presione 1-5 para seleccionar respuesta | ESC para salir', 
                               color='black', height=18, pos=(0, -150))
pregunta_text = visual.TextStim(win, text='', color='darkblue', height=20, pos=(0, 100))

# Función para administrar ítem de práctica A
def administrar_practica_A():
    instrucciones.text = "ÍTEM DE PRÁCTICA A"
    instrucciones.draw()
    win.flip()
    core.wait(2)
    
    balanza_text.text = descripciones_items['PA']
    pregunta_text.text = "¿Cuál de estos pesa lo mismo que el círculo rojo?"
    opciones_text.text = "Opciones:\n1. Círculo azul\n2. Círculo rojo\n3. Cuadrado rojo\n4. Triángulo azul\n5. Dos círculos rojos"
    
    # Dibujar elementos
    pregunta_text.draw()
    balanza_text.draw()
    opciones_text.draw()
    continuar_text.draw()
    win.flip()
    
    # Esperar respuesta
    respuesta = None
    keys = event.waitKeys(keyList=['1', '2', '3', '4', '5', 'escape'])
    
    if keys[0] == 'escape':
        return None
    else:
        respuesta = int(keys[0])
    
    # Verificar respuesta y dar retroalimentación
    if respuesta == respuestas_correctas['PA']:
        instrucciones.text = "¡Eso es correcto! Este tiene el color correcto y la forma correcta, así que sabes que pesa lo mismo que el círculo rojo."
    else:
        if respuesta == 1:
            instrucciones.text = "Eso no es correcto. Este tiene un color distinto, por lo que no puedes saber si pesa lo mismo."
        elif respuesta == 3:
            instrucciones.text = "Eso no es correcto. Este tiene una forma distinta, por lo que no puedes saber si pesa lo mismo."
        elif respuesta == 4:
            instrucciones.text = "Eso no es correcto. Este tiene un color distinto y una forma distinta, por lo que no puedes saber si pesa lo mismo."
        elif respuesta == 5:
            instrucciones.text = "Eso no es correcto. Dos círculos rojos pesan más que uno."
        
        instrucciones.text += "\n\n¿Cuál de los otros pesa lo mismo que el círculo rojo?"
    
    instrucciones.draw()
    win.flip()
    core.wait(4)
    
    # Independientemente del resultado, continuar
    instrucciones.text = "Intentemos con otros más."
    instrucciones.draw()
    win.flip()
    core.wait(2)
    
    return respuesta

# Función para administrar ítem de práctica B
def administrar_practica_B():
    instrucciones.text = "ÍTEM DE PRÁCTICA B"
    instrucciones.draw()
    win.flip()
    core.wait(2)
    
    balanza_text.text = descripciones_items['PB']
    pregunta_text.text = "¿Cuál de estos pesa lo mismo que el cuadrado amarillo?"
    opciones_text.text = "Opciones:\n1. Círculo azul\n2. Círculo amarillo\n3. Cuadrado azul\n4. Triángulo amarillo\n5. Dos círculos amarillos"
    
    # Dibujar elementos
    pregunta_text.draw()
    balanza_text.draw()
    opciones_text.draw()
    continuar_text.draw()
    win.flip()
    
    # Esperar respuesta
    respuesta = None
    keys = event.waitKeys(keyList=['1', '2', '3', '4', '5', 'escape'])
    
    if keys[0] == 'escape':
        return None
    else:
        respuesta = int(keys[0])
    
    # Verificar respuesta y dar retroalimentación
    if respuesta == respuestas_correctas['PB']:
        instrucciones.text = "¡Eso es correcto! La primera balanza muestra que un círculo amarillo pesa lo mismo que un cuadrado amarillo."
    else:
        if respuesta == 1:
            instrucciones.text = "Eso no es correcto. Este tiene un color diferente, por lo que no puedes saber si pesa lo mismo."
        elif respuesta == 3:
            instrucciones.text = "Eso no es correcto. Este tiene un color diferente, por lo que no puedes saber si pesa lo mismo."
        elif respuesta == 4:
            instrucciones.text = "Eso no es correcto. Este tiene una forma diferente, por lo que no puedes saber si pesa lo mismo."
        elif respuesta == 5:
            instrucciones.text = "Eso no es correcto. Dos círculos amarillos pesan más que uno."
        
        instrucciones.text += "\n\n¿Cuál de estos pesa lo mismo que el cuadrado amarillo?"
    
    instrucciones.draw()
    win.flip()
    core.wait(4)
    
    # Independientemente del resultado, continuar
    instrucciones.text = "Intentemos con otros más."
    instrucciones.draw()
    win.flip()
    core.wait(2)
    
    return respuesta

# Función para administrar un ítem principal
def administrar_item(item_num):
    tiempo_limite = tiempos_limite[item_num]
    tiempo_pregunta = 10 if item_num <= 18 else 20  # Tiempo para preguntar "¿Tienes alguna respuesta?"
    
    instrucciones.text = f"Ítem {item_num}"
    instrucciones.draw()
    win.flip()
    core.wait(1)
    
    # Descripción del ítem
    balanza_text.text = descripciones_items.get(item_num, f"Balanzas - Patrón {item_num}")
    pregunta_text.text = "¿Cuál de estos pesa lo mismo que este?"
    opciones_text.text = "Opciones de respuesta:\n1. Opción 1\n2. Opción 2\n3. Opción 3\n4. Opción 4\n5. Opción 5"
    
    # Instrucción especial para ítem 27
    if item_num == 27:
        instrucciones_especial = visual.TextStim(win, 
            text="¡ATENCIÓN! Ahora tienes que mirar las TRES balanzas para saber cuál es la respuesta correcta.",
            color='red', height=22, pos=(0, -200))
    
    # Dibujar elementos iniciales
    pregunta_text.draw()
    balanza_text.draw()
    opciones_text.draw()
    continuar_text.draw()
    win.flip()
    core.wait(1)
    
    # Esperar respuesta con temporizador
    timer = core.Clock()
    respuesta = None
    tiempo_respuesta = 0
    pregunta_realizada = False
    
    while timer.getTime() < tiempo_limite:
        tiempo_transcurrido = timer.getTime()
        tiempo_restante = tiempo_limite - tiempo_transcurrido
        
        # Preguntar si no ha respondido después del tiempo establecido
        if not respuesta and tiempo_transcurrido >= tiempo_pregunta and not pregunta_realizada:
            instrucciones.text = "¿Tienes alguna respuesta?"
            pregunta_realizada = True
        else:
            instrucciones.text = f"Ítem {item_num}"
        
        # Actualizar temporizador
        temporizador_text.text = f"Tiempo: {int(tiempo_restante)}s"
        
        # Dibujar todos los elementos
        instrucciones.draw()
        pregunta_text.draw()
        balanza_text.draw()
        opciones_text.draw()
        temporizador_text.draw()
        continuar_text.draw()
        
        # Instrucción especial para ítem 27
        if item_num == 27:
            instrucciones_especial.draw()
        
        win.flip()
        
        # Verificar teclas
        keys = event.getKeys(keyList=['1', '2', '3', '4', '5', 'escape'])
        
        if keys:
            if keys[0] == 'escape':
                return None, 0
            else:
                respuesta = int(keys[0])
                tiempo_respuesta = timer.getTime()
                break
    
    # Si se acabó el tiempo
    if respuesta is None:
        tiempo_respuesta = tiempo_limite
    
    # Calificar respuesta
    puntaje = 1 if (respuesta == respuestas_correctas.get(item_num, 0) and tiempo_respuesta <= tiempo_limite) else 0
    
    return puntaje, tiempo_respuesta

# Función para secuencia inversa
def administrar_secuencia_inversa(item_actual, resultados):
    if 9 <= edad <= 16 and item_actual in [item_inicio, item_inicio + 1]:
        # Verificar si necesita secuencia inversa
        items_recientes = [r for r in resultados if r['item'] in [item_inicio, item_inicio + 1]]
        if len(items_recientes) >= 2 and any(r['puntaje'] == 0 for r in items_recientes):
            instrucciones.text = "Vamos a intentar con algunos ítems más fáciles."
            instrucciones.draw()
            win.flip()
            core.wait(2)
            
            # Administrar ítems anteriores
            for item_inverso in range(item_inicio - 1, 0, -1):
                if item_inverso >= 1:
                    puntaje, tiempo = administrar_item(item_inverso)
                    if puntaje is None:
                        return resultados
                    
                    resultados.append({
                        'item': item_inverso,
                        'puntaje': puntaje,
                        'tiempo': tiempo,
                        'correcto': puntaje == 1,
                        'secuencia_inversa': True
                    })
    
    return resultados

# Función para mostrar gráfico de resultados
def mostrar_grafico(resultados):
    if not resultados:
        return
    
    # Filtrar solo ítems principales (no de secuencia inversa)
    items_principales = [r for r in resultados if not r.get('secuencia_inversa', False)]
    
    if not items_principales:
        return
    
    items_num = [r['item'] for r in items_principales]
    puntajes = [r['puntaje'] for r in items_principales]
    tiempos = [r['tiempo'] for r in items_principales]
    
    plt.figure(figsize=(15, 10))
    
    # Gráfico 1: Puntaje por ítem
    plt.subplot(2, 3, 1)
    colors = ['red' if p == 0 else 'green' for p in puntajes]
    bars = plt.bar(items_num, puntajes, color=colors, alpha=0.7)
    plt.xlabel('Ítems')
    plt.ylabel('Puntaje (0-1)')
    plt.title('Puntaje por Ítem')
    plt.ylim(0, 1.2)
    plt.grid(True, alpha=0.3)
    
    # Línea divisoria para cambio de tiempo
    plt.axvline(x=18.5, color='black', linestyle='--', linewidth=2, label='Cambio a 30s')
    
    # Gráfico 2: Progreso acumulado
    plt.subplot(2, 3, 2)
    acumulado = np.cumsum(puntajes)
    plt.plot(items_num, acumulado, 'b-o', linewidth=2, markersize=6)
    plt.xlabel('Ítems')
    plt.ylabel('Puntaje Acumulado')
    plt.title('Progreso del Puntaje Acumulado')
    plt.grid(True, alpha=0.3)
    plt.axvline(x=18.5, color='black', linestyle='--', linewidth=2)
    
    # Gráfico 3: Tiempo de respuesta
    plt.subplot(2, 3, 3)
    plt.plot(items_num, tiempos, 'g-s', linewidth=2, markersize=4)
    plt.axhline(y=20, color='red', linestyle='--', alpha=0.5, label='Límite 20s')
    plt.axhline(y=30, color='orange', linestyle='--', alpha=0.5, label='Límite 30s')
    plt.xlabel('Ítems')
    plt.ylabel('Tiempo (segundos)')
    plt.title('Tiempo de Respuesta por Ítem')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.axvline(x=18.5, color='black', linestyle='--', linewidth=2)
    
    # Gráfico 4: Distribución de respuestas
    plt.subplot(2, 3, 4)
    categorias = ['Correctas', 'Incorrectas/Timeout']
    valores = [sum(puntajes), len(puntajes) - sum(puntajes)]
    colores = ['green', 'red']
    plt.pie(valores, labels=categorias, colors=colores, autopct='%1.1f%%', startangle=90)
    plt.title('Distribución de Respuestas')
    
    # Gráfico 5: Eficiencia por segmento
    plt.subplot(2, 3, 5)
    segmentos = ['Items 1-18', 'Items 19-34']
    items_1_18 = [r for r in items_principales if 1 <= r['item'] <= 18]
    items_19_34 = [r for r in items_principales if 19 <= r['item'] <= 34]
    
    correctos_1_18 = sum(r['puntaje'] for r in items_1_18) if items_1_18 else 0
    correctos_19_34 = sum(r['puntaje'] for r in items_19_34) if items_19_34 else 0
    
    porcentaje_1_18 = (correctos_1_18 / len(items_1_18) * 100) if items_1_18 else 0
    porcentaje_19_34 = (correctos_19_34 / len(items_19_34) * 100) if items_19_34 else 0
    
    bars = plt.bar(segmentos, [porcentaje_1_18, porcentaje_19_34], color=['lightblue', 'lightgreen'], alpha=0.7)
    plt.ylabel('Porcentaje de Aciertos (%)')
    plt.title('Eficiencia por Segmento')
    plt.ylim(0, 100)
    
    for bar, valor in zip(bars, [porcentaje_1_18, porcentaje_19_34]):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                f'{valor:.1f}%', ha='center', va='bottom')
    
    # Gráfico 6: Progreso de dificultad
    plt.subplot(2, 3, 6)
    # Calcular porcentaje de aciertos por grupos de 5 ítems
    grupos = []
    porcentajes = []
    
    for i in range(0, len(items_principales), 5):
        grupo = items_principales[i:i+5]
        if grupo:
            correctos_grupo = sum(r['puntaje'] for r in grupo)
            porcentaje_grupo = (correctos_grupo / len(grupo)) * 100
            grupos.append(f"{grupo[0]['item']}-{grupo[-1]['item']}")
            porcentajes.append(porcentaje_grupo)
    
    if grupos:
        plt.plot(grupos, porcentajes, 'o-', linewidth=2, markersize=8)
        plt.xlabel('Grupos de Ítems')
        plt.ylabel('Porcentaje de Aciertos (%)')
        plt.title('Progreso por Dificultad')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Guardar gráfico
    filename = f'balanzas_resultados_{id_evaluado}.png'
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

# Función principal
def administrar_prueba():
    resultados = []
    item_actual = item_inicio
    ceros_consecutivos = 0
    
    # Mostrar instrucciones iniciales
    instrucciones.text = """BALANZAS

En esta prueba, verás balanzas desequilibradas y deberás seleccionar qué opción las equilibra.

Usa las teclas 1-5 para seleccionar tu respuesta.
Tienes tiempo límite para cada ítem.

Presiona ESPACIO para comenzar."""
    instrucciones.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    
    # Ítem de práctica según edad
    if practica_tipo == 'A':
        practica_result = administrar_practica_A()
    else:
        practica_result = administrar_practica_B()
    
    if practica_result is None:
        return resultados
    
    # Prueba principal
    while item_actual <= 34 and ceros_consecutivos < 3:
        # Verificar secuencia inversa si es necesario
        resultados = administrar_secuencia_inversa(item_actual, resultados)
        
        # Administrar ítem actual
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
        
        item_actual += 1
        
        # Mensaje entre ítems si no se ha cumplido criterio de suspensión
        if item_actual <= 34 and ceros_consecutivos < 3:
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
        # Filtrar solo ítems principales para el resumen
        items_principales = [r for r in resultados if not r.get('secuencia_inversa', False)]
        
        if items_principales:
            total_puntos = sum(r['puntaje'] for r in items_principales)
            total_items = len(items_principales)
            porcentaje = (total_puntos / total_items) * 100 if total_items > 0 else 0
            
            instrucciones.text = f"""PRUEBA FINALIZADA

Resultados:
- Ítems respondidos: {total_items}
- Puntaje total: {total_puntos}/34
- Porcentaje de aciertos: {porcentaje:.1f}%

Presiona ESPACIO para ver el gráfico de resultados."""
            instrucciones.draw()
            win.flip()
            event.waitKeys(keyList=['space'])
            
            # Mostrar gráfico
            mostrar_grafico(resultados)
            
            # Guardar datos
            df = pd.DataFrame(resultados)
            df.to_csv(f'balanzas_datos_{id_evaluado}.csv', index=False)
        
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
