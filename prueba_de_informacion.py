from psychopy import visual, core, event, gui, data
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os

class InformacionWISC:
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
        self.question = visual.TextStim(self.win, color='black', height=28, wrapWidth=1100)
        self.response_box = visual.Rect(self.win, width=800, height=100, fillColor='lightgray')
        self.response_text = visual.TextStim(self.win, color='black', height=24, wrapWidth=780)
        
        # Variables de la prueba
        self.edad = None
        self.nombre = ""
        self.puntaje_total = 0
        self.puntajes_consecutivos_cero = 0
        self.item_inicio = None
        self.items_administrados = []
        self.respuestas = {}
        self.criterio_suspension = False
        
        # Base de datos de preguntas y respuestas
        self.items = {
            1: {
                "pregunta": "Señálame tu nariz",
                "respuestas_1_punto": ["toca nariz", "apunta nariz", "señala nariz"],
                "retroalimentacion": "Esta es tu nariz.",
                "aprendizaje": True
            },
            2: {
                "pregunta": "Señálame tu oreja", 
                "respuestas_1_punto": ["toca oreja", "apunta oreja", "señala oreja"],
                "retroalimentacion": "Esta es tu oreja.",
                "aprendizaje": True
            },
            3: {
                "pregunta": "Nombra un tipo de pájaro",
                "respuestas_1_punto": ["colibrí", "paloma", "gaviota", "codorniz", "tucán", "búho", "pájaro carpintero", 
                                      "mirlo", "cardenal", "pingüino", "avestruz", "águila", "halcón", "cóndor", 
                                      "canario", "cacatúa", "loro"],
                "pregunta_aclaracion": None
            },
            4: {
                "pregunta": "¿Qué día viene inmediatamente después del jueves?",
                "respuestas_1_punto": ["viernes"],
                "pregunta_aclaracion": "¿Cómo se llama ese día?"
            },
            5: {
                "pregunta": "Nombra algo con cuerdas que se utilice para hacer música",
                "respuestas_1_punto": ["guitarra", "violín", "arpa", "piano", "bajo", "chelo", "viola", "banjo"]
            },
            6: {
                "pregunta": "¿Qué mes viene inmediatamente después de junio?",
                "respuestas_1_punto": ["julio"],
                "pregunta_aclaracion": "Sí, pero ¿cómo se llama ese mes?"
            },
            7: {
                "pregunta": "Nombra un tipo de árbol",
                "respuestas_1_punto": ["roble", "pino", "manzano", "eucalipto", "sauce", "árbol de naranja", "peral"]
            },
            8: {
                "pregunta": "Dime alguna tecnología que haya cambiado la forma en que los humanos se comunican",
                "respuestas_1_punto": ["computador", "teléfono", "celular", "internet", "email"],
                "retroalimentacion": "Los computadores son una tecnología que ha cambiado la forma en que los humanos se comunican.",
                "aprendizaje": True
            },
            9: {
                "pregunta": "Dime el nombre de dos océanos",
                "respuestas_1_punto": ["pacífico atlántico", "índico pacífico", "atlántico índico", "ártico antártico"],
                "aprendizaje": True
            },
            10: {
                "pregunta": "¿De qué país es originaria la pizza?",
                "respuestas_1_punto": ["italia"]
            },
            11: {
                "pregunta": "¿En qué país está la Torre Eiffel?",
                "respuestas_1_punto": ["francia"]
            },
            12: {
                "pregunta": "¿Cuáles son los cuatro puntos cardinales?",
                "respuestas_1_punto": ["norte sur este oeste"],
                "pregunta_aclaracion": "Dime otro de los puntos cardinales"
            },
            13: {
                "pregunta": "¿Qué hace el corazón en nuestros cuerpos?",
                "respuestas_1_punto": ["bombea sangre", "circula sangre", "envía sangre"]
            },
            14: {
                "pregunta": "¿Cuál es la causa de los terremotos?",
                "respuestas_1_punto": ["placas tectónicas", "movimiento de placas", "fallas geológicas"],
                "pregunta_aclaracion": "¿Qué cosa de la naturaleza causa los terremotos?"
            },
            15: {
                "pregunta": "¿Quiénes fueron los Beatles?",
                "respuestas_1_punto": ["una banda", "grupo musical", "músicos ingleses"]
            },
            16: {
                "pregunta": "¿Cuál es la montaña más alta del mundo?",
                "respuestas_1_punto": ["everest", "monte everest"],
                "pregunta_aclaracion": "Sí, pero ¿cuál es la montaña más alta del mundo desde el nivel del mar?"
            },
            17: {
                "pregunta": "¿Cuántos días hay en un año?",
                "respuestas_1_punto": ["365", "365 y cuarto", "365.25"],
                "pregunta_aclaracion": "¿Cuántos días hay en la mayoría de los años?"
            },
            18: {
                "pregunta": "¿Para qué sirve un satélite?",
                "respuestas_1_punto": ["comunicaciones", "observación", "investigación espacial"]
            },
            19: {
                "pregunta": "¿En qué continente está Polonia?",
                "respuestas_1_punto": ["europa"],
                "pregunta_aclaracion": "Sí, pero ¿en qué continente está el país llamado Polonia?"
            },
            20: {
                "pregunta": "¿Qué continente tiene la mayor cantidad de personas?",
                "respuestas_1_punto": ["asia"]
            },
            21: {
                "pregunta": "¿Quién pintó la Mona Lisa?",
                "respuestas_1_punto": ["leonardo da vinci", "da vinci"]
            },
            22: {
                "pregunta": "¿Quiénes fueron los Mayas?",
                "respuestas_1_punto": ["civilización antigua", "pueblo mesoamericano", "cultura precolombina"]
            },
            23: {
                "pregunta": "¿Cuántos países hay en el mundo?",
                "respuestas_1_punto": ["195", "200", "150", "180", "190", "210"],
                "pregunta_aclaracion": "¿Pero cuántos crees que son aproximadamente?"
            },
            24: {
                "pregunta": "¿En qué lugares del mundo existen noches de 24 horas?",
                "respuestas_1_punto": ["polos", "círculo polar", "ártico", "antártida"],
                "pregunta_aclaracion": "Sí, pero, ¿en qué parte específicamente?"
            },
            25: {
                "pregunta": "¿Quién fue Stephen Hawking?",
                "respuestas_1_punto": ["científico", "físico", "cosmólogo"]
            },
            26: {
                "pregunta": "¿Quién es Quetzalcoatl?",
                "respuestas_1_punto": ["dios mesoamericano", "serpiente emplumada", "dios azteca"]
            },
            27: {
                "pregunta": "¿Cuántos kilómetros tiene América del Sur desde el extremo norte al extremo sur?",
                "respuestas_1_punto": ["7000", "7500", "8000", "7200"],
                "pregunta_aclaracion": "¿Pero cuántos crees que son aproximadamente?"
            },
            28: {
                "pregunta": "Dime alguna obra que haya hecho Miguel Ángel",
                "respuestas_1_punto": ["el david", "capilla sixtina", "la piedad", "moisés"]
            },
            29: {
                "pregunta": "¿Por qué se eleva el aire caliente?",
                "respuestas_1_punto": ["menos denso", "más ligero", "expansión térmica"]
            },
            30: {
                "pregunta": "¿Quién fue Ícaro?",
                "respuestas_1_punto": ["mitología griega", "alas de cera", "personaje mitológico"]
            }
        }
        
    def obtener_datos_participante(self):
        """Obtener información del participante"""
        info_dialog = gui.Dlg(title="Información - WISC")
        info_dialog.addField('Edad del participante:', 8)
        info_dialog.addField('Nombre:', 'Participante')
        info_dialog.addField('¿Sospecha de discapacidad intelectual?', choices=['No', 'Sí'])
        info_dialog.show()
        
        if info_dialog.OK:
            self.edad = int(info_dialog.data[0])
            self.nombre = info_dialog.data[1]
            discapacidad_sospecha = info_dialog.data[2] == 'Sí'
            
            # Determinar punto de inicio según edad y sospecha
            if discapacidad_sospecha or self.edad <= 8:
                self.item_inicio = 1
            else:
                self.item_inicio = 8
                
            return True
        return False
    
    def mostrar_instrucciones(self, texto):
        """Mostrar instrucciones en pantalla"""
        self.instruction.text = texto
        self.instruction.draw()
        self.win.flip()
        event.waitKeys(keyList=['space'])
    
    def evaluar_respuesta(self, item_num, respuesta):
        """Evaluar si la respuesta merece 1 punto"""
        item = self.items[item_num]
        respuesta_limpia = respuesta.lower().strip()
        
        # Para items que requieren múltiples elementos
        if item_num == 9:  # Dos océanos
            océanos_correctos = 0
            for oceano in ["pacífico", "atlántico", "índico", "ártico", "antártico"]:
                if oceano in respuesta_limpia:
                    océanos_correctos += 1
            return 1 if océanos_correctos >= 2 else 0
        
        if item_num == 12:  # Cuatro puntos cardinales
            puntos_correctos = 0
            for punto in ["norte", "sur", "este", "oeste"]:
                if punto in respuesta_limpia:
                    puntos_correctos += 1
            return 1 if puntos_correctos == 4 else 0
        
        # Para otros items, buscar coincidencias en respuestas correctas
        for respuesta_correcta in item["respuestas_1_punto"]:
            if respuesta_correcta in respuesta_limpia:
                return 1
        
        return 0
    
    def administrar_item(self, item_num):
        """Administrar un ítem individual"""
        item = self.items[item_num]
        respuesta_final = ""
        puntaje = 0
        
        # Mostrar pregunta
        self.question.text = f"Ítem {item_num}: {item['pregunta']}"
        self.question.draw()
        self.win.flip()
        core.wait(1)
        
        # Capturar respuesta inicial
        respuesta = self.capturar_respuesta_verbal(item_num)
        if not respuesta:
            respuesta = "sin respuesta"
        
        # Evaluar respuesta inicial
        puntaje = self.evaluar_respuesta(item_num, respuesta)
        
        # Proceso de aclaración si es necesario
        if puntaje == 0 and "pregunta_aclaracion" in item and item["pregunta_aclaracion"]:
            self.mostrar_instrucciones(f"{item['pregunta_aclaracion']}\n\nPresiona ESPACIO para responder nuevamente")
            respuesta_aclaracion = self.capturar_respuesta_verbal(item_num)
            if respuesta_aclaracion:
                respuesta = respuesta_aclaracion
                puntaje = self.evaluar_respuesta(item_num, respuesta)
        
        # Retroalimentación para items de aprendizaje
        if puntaje == 0 and "aprendizaje" in item and item["aprendizaje"]:
            self.mostrar_instrucciones(f"Retroalimentación: {item['retroalimentacion']}")
        
        # Guardar resultados
        self.respuestas[item_num] = {
            'respuesta': respuesta,
            'puntaje': puntaje,
            'pregunta': item['pregunta']
        }
        
        # Actualizar contador de ceros consecutivos
        if puntaje == 0:
            self.puntajes_consecutivos_cero += 1
        else:
            self.puntajes_consecutivos_cero = 0
        
        # Verificar criterio de suspensión
        if self.puntajes_consecutivos_cero >= 3:
            self.criterio_suspension = True
        
        return puntaje
    
    def capturar_respuesta_verbal(self, item_num):
        """Capturar respuesta verbal del evaluado"""
        self.message.text = "Escribe la respuesta y presiona ENTER:"
        self.message.pos = (0, 300)
        self.message.draw()
        
        self.response_box.draw()
        
        self.question.text = f"Ítem {item_num}: {self.items[item_num]['pregunta']}"
        self.question.pos = (0, 150)
        self.question.draw()
        
        self.win.flip()
        
        # Capturar texto
        respuesta = ""
        while True:
            self.response_text.text = respuesta
            self.response_text.pos = (0, -50)
            
            self.message.draw()
            self.response_box.draw()
            self.response_text.draw()
            self.question.draw()
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
        
        return respuesta
    
    def ejecutar_secuencia_inversa(self, item_actual):
        """Ejecutar secuencia inversa si es necesario"""
        if self.edad >= 9 and item_actual in [8, 9]:
            # Verificar si necesita secuencia inversa
            primeros_dos_items = list(self.respuestas.keys())[-2:]
            if len(primeros_dos_items) == 2:
                puntajes_primeros = [self.respuestas[item]['puntaje'] for item in primeros_dos_items]
                if not all(puntaje == 1 for puntaje in puntajes_primeros):
                    # Ejecutar secuencia inversa
                    item_reversa = item_actual - 1
                    while item_reversa >= 1:
                        if self.criterio_suspension:
                            break
                        
                        puntaje = self.administrar_item(item_reversa)
                        
                        # Verificar dos consecutivos perfectos
                        ultimos_items = list(self.respuestas.keys())[-2:]
                        if len(ultimos_items) == 2:
                            ultimos_puntajes = [self.respuestas[item]['puntaje'] for item in ultimos_items]
                            if all(puntaje == 1 for puntaje in ultimos_puntajes):
                                break
                        
                        item_reversa -= 1
    
    def ejecutar_prueba(self):
        """Ejecutar la prueba completa"""
        # Pantalla de inicio
        self.mostrar_instrucciones(
            "PRUEBA DE INFORMACIÓN - WISC\n\n"
            "Instrucciones:\n"
            "• Voy a hacerte algunas preguntas\n"
            "• Responde lo mejor que puedas\n"
            "• Si no entiendes una pregunta, puedo repetirla\n"
            "• Trabajaremos hasta completar la prueba\n\n"
            "Presiona ESPACIO para comenzar"
        )
        
        # Administrar items según secuencia
        item_actual = self.item_inicio
        
        while item_actual <= 30 and not self.criterio_suspension:
            self.administrar_item(item_actual)
            
            # Ejecutar secuencia inversa si es necesario
            if item_actual == self.item_inicio + 1:
                self.ejecutar_secuencia_inversa(item_actual)
            
            item_actual += 1
        
        # Calcular puntaje total
        self.puntaje_total = sum(resp['puntaje'] for resp in self.respuestas.values())
        
        # Mostrar resultados
        self.mostrar_resultados()
    
    def mostrar_resultados(self):
        """Mostrar gráfico con los resultados"""
        # Crear figura
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Gráfico 1: Puntaje por ítem
        items = list(self.respuestas.keys())
        puntajes = [self.respuestas[item]['puntaje'] for item in items]
        
        ax1.bar(range(len(items)), puntajes, color=['red' if p == 0 else 'green' for p in puntajes])
        ax1.set_title('Puntaje por Ítem')
        ax1.set_xlabel('Ítem')
        ax1.set_ylabel('Puntaje (0-1)')
        ax1.set_xticks(range(len(items)))
        ax1.set_xticklabels(items)
        ax1.set_ylim(0, 1)
        
        # Agregar valores en las barras
        for i, v in enumerate(puntajes):
            ax1.text(i, v + 0.05, str(v), ha='center', va='bottom')
        
        # Gráfico 2: Resumen general
        categorias = ['Puntaje Total', 'Ítems Correctos', 'Ítems Incorrectos', 'Ítems Administrados']
        correctos = sum(puntajes)
        incorrectos = len(puntajes) - correctos
        valores = [self.puntaje_total, correctos, incorrectos, len(items)]
        
        ax2.bar(categorias, valores, color=['blue', 'green', 'red', 'gray'], alpha=0.7)
        ax2.set_title('Resumen de Resultados')
        ax2.set_ylabel('Cantidad')
        
        # Rotar etiquetas del eje x
        ax2.set_xticklabels(categorias, rotation=45, ha='right')
        
        # Agregar valores en las barras
        for i, v in enumerate(valores):
            ax2.text(i, v + 0.1, str(v), ha='center', va='bottom')
        
        # Línea de máximo puntaje
        ax2.axhline(y=31, color='red', linestyle='--', alpha=0.5, label='Máximo (31)')
        ax2.legend()
        
        plt.suptitle(f'PRUEBA DE INFORMACIÓN - WISC\n'
                    f'Edad: {self.edad} años | Puntaje: {self.puntaje_total}/31', 
                    fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        # Guardar resultados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"informacion_{self.nombre}_{timestamp}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        
        # Mostrar resumen detallado
        self.mostrar_resumen_detallado(filename)
    
    def mostrar_resumen_detallado(self, filename):
        """Mostrar resumen detallado de los resultados"""
        resumen_texto = f"""
        RESULTADOS FINALES - INFORMACIÓN
        
        Participante: {self.nombre}
        Edad: {self.edad} años
        Ítem de inicio: {self.item_inicio}
        Criterio de suspensión: {'Sí' if self.criterio_suspension else 'No'}
        
        PUNTAJE TOTAL: {self.puntaje_total}/31
        
        Detalle por ítem:
        """
        
        # Agregar detalles de cada ítem
        for item_num in sorted(self.respuestas.keys()):
            resp = self.respuestas[item_num]
            resumen_texto += f"\nÍtem {item_num}: {resp['puntaje']} punto(s)"
            resumen_texto += f"\n   Pregunta: {resp['pregunta']}"
            resumen_texto += f"\n   Respuesta: {resp['respuesta'][:50]}..."
            if len(resp['respuesta']) > 50:
                resumen_texto += f" (continúa)"
        
        resumen_texto += f"\n\nGráfico guardado como: {filename}"
        resumen_texto += "\n\nPresiona ESPACIO para finalizar"
        
        # Mostrar en pantallas separadas si es muy largo
        lineas = resumen_texto.split('\n')
        max_lineas_por_pantalla = 20
        
        for i in range(0, len(lineas), max_lineas_por_pantalla):
            pantalla_actual = '\n'.join(lineas[i:i + max_lineas_por_pantalla])
            self.mostrar_instrucciones(pantalla_actual)
        
        self.win.close()

# Ejecutar la prueba
if __name__ == "__main__":
    prueba = InformacionWISC()
    if prueba.obtener_datos_participante():
        prueba.ejecutar_prueba()
