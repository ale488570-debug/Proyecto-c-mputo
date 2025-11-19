from psychopy import visual, core, event, gui, data
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

# Configuración de la ventana
win = visual.Window(size=(1200, 800), color='white', units='pix')

# Datos del evaluado
info = gui.Dlg(title="Datos del Evaluado - Rompecabezas Visuales")
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
    item_inicio = 8
else:
    item_inicio = 1

# Respuestas correctas (las tres piezas correctas para cada ítem)
respuestas_correctas = {
    'E': [1, 2, 6],  # Ejemplo
    'P': [3, 4, 5],  # Práctica
    1: [2, 3, 5], 2: [2, 4, 5], 3: [2, 3, 4], 4: [1, 3, 5], 5: [1, 4, 5],
    6: [1, 2, 6], 7: [2, 4, 5], 8: [3, 5, 6], 9: [1, 2, 5], 10: [3, 4, 5],
    11: [2, 5, 6], 12: [1, 3, 6], 13: [3, 4, 6], 14: [2, 3, 5], 15: [2, 3, 4],
    16: [1, 3, 5], 17: [1, 4, 6], 18: [1, 2, 4], 19: [3, 4, 6], 20: [1, 2, 5],
    21: [2, 5, 6], 22: [1, 3, 4], 23: [2, 4, 6], 24: [3, 5, 6], 25: [2, 3, 6],
    26: [1, 4, 5], 27: [1, 4, 6], 28: [1, 2, 4], 29: [1, 3, 6]
}

# Descripciones de los rompecabezas (en lugar de imágenes reales)
descripciones_rompecabezas = {
    'E': "ROMECABEZAS EJEMPLO: Forma geométrica simple",
    'P': "ROMECABEZAS PRÁCTICA: Forma que requiere rotación mental",
    1: "Rompecabezas 1: Patrón básico",
    2: "Rompecabezas 2: Patrón básico",
    3: "Rompecabezas 3: Patrón básico",
    # ... continuar con descripciones
    29: "Rompecabezas 29: Patrón complejo final"
}

# Elementos visuales
instrucciones = visual.TextStim(win, text='', color='black', height=24, wrapWidth=1000)
rompecabezas_text = visual.TextStim(win, text='', color='blue', height=20, pos=(0, 150), wrapWidth=1100)
opciones_text = visual.TextStim(win, text='', color='black', height=18, pos=(0, 0), wrapWidth=1100)
temporizador_text = visual.TextStim(win, text='', color='red', height=22, pos=(0, -100))
continuar_text = visual.TextStim(win, text='Presione 1-6 para seleccionar piezas | ENTER para enviar | ESC para salir', 
                               color='black', height=18, pos=(0, -150))
seleccion_text = visual.TextStim(win, text='', color='green', height=20, pos=(0, -50))
pregunta_text = visual.TextStim(win, text='', color='darkblue', height=22, pos=(0, 100))

# Función para administrar ítem de ejemplo
def administrar_ejemplo():
    instrucciones.text = "ÍTEM DE EJEMPLO"
    instrucciones.draw()
    win.flip()
    core.wait(2)
    
    rompecabezas_text.text = descripciones_rompecabezas['E']
    pregunta_text.text = "Voy a escoger tres piezas que al juntarlas arman este rompecabezas:"
    opciones_text.text = "Opciones de piezas (1-6):\n1. Pieza 1  2. Pieza 2  3. Pieza 3\n4. Pieza 4  5. Pieza 5  6. Pieza 6"
    
    # Dibujar elementos
    pregunta_text.draw()
    rompecabezas_text.draw()
    opciones_text.draw()
    continuar_text.draw()
    win.flip()
    core.wait(3)
    
    # Mostrar selección del examinador
    instrucciones.text = "Después de mirar atentamente, voy a escoger estas tres piezas: 1, 2 y 6"
    instrucciones.draw()
    win.flip()
    core.wait(3)
    
    instrucciones.text = "Si las junto mentalmente, armarían este rompecabezas.\nLas piezas van una al lado de la otra, no una sobre otra."
    instrucciones.draw()
    win.flip()
    core.wait(3)

# Función para administrar ítem de práctica
def administrar_practica():
    instrucciones.text = "ÍTEM DE PRÁCTICA"
    instrucciones.draw()
    win.flip()
    core.wait(2)
    
    rompecabezas_text.text = descripciones_rompecabezas['P']
    pregunta_text.text = "¿Cuáles son las TRES piezas que arman este rompecabezas?"
    opciones_text.text = "Opciones de piezas (1-6):\n1. Pieza 1  2. Pieza 2  3. Pieza 3\n4. Pieza 4  5. Pieza 5  6. Pieza 6"
    
    # Variables para la selección
    seleccionadas = []
    timer = core.Clock()
    tiempo_limite = 30
    pregunta_realizada = False
    
    while timer.getTime() < tiempo_limite and len(seleccionadas) < 3:
        tiempo_transcurrido = timer.getTime()
        tiempo_restante = tiempo_limite - tiempo_transcurrido
        
        # Preguntar si no ha respondido después de 20 segundos
        if not seleccionadas and tiempo_transcurrido >= 20 and not pregunta_realizada:
            instrucciones.text = "¿Tienes alguna respuesta?"
            pregunta_realizada = True
        else:
            instrucciones.text = f"Seleccionadas: {len(seleccionadas)}/3 piezas"
        
        # Actualizar texto de selección
        seleccion_text.text = f"Piezas seleccionadas: {sorted(seleccionadas)}" if seleccionadas else "Piezas seleccionadas: Ninguna"
        
        # Actualizar temporizador
        temporizador_text.text = f"Tiempo: {int(tiempo_restante)}s"
        
        # Dibujar todos los elementos
        instrucciones.draw()
        pregunta_text.draw()
        rompecabezas_text.draw()
        opciones_text.draw()
        seleccion_text.draw()
        temporizador_text.draw()
        continuar_text.draw()
        win.flip()
        
        # Verificar teclas
        keys = event.getKeys(keyList=['1', '2', '3', '4', '5', '6', 'escape', 'return'])
        
        if keys:
            if keys[0] == 'escape':
                return None
            elif keys[0] == 'return' and len(seleccionadas) == 3:
                break
            elif keys[0] in ['1', '2', '3', '4', '5', '6']:
                pieza = int(keys[0])
                if pieza not in seleccionadas and len(seleccionadas) < 3:
                    seleccionadas.append(pieza)
                elif pieza in seleccionadas:
                    seleccionadas.remove(pieza)  # Deseleccionar
    
    # Si se acabó el tiempo
    if len(seleccionadas) < 3:
        instrucciones.text = "Debes escoger TRES piezas para armar el rompecabezas."
        instrucciones.draw()
        win.flip()
        core.wait(2)
        
        # Dar oportunidad de completar
        while len(seleccionadas) < 3 and timer.getTime() < tiempo_limite + 5:  # 5 segundos extra
            tiempo_restante = tiempo_limite + 5 - timer.getTime()
            temporizador_text.text = f"Tiempo extra: {int(tiempo_restante)}s"
            
            instrucciones.draw()
            pregunta_text.draw()
            rompecabezas_text.draw()
            opciones_text.draw()
            seleccion_text.draw()
            temporizador_text.draw()
            continuar_text.draw()
            win.flip()
            
            keys = event.getKeys(keyList=['1', '2', '3', '4', '5', '6', 'return'])
            if keys and keys[0] in ['1', '2', '3', '4', '5', '6']:
                pieza = int(keys[0])
                if pieza not in seleccionadas and len(seleccionadas) < 3:
                    seleccionadas.append(pieza)
                elif pieza in seleccionadas:
                    seleccionadas.remove(pieza)
            elif keys and keys[0] == 'return' and len(seleccionadas) == 3:
                break
    
    # Verificar respuesta
    seleccionadas_sorted = sorted(seleccionadas)
    correctas_sorted = sorted(respuestas_correctas['P'])
    
    if seleccionadas_sorted == correctas_sorted:
        instrucciones.text = "¡Eso es correcto! Si juntas estas tres piezas se arma este rompecabezas.\nEs necesario que rotes mentalmente algunas piezas."
    else:
        if seleccionadas_sorted == [3, 5, 6]:
            instrucciones.text = "Eso no es correcto. Las piezas deben ir una al lado de la otra y no una sobre otra."
        else:
            instrucciones.text = "Eso no es correcto. Estas tres piezas arman el rompecabezas."
        
        instrucciones.text += "\nTienes que rotar mentalmente algunas piezas."
    
    instrucciones.draw()
    win.flip()
    core.wait(4)
    
    # Independientemente del resultado, continuar
    instrucciones.text = "Intentemos algunos más."
    instrucciones.draw()
    win.flip()
    core.wait(2)
    
    return seleccionadas_sorted == correctas_sorted

# Función para administrar un ítem principal
def administrar_item(item_num):
    tiempo_limite = 30
    
    instrucciones.text = f"Ítem {item_num}"
    instrucciones.draw()
    win.flip()
    core.wait(1)
    
    rompecabezas_text.text = descripciones_rompecabezas.get(item_num, f"Rompecabezas {item_num}")
    pregunta_text.text = "¿Cuáles son las TRES piezas que arman este rompecabezas?"
    opciones_text.text = "Opciones de piezas (1-6):\n1. Pieza 1  2. Pieza 2  3. Pieza 3\n4. Pieza 4  5. Pieza 5  6. Pieza 6"
    
    # Variables para la selección
    seleccionadas = []
    timer = core.Clock()
    pregunta_realizada = False
    tiempo_respuesta = 0
    
    while timer.getTime() < tiempo_limite and len(seleccionadas) < 3:
        tiempo_transcurrido = timer.getTime()
        tiempo_restante = tiempo_limite - tiempo_transcurrido
        
        # Preguntar si no ha respondido después de 20 segundos
        if not seleccionadas and tiempo_transcurrido >= 20 and not pregunta_realizada:
            instrucciones.text = "¿Tienes alguna respuesta?"
            pregunta_realizada = True
        else:
            instrucciones.text = f"Ítem {item_num} - Seleccionadas: {len(seleccionadas)}/3"
        
        # Actualizar texto de selección
        seleccion_text.text = f"Piezas seleccionadas: {sorted(seleccionadas)}" if seleccionadas else "Piezas seleccionadas: Ninguna"
        
        # Actualizar temporizador
        temporizador_text.text = f"Tiempo: {int(tiempo_restante)}s"
        
        # Dibujar todos los elementos
        instrucciones.draw()
        pregunta_text.draw()
        rompecabezas_text.draw()
        opciones_text.draw()
        seleccion_text.draw()
        temporizador_text.draw()
        continuar_text.draw()
        win.flip()
        
        # Verificar teclas
        keys = event.getKeys(keyList=['1', '2', '3', '4', '5', '6', 'escape', 'return'])
        
        if keys:
            if keys[0] == 'escape':
                return None, 0
            elif keys[0] == 'return' and len(seleccionadas) == 3:
                tiempo_respuesta = timer.getTime()
                break
            elif keys[0] in ['1', '2', '3', '4', '5', '6']:
                pieza = int(keys[0])
                if pieza not in seleccionadas and len(seleccionadas) < 3:
                    seleccionadas.append(pieza)
                elif pieza in seleccionadas:
                    seleccionadas.remove(pieza)
    
    # Si se acabó el tiempo sin 3 selecciones
    if len(seleccionadas) < 3:
        tiempo_respuesta = tiempo_limite
        # Recordatorio para seleccionar 3 piezas
        instrucciones.text = "Debes escoger TRES piezas para armar el rompecabezas."
        instrucciones.draw()
        win.flip()
        core.wait(2)
    
    # Calificar respuesta
    seleccionadas_sorted = sorted(seleccionadas)
    correctas_sorted = sorted(respuestas_correctas.get(item_num, []))
    
    puntaje = 1 if (seleccionadas_sorted == correctas_sorted and tiempo_respuesta <= tiempo_limite) else 0
    
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
            
            # Administrar ítems anteriores en orden inverso
            for item_inverso in range(item_actual - 1, 0, -1):
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
                    
                    # Verificar si alcanzó 2 consecutivos correctos
                    ultimos_2 = [r for r in resultados if not r.get('secuencia_inversa', False)][-2:]
                    if len(ultimos_2) == 2 and all(r['puntaje'] == 1 for r in ultimos_2):
                        break
    
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
    plt.title('Puntaje por Ítem - Rompecabezas Visuales')
    plt.ylim(0, 1.2)
    plt.grid(True, alpha=0.3)
    
    # Agregar valores en las barras
    for bar, puntaje in zip(bars, puntajes):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, 
                f'{puntaje}', ha='center', va='bottom')
    
    # Gráfico 2: Progreso acumulado
    plt.subplot(2, 3, 2)
    acumulado = np.cumsum(puntajes)
    plt.plot(items_num, acumulado, 'b-o', linewidth=2, markersize=6)
    plt.xlabel('Ítems')
    plt.ylabel('Puntaje Acumulado')
    plt.title('Progreso del Puntaje Acumulado')
    plt.grid(True, alpha=0.3)
    
    # Gráfico 3: Tiempo de respuesta
    plt.subplot(2, 3, 3)
    plt.plot(items_num, tiempos, 'g-s', linewidth=2, markersize=4)
    plt.axhline(y=30, color='red', linestyle='--', alpha=0.5, label='Límite 30s')
    plt.xlabel('Ítems')
    plt.ylabel('Tiempo (segundos)')
    plt.title('Tiempo de Respuesta por Ítem')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Gráfico 4: Distribución de respuestas
    plt.subplot(2, 3, 4)
    categorias = ['Correctas', 'Incorrectas/Timeout']
    valores = [sum(puntajes), len(puntajes) - sum(puntajes)]
    colores = ['green', 'red']
    plt.pie(valores, labels=categorias, colors=colores, autopct='%1.1f%%', startangle=90)
    plt.title('Distribución de Respuestas')
    
    # Gráfico 5: Eficiencia temporal
    plt.subplot(2, 3, 5)
    items_correctos = [r for r in items_principales if r['puntaje'] == 1]
    items_incorrectos = [r for r in items_principales if r['puntaje'] == 0]
    
    tiempos_correctos = [r['tiempo'] for r in items_correctos]
    tiempos_incorrectos = [r['tiempo'] for r in items_incorrectos]
    
    if tiempos_correctos:
        plt.hist(tiempos_correctos, bins=10, alpha=0.7, color='green', label='Correctos')
    if tiempos_incorrectos:
        plt.hist(tiempos_incorrectos, bins=10, alpha=0.7, color='red', label='Incorrectos')
    
    plt.axvline(x=30, color='black', linestyle='--', label='Límite 30s')
    plt.xlabel('Tiempo (segundos)')
    plt.ylabel('Frecuencia')
    plt.title('Distribución de Tiempos por Resultado')
    plt.legend()
    
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
        plt.plot(grupos, porcentajes, 'o-', linewidth=2, markersize=8, color='purple')
        plt.xlabel('Grupos de Ítems')
        plt.ylabel('Porcentaje de Aciertos (%)')
        plt.title('Progreso por Dificultad')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.ylim(0, 100)
    
    plt.tight_layout()
    
    # Guardar gráfico
    filename = f'rompecabezas_resultados_{id_evaluado}.png'
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
    instrucciones.text = """ROMPECABEZAS VISUALES

En esta prueba, verás un rompecabezas resuelto y deberás seleccionar las TRES piezas que lo forman.

Usa las teclas 1-6 para seleccionar/deseleccionar piezas.
Presiona ENTER cuando hayas seleccionado 3 piezas.
Tienes 30 segundos por ítem.

Presiona ESPACIO para comenzar con el ejemplo."""
    instrucciones.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    
    # Ítem de ejemplo
    administrar_ejemplo()
    
    # Ítem de práctica
    practica_result = administrar_practica()
    if practica_result is None:
        return resultados
    
    # Prueba principal
    while item_actual <= 29 and ceros_consecutivos < 3:
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
        if item_actual <= 29 and ceros_consecutivos < 3:
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

Resultados - Rompecabezas Visuales:
- Ítems respondidos: {total_items}
- Puntaje total: {total_puntos}/29
- Porcentaje de aciertos: {porcentaje:.1f}%

Presiona ESPACIO para ver el gráfico de resultados."""
            instrucciones.draw()
            win.flip()
            event.waitKeys(keyList=['space'])
            
            # Mostrar gráfico
            mostrar_grafico(resultados)
            
            # Guardar datos
            df = pd.DataFrame(resultados)
            df.to_csv(f'rompecabezas_datos_{id_evaluado}.csv', index=False)
        
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
