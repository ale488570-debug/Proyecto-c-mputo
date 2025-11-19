from psychopy import visual, core, event, gui, sound, microphone
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os
import re

class SecuenciacionLetrasNumeros:
    def __init__(self):
        # Crear ventana
        self.win = visual.Window(
            size=[1200, 800],
            units='pix',
            fullscr=False,
            color='white'
        )
        
        # Estímulos visuales
        self.message = visual.TextStim(self.win, color='black', height=30)
        self.instruction = visual.TextStim(self.win, color='black', height=24, wrapWidth=1000)
        self.sequence_text = visual.TextStim(self.win, color='blue', height=40)
        
        # Variables de la prueba
        self.edad = None
        self.nombre = ""
        self.puntaje_total = 0
        self.criterio_suspension = False
        self.resultados = {}
        self.slnms = 0  # Mayor secuencia
        
        # Base de datos de secuencias
        self.secuencias = {
            # Ítems de calificación
            'calificacion_conteo': "Cuenta hasta 5",
            'calificacion_alfabeto': "Dime las letras del alfabeto",
            
            # Ejemplos y práctica
            'EA': ['A-2'],
            'PA': ['B-1'],
            
            # Ítems 1-2 (un número, una letra)
            '1': ['A-3', '1-C', 'B-2'],
            '2': ['5-E', 'C-4', '1-D'],
            
            # Ejemplos y práctica con 3 elementos
            'EB': ['3-F-2'],
            'PB': ['E-5-A', '1-D-2'],
            
            # Ítems 3-10 (secuencias progresivas)
            '3': ['A-3-2', '4-1-C', 'F-D-5'],
            '4': ['Z-U-9', '8-2-D', 'C-5-U'],
            '5': ['9-H-3', 'J-6-N', '5-E-8'],
            '6': ['1-Z-4-J', 'T-8-M-9', '5-A-2-G'],
            '7': ['U-1-G-7-X', '8-D-2-R-7', 'S-6-K-3-M'],
            '8': ['1-E-4-F-9-H', 'J-2-P-5-F-6', '7-U-6-M-3-T'],
            '9': ['S-2-K-4-U-1-G', '7-5-9-K-1-T-6', 'N-2-J-6-R-8-D'],
            '10': ['4-X-9-R-1-M-7-H', 'D-2-X-9-A-6-Z-4', '2-P-1-U-4-K-7-D']
        }
        
        # Respuestas correctas
        self.respuestas_correctas = {
            'EA': ['2-A'],
            'PA': ['1-B'],
            '1': ['3-A', '1-C', '2-B'],
            '2': ['5-E', '4-C', '1-D'],
            'EB': ['2-3-F'],
            'PB': ['5-A-E', '1-2-D'],
            '3': ['2-3-A', '1-4-C', '5-D-F'],
            '4': ['9-U-Z', '2-8-D', '5-C-U'],
            '5': ['3-9-H', '6-J-N', '5-8-E'],
            '6': ['1-4-J-Z', '8-9-M-T', '2-5-A-G'],
            '7': ['1-7-G-U-X', '2-7-8-D-R', '3-6-K-M-S'],
            '8': ['1-4-9-E-F-H', '2-5-6-F-J-P', '3-6-7-M-T-U'],
            '9': ['1-2-4-G-K-S-U', '1-5-6-7-9-K-S-T', '2-6-8-D-J-N-R'],
            '10': ['1-4-7-9-H-M-R-X', '2-4-6-9-A-D-X-Z', '1-2-4-7-D-K-P-U']
        }
        
    def obtener_datos_participante(self):
        """Obtener información del participante"""
        info_dialog = gui.Dlg(title="Secuenciación Letras-Números - WISC")
        info_dialog.addField('Edad del participante:', 8)
        info_dialog.addField('Nombre:', 'Participante')
        info_dialog.show()
        
        if info_dialog.OK:
            self.edad = int(info_dialog.data[0])
            self.nombre = info_dialog.data[1]
            return True
        return False
    
    def mostrar_instrucciones(self, texto):
        """Mostrar instrucciones en pantalla"""
        self.instruction.text = texto
        self.instruction.draw()
        self.win.flip()
        event.waitKeys(keyList=['space'])
    
    def presentar_secuencia(self, secuencia):
        """Presentar una secuencia auditiva"""
        # Mostrar indicación
        self.message.text = "Escucha atentamente la secuencia..."
        self.message.draw()
        self.win.flip()
        core.wait(1)
        
        # Presentar secuencia visualmente (como apoyo)
        self.sequence_text.text = secuencia
        self.sequence_text.draw()
        self.win.flip()
        
        # Leer la secuencia (en una implementación real, usarías audio)
        elementos = secuencia.split('-')
        for elemento in elementos:
            self.message.text = elemento
            self.message.draw()
            self.win.flip()
            core.wait(1)  # Un elemento por segundo
        
        # Limpiar pantalla
        self.win.flip()
        core.wait(0.5)
    
    def capturar_respuesta(self, item_num, intento_num):
        """Capturar respuesta del evaluado"""
        self.message.text = f"Ahora repite la secuencia ordenada:\n(Números de menor a mayor, luego letras en orden alfabético)"
        self.message.draw()
        self.win.flip()
        
        # En una implementación real, usarías reconocimiento de voz
        # Por ahora simulamos con entrada de texto
        self.message.text = "Escribe tu respuesta (ej: 1-2-A-B) y presiona ENTER:"
        self.message.draw()
        self.win.flip()
        
        respuesta = ""
        while True:
            # Mostrar cuadro de respuesta
            resp_text = visual.TextStim(self.win, text=respuesta, color='black', height=30, pos=(0, -100))
            resp_text.draw()
            self.message.draw()
            self.win.flip()
            
            keys = event.waitKeys()
            
            if keys:
                key = keys[0]
                if key == 'return':
                    break
                elif key == 'backspace':
                    respuesta = respuesta[:-1]
                elif key == 'escape':
                    return None
                elif len(key) == 1 and key.isprintable():
                    respuesta += key
        
        return respuesta.upper().strip()
    
    def evaluar_respuesta(self, item_num, intento_num, respuesta):
        """Evaluar si la respuesta es correcta"""
        clave = f"{item_num}_{intento_num}"
        secuencia_original = self.secuencias[str(item_num)][intento_num-1] if item_num not in ['EA', 'PA', 'EB', 'PB'] else self.secuencias[item_num][0]
        
        if item_num in ['EA', 'PA', '1', '2']:
            # Para ítems 1-2: número primero, luego letra
            respuesta_correcta = self.respuestas_correctas[str(item_num)][intento_num-1] if item_num not in ['EA', 'PA'] else self.respuestas_correctas[item_num][0]
            return 1 if respuesta == respuesta_correcta else 0
        else:
            # Para ítems 3-10: números ordenados ascendente, luego letras alfabéticamente
            respuesta_correcta = self.respuestas_correctas[str(item_num)][intento_num-1] if item_num not in ['EB', 'PB'] else self.respuestas_correctas[item_num][intento_num-1]
            
            # Permitir tanto "números-letras" como "letras-números"
            elementos_respuesta = respuesta.split('-')
            elementos_correctos = respuesta_correcta.split('-')
            
            # Verificar si todos los elementos están presentes y correctamente ordenados en su grupo
            numeros_respuesta = [e for e in elementos_respuesta if e.isdigit()]
            letras_respuesta = [e for e in elementos_respuesta if e.isalpha()]
            
            numeros_correctos = [e for e in elementos_correctos if e.isdigit()]
            letras_correctos = [e for e in elementos_correctos if e.isalpha()]
            
            # Verificar orden correcto dentro de cada grupo
            numeros_ordenados = numeros_respuesta == sorted(numeros_respuesta, key=int)
            letras_ordenadas = letras_respuesta == sorted(letras_respuesta)
            
            # Verificar que todos los elementos estén presentes
            elementos_presentes = (set(numeros_respuesta) == set(numeros_correctos) and 
                                 set(letras_respuesta) == set(letras_correctos))
            
            return 1 if (numeros_ordenados and letras_ordenadas and elementos_presentes) else 0
    
    def administrar_calificacion(self):
        """Administrar ítems de calificación para 6-7 años"""
        if self.edad not in [6, 7]:
            return True
        
        # Calificación de conteo
        self.mostrar_instrucciones(
            "Vamos a comenzar con algunas preguntas de calificación.\n\n"
            "Primero: Cuenta hasta 5 en voz alta.\n\n"
            "Presiona ESPACIO cuando estés listo para que el participante responda."
        )
        
        # Simular evaluación de conteo
        conteo_correcto = True  # En realidad evaluarías la respuesta
        
        if not conteo_correcto:
            self.mostrar_instrucciones("El participante no cuenta correctamente hasta 3. Prueba suspendida.")
            return False
        
        # Calificación de alfabeto
        self.mostrar_instrucciones(
            "Ahora: Dime las letras del alfabeto o abecedario.\n\n"
            "Presiona ESPACIO cuando estés listo para que el participante responda."
        )
        
        # Simular evaluación de alfabeto
        alfabeto_correcto = True  # En realidad evaluarías la respuesta
        
        if not alfabeto_correcto:
            self.mostrar_instrucciones("El participante no recita correctamente el alfabeto hasta la C. Prueba suspendida.")
            return False
        
        return True
    
    def administrar_item(self, item_num, es_practica=False):
        """Administrar un ítem completo (3 intentos)"""
        puntaje_item = 0
        resultados_intentos = []
        
        num_intentos = len(self.secuencias[str(item_num)]) if item_num not in ['EA', 'PA', 'EB', 'PB'] else 1
        
        for intento in range(1, num_intentos + 1):
            if self.criterio_suspension:
                break
            
            # Presentar secuencia
            secuencia = self.secuencias[str(item_num)][intento-1] if item_num not in ['EA', 'PA', 'EB', 'PB'] else self.secuencias[item_num][0]
            self.presentar_secuencia(secuencia)
            
            # Capturar respuesta
            respuesta = self.capturar_respuesta(item_num, intento)
            
            if respuesta is None:  # Usuario salió
                return 0
            
            # Evaluar respuesta
            puntaje_intento = self.evaluar_respuesta(item_num, intento, respuesta)
            puntaje_item += puntaje_intento
            
            # Guardar resultados del intento
            resultados_intentos.append({
                'secuencia': secuencia,
                'respuesta': respuesta,
                'puntaje': puntaje_intento
            })
            
            # Mostrar retroalimentación si es práctica o ítem de aprendizaje
            if es_practica or item_num in ['1', '2']:
                if puntaje_intento == 0:
                    respuesta_correcta = self.respuestas_correctas[str(item_num)][intento-1] if item_num not in ['EA', 'PA', 'EB', 'PB'] else self.respuestas_correctas[item_num][0]
                    self.mostrar_instrucciones(f"Recuerda: debes decir {respuesta_correcta}")
            
            # Actualizar SLNms si es correcto
            if puntaje_intento == 1:
                elementos = len(secuencia.split('-'))
                self.slnms = max(self.slnms, elementos)
        
        # Guardar resultados del ítem
        self.resultados[item_num] = {
            'puntaje_total': puntaje_item,
            'intentos': resultados_intentos,
            'max_intentos': num_intentos
        }
        
        # Verificar criterio de suspensión
        if not es_practica and puntaje_item == 0:
            if self.edad in [6, 7]:
                self.criterio_suspension = True
            else:
                # Para 8-16 años, suspender después de 3 intentos con 0 en un ítem
                self.criterio_suspension = (puntaje_item == 0)
        
        return puntaje_item
    
    def ejecutar_prueba(self):
        """Ejecutar la prueba completa"""
        # Pantalla de inicio
        self.mostrar_instrucciones(
            "SECUENCIACIÓN LETRAS-NÚMEROS - WISC\n\n"
            "Instrucciones:\n"
            "• Escucharás secuencias de números y letras\n"
            "• Debes repetirlas ordenando los números de menor a mayor\n"
            "• Luego las letras en orden alfabético\n"
            "• Trabaja con atención y precisión\n\n"
            "Presiona ESPACIO para comenzar"
        )
        
        # Administrar calificación para 6-7 años
        if not self.administrar_calificacion():
            return
        
        # Ítem de ejemplo A
        self.mostrar_instrucciones(
            "Ahora voy a decir unos números y unas letras. "
            "Tienes que decirme el número primero y luego la letra.\n\n"
            "Si digo A-2, tú deberías decir 2-A.\n\n"
            "Presiona ESPACIO para el ejemplo."
        )
        self.administrar_item('EA', es_practica=True)
        
        # Ítem de práctica A
        self.mostrar_instrucciones("Ahora practiquemos...")
        self.administrar_item('PA', es_practica=True)
        
        # Ítems 1-2
        for item in ['1', '2']:
            if self.criterio_suspension:
                break
            self.administrar_item(item, es_practica=True)
        
        # Ítem de ejemplo B
        self.mostrar_instrucciones(
            "Ahora intentemos con más números y letras.\n"
            "Debes decirme primero los números ordenados de menor a mayor,\n"
            "luego las letras en orden alfabético.\n\n"
            "Si digo 3-F-2, deberías decir 2-3-F.\n\n"
            "Presiona ESPACIO para continuar."
        )
        self.administrar_item('EB', es_practica=True)
        
        # Ítem de práctica B
        self.mostrar_instrucciones("Practiquemos con más ejemplos...")
        self.administrar_item('PB', es_practica=True)
        
        # Ítems 3-10
        for item in range(3, 11):
            if self.criterio_suspension:
                break
            self.administrar_item(str(item))
        
        # Calcular puntaje total
        self.puntaje_total = sum(resultado['puntaje_total'] for resultado in self.resultados.values())
        
        # Mostrar resultados
        self.mostrar_resultados()
    
    def mostrar_resultados(self):
        """Mostrar gráfico con los resultados"""
        # Crear figura
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
        
        # Gráfico 1: Puntaje por ítem
        items = [k for k in self.resultados.keys() if k not in ['EA', 'PA', 'EB', 'PB']]
        puntajes = [self.resultados[item]['puntaje_total'] for item in items]
        max_puntajes = [self.resultados[item]['max_intentos'] for item in items]
        
        x = range(len(items))
        ax1.bar(x, puntajes, color=['red' if p == 0 else 'green' for p in puntajes], alpha=0.7, label='Puntaje obtenido')
        ax1.bar(x, max_puntajes, color='gray', alpha=0.3, label='Máximo posible')
        ax1.set_title('Puntaje por Ítem')
        ax1.set_xlabel('Ítem')
        ax1.set_ylabel('Puntaje')
        ax1.set_xticks(x)
        ax1.set_xticklabels(items)
        ax1.legend()
        
        # Agregar valores en las barras
        for i, (v, m) in enumerate(zip(puntajes, max_puntajes)):
            ax1.text(i, v + 0.1, f'{v}/{m}', ha='center', va='bottom')
        
        # Gráfico 2: Puntajes de proceso
        categorias = ['Puntaje Total', 'Mayor Secuencia (SLNms)']
        valores = [self.puntaje_total, self.slnms]
        maximos = [30, 8]
        
        ax2.bar(categorias, valores, color=['blue', 'orange'], alpha=0.7)
        ax2.set_title('Puntajes de Proceso')
        ax2.set_ylabel('Puntaje')
        
        # Agregar valores y máximos
        for i, (v, m) in enumerate(zip(valores, maximos)):
            ax2.text(i, v + 0.1, f'{v}/{m}', ha='center', va='bottom')
            ax2.axhline(y=m, color='red', linestyle='--', alpha=0.5)
        
        # Gráfico 3: Distribución de aciertos por longitud de secuencia
        longitudes = {}
        for item, datos in self.resultados.items():
            for intento in datos['intentos']:
                longitud = len(intento['secuencia'].split('-'))
                if longitud not in longitudes:
                    longitudes[longitud] = {'correctos': 0, 'totales': 0}
                longitudes[longitud]['totales'] += 1
                if intento['puntaje'] == 1:
                    longitudes[longitud]['correctos'] += 1
        
        if longitudes:
            long_ordenadas = sorted(longitudes.keys())
            porcentajes = [longitudes[l]['correctos'] / longitudes[l]['totales'] * 100 for l in long_ordenadas]
            
            ax3.bar(long_ordenadas, porcentajes, color='purple', alpha=0.7)
            ax3.set_title('Porcentaje de Acierto por Longitud')
            ax3.set_xlabel('Longitud de Secuencia')
            ax3.set_ylabel('Porcentaje de Acierto (%)')
            ax3.set_ylim(0, 100)
            
            # Agregar valores en las barras
            for i, v in enumerate(porcentajes):
                ax3.text(long_ordenadas[i], v + 2, f'{v:.0f}%', ha='center', va='bottom')
        else:
            ax3.text(0.5, 0.5, 'No hay datos\nde secuencias', 
                    ha='center', va='center', transform=ax3.transAxes, fontsize=12)
            ax3.set_title('Porcentaje de Acierto por Longitud')
        
        plt.suptitle(f'SECUENCIACIÓN LETRAS-NÚMEROS - WISC\n'
                    f'Edad: {self.edad} años | Puntaje Total: {self.puntaje_total}/30', 
                    fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        # Guardar resultados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"secuenciacion_ln_{self.nombre}_{timestamp}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        
        # Mostrar resumen detallado
        self.mostrar_resumen_detallado(filename)
    
    def mostrar_resumen_detallado(self, filename):
        """Mostrar resumen detallado de los resultados"""
        resumen_texto = f"""
        RESULTADOS FINALES - SECUENCIACIÓN LETRAS-NÚMEROS
        
        Participante: {self.nombre}
        Edad: {self.edad} años
        Criterio de suspensión: {'Sí' if self.criterio_suspension else 'No'}
        
        PUNTAJE TOTAL: {self.puntaje_total}/30
        Mayor Secuencia (SLNms): {self.slnms}/8
        
        Detalle por ítem:
        """
        
        # Agregar detalles de cada ítem
        for item in sorted(self.resultados.keys()):
            datos = self.resultados[item]
            resumen_texto += f"\n\nÍtem {item}: {datos['puntaje_total']}/{datos['max_intentos']}"
            
            for i, intento in enumerate(datos['intentos'], 1):
                estado = "✓" if intento['puntaje'] == 1 else "✗"
                resumen_texto += f"\n   Intento {i}: {estado} | Secuencia: {intento['secuencia']}"
                resumen_texto += f" | Respuesta: {intento['respuesta']}"
        
        resumen_texto += f"\n\nGráfico guardado como: {filename}"
        resumen_texto += "\n\nPresiona ESPACIO para finalizar"
        
        # Mostrar en pantallas separadas si es muy largo
        lineas = resumen_texto.split('\n')
        max_lineas_por_pantalla = 15
        
        for i in range(0, len(lineas), max_lineas_por_pantalla):
            pantalla_actual = '\n'.join(lineas[i:i + max_lineas_por_pantalla])
            self.mostrar_instrucciones(pantalla_actual)
        
        self.win.close()

# Ejecutar la prueba
if __name__ == "__main__":
    prueba = SecuenciacionLetrasNumeros()
    if prueba.obtener_datos_participante():
        prueba.ejecutar_prueba()
