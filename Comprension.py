from psychopy import visual, core, event, gui, data
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os

class ComprensionWISC:
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
        self.question_text = visual.TextStim(self.win, color='blue', height=28, wrapWidth=1100)
        self.response_box = visual.Rect(self.win, width=800, height=100, fillColor='lightgray')
        self.response_display = visual.TextStim(self.win, color='black', height=24, wrapWidth=780)
        
        # Variables de la prueba
        self.edad = None
        self.nombre = ""
        self.puntaje_total = 0
        self.puntajes_consecutivos_cero = 0
        self.item_inicio = None
        self.criterio_suspension = False
        self.resultados = {}
        
        # Base de datos de preguntas y criterios de puntuación
        self.items = {
            1: {
                "pregunta": "¿Por qué es importante lavarse los dientes?",
                "conceptos": 1,
                "aprendizaje": True,
                "retroalimentacion": "Es importante lavarse los dientes para mantenerlos limpios y prevenir las caries.",
                "2_puntos": ["prevenir caries", "evitar enfermedades", "mantener limpios", "matar gérmenes", "dientes sanos", "higiene"],
                "1_punto": ["blancos", "sonrisa bonita", "bueno para los dientes", "aliento fresco", "evitar dentista"]
            },
            2: {
                "pregunta": "¿Por qué debe usarse el cinturón de seguridad cuando se viaja en auto?",
                "conceptos": 1,
                "aprendizaje": True,
                "retroalimentacion": "Debe usarse el cinturón de seguridad cuando se viaja en auto para prevenir que las personas se dañen en un accidente.",
                "2_puntos": ["prevenir daños accidente", "sujetar en accidente", "proteger en choque", "salvar vida", "evitar salir volando"],
                "1_punto": ["seguridad", "protección", "evitar daños", "sujetar", "ley"]
            },
            3: {
                "pregunta": "¿Qué deberías hacer si encuentras la billetera o la cartera de alguien en una tienda?",
                "conceptos": 1,
                "aprendizaje": True,
                "retroalimentacion": "Si encuentras la billetera o la cartera de alguien en una tienda, deberías intentar devolvérsela a su dueño. Podrías dársela a alguien que trabaje en la tienda o podrías encontrar al dueño y entregársela.",
                "2_puntos": ["buscar identificación", "devolver dueño", "cosas perdidas", "policía", "encontrar dueño"],
                "1_punto": ["documentos", "policía", "encontrar dueño", "devolver", "anuncio"]
            },
            4: {
                "pregunta": "¿Qué deberías hacer si ves que sale humo de la casa de tu vecino?",
                "conceptos": 2,
                "aprendizaje": True,
                "pregunta_segundo_concepto": "Dime qué otra cosa que deberías hacer si ves que sale humo de la casa de tu vecino.",
                "2_puntos": ["llamar bomberos", "avisar adultos", "emergencias", "ayudar", "verificar seguridad", "evacuar"],
                "1_punto": ["bomberos", "policía", "adultos", "ayuda", "ver"]
            },
            5: {
                "pregunta": "¿Por qué hay que lavar la ropa?",
                "conceptos": 1,
                "2_puntos": ["limpieza", "higiene", "gérmenes", "salud", "limpia"],
                "1_punto": ["mal olor", "suciedad", "presentable"]
            },
            6: {
                "pregunta": "Dime algunas razones por las que deberías apagar las luces cuando nadie más las está usando",
                "conceptos": 2,
                "pregunta_segundo_concepto": "Dime otra razón por la que deberías apagar las luces cuando nadie más las está usando.",
                "2_puntos": ["ahorrar energía", "conservar electricidad", "ahorrar dinero", "cuenta luz", "medio ambiente"],
                "1_punto": ["energía", "electricidad", "dinero", "contaminación"]
            },
            7: {
                "pregunta": "¿Por qué es necesario que los alimentos envasados indiquen la fecha de vencimiento?",
                "conceptos": 1,
                "2_puntos": ["enfermedades", "hacer daño", "salud", "riesgo"],
                "1_punto": ["enfermar", "estómago", "evitar enfermarse"]
            },
            8: {
                "pregunta": "¿Por qué se deben cumplir los compromisos que uno tiene con otras personas?",
                "conceptos": 1,
                "2_puntos": ["confiable", "responsable", "consideración", "formalidad", "palabra"],
                "1_punto": ["amigos", "educado", "oportunidades", "compromiso"]
            },
            9: {
                "pregunta": "¿Qué significa el refrán 'los profesores pueden abrir las puertas, pero solo tú puedes entrar'?",
                "conceptos": 1,
                "2_puntos": ["responsabilidad aprendizaje", "oportunidades tomar", "esfuerzo", "trabajar", "estudiar"],
                "1_punto": ["forzar aprender", "trabajar mucho", "tareas", "profesores no todo"]
            },
            10: {
                "pregunta": "¿Qué harías si un niño mucho más chico que tú empieza a pelear contigo?",
                "conceptos": 1,
                "2_puntos": ["hacer paces", "detener sin pegar", "convencer", "calmar", "tranquilizar"],
                "1_punto": ["evitar pelea", "no pegar", "alejarse", "controlar", "decir no"]
            },
            11: {
                "pregunta": "¿Por qué es malo presumir de los propios logros frente a otros?",
                "conceptos": 1,
                "2_puntos": ["mejor que otros", "sentir mal", "egoísta", "ofender", "maleducado"],
                "1_punto": ["no gusta", "mala educación", "atención", "ofender", "no amigos"]
            },
            12: {
                "pregunta": "¿Por qué no se debe copiar en las pruebas?",
                "conceptos": 1,
                "2_puntos": ["no justo", "no aprender", "reprobar", "consecuencia académica"],
                "1_punto": ["injusto", "mala nota", "deshonesto", "no aprender", "profesor saber"]
            },
            13: {
                "pregunta": "¿Por qué es bueno que en las elecciones el voto sea secreto?",
                "conceptos": 1,
                "2_puntos": ["presiones", "obligar votar", "represalias", "juzgar", "discriminar"],
                "1_punto": ["votar como quiera", "secreto", "conflictos", "opinión personal"]
            },
            14: {
                "pregunta": "¿Por qué es más caro un terreno en la ciudad que en el campo?",
                "conceptos": 1,
                "2_puntos": ["oferta demanda", "menos terrenos ciudad", "más personas", "espacio limitado"],
                "1_punto": ["demanda ciudad", "terrenos escasos", "difícil obtener", "más personas", "conveniencia"]
            },
            15: {
                "pregunta": "¿Por qué es importante que una sociedad no discrimine a las personas diferentes?",
                "conceptos": 1,
                "2_puntos": ["respeto igual", "derechos iguales", "ley igualdad"],
                "1_punto": ["todos iguales", "seres humanos", "personas iguales"]
            },
            16: {
                "pregunta": "¿Por qué son necesarias las leyes?",
                "conceptos": 1,
                "2_puntos": ["evitar caos", "sociedad organizada", "normas conducta", "funcionar sociedad"],
                "1_punto": ["reglas", "orden", "bien común", "respeto", "indicar hacer"]
            },
            17: {
                "pregunta": "¿Qué significa el refrán 'es mejor prender una vela que quejarse por la oscuridad'?",
                "conceptos": 1,
                "2_puntos": ["soluciones problema", "buscar soluciones", "acción que quejas"],
                "1_punto": ["no quejarse", "buscar soluciones", "hacer algo"]
            },
            18: {
                "pregunta": "¿Por qué es importante la libertad de expresión en una democracia?",
                "conceptos": 1,
                "2_puntos": ["diversas opiniones", "sin censura", "todos escuchados", "diferencias ideas"],
                "1_punto": ["ideas diferentes", "derecho opinar", "mejores ideas"]
            },
            19: {
                "pregunta": "¿Qué significa el refrán 'más vale pájaro en mano que cien volando'?",
                "conceptos": 1,
                "2_puntos": ["seguro que inseguro", "certeza incertidumbre", "concreto que ideas"],
                "1_punto": ["cosa segura", "optar seguro", "conformarse"]
            },
            20: {
                "pregunta": "¿Qué significa la expresión 'el que a buen árbol se arrima, buena sombra le cobija'?",
                "conceptos": 1,
                "2_puntos": ["buen mentor", "personas influyentes", "protegido", "éxito", "crecer"],
                "1_punto": ["personas poderosas", "proteger", "buenas personas", "amigos"]
            }
        }
        
    def obtener_datos_participante(self):
        """Obtener información del participante"""
        info_dialog = gui.Dlg(title="Comprensión - WISC")
        info_dialog.addField('Edad del participante:', 8)
        info_dialog.addField('Nombre:', 'Participante')
        info_dialog.addField('¿Sospecha de discapacidad intelectual?', choices=['No', 'Sí'])
        info_dialog.show()
        
        if info_dialog.OK:
            self.edad = int(info_dialog.data[0])
            self.nombre = info_dialog.data[1]
            discapacidad_sospecha = info_dialog.data[2] == 'Sí'
            
            # Determinar punto de inicio según edad y sospecha
            if discapacidad_sospecha or self.edad <= 11:
                self.item_inicio = 1
            else:
                self.item_inicio = 3
                
            return True
        return False
    
    def mostrar_instrucciones(self, texto):
        """Mostrar instrucciones en pantalla"""
        self.instruction.text = texto
        self.instruction.draw()
        self.win.flip()
        event.waitKeys(keyList=['space'])
    
    def evaluar_respuesta(self, item_num, respuesta):
        """Evaluar la respuesta del participante"""
        item = self.items[item_num]
        respuesta_limpia = respuesta.lower().strip()
        puntaje = 0
        
        # Verificar respuestas de 2 puntos
        for keyword in item["2_puntos"]:
            if keyword in respuesta_limpia:
                if item["conceptos"] == 1:
                    return 2
                else:
                    # Para items de 2 conceptos, necesitamos verificar múltiples conceptos
                    conceptos_encontrados = 1
                    # Buscar otro concepto diferente
                    for otro_keyword in item["2_puntos"]:
                        if otro_keyword != keyword and otro_keyword in respuesta_limpia:
                            conceptos_encontrados += 1
                            break
                    
                    if conceptos_encontrados >= 2:
                        return 2
                    else:
                        puntaje = 1  # Al menos un concepto encontrado
        
        # Verificar respuestas de 1 punto
        for keyword in item["1_punto"]:
            if keyword in respuesta_limpia:
                puntaje = max(puntaje, 1)
        
        return puntaje
    
    def capturar_respuesta_verbal(self, item_num):
        """Capturar respuesta verbal del evaluado"""
        self.question_text.text = f"Ítem {item_num}: {self.items[item_num]['pregunta']}"
        self.question_text.pos = (0, 200)
        self.question_text.draw()
        
        self.message.text = "Escribe tu respuesta y presiona ENTER:"
        self.message.pos = (0, 100)
        self.message.draw()
        
        self.response_box.draw()
        
        self.win.flip()
        
        # Capturar texto
        respuesta = ""
        while True:
            self.response_display.text = respuesta
            self.response_display.pos = (0, -50)
            
            # Redibujar todo
            self.question_text.draw()
            self.message.draw()
            self.response_box.draw()
            self.response_display.draw()
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
    
    def administrar_item(self, item_num):
        """Administrar un ítem individual"""
        item = self.items[item_num]
        respuesta_final = ""
        puntaje_final = 0
        
        # Mostrar pregunta y capturar respuesta inicial
        respuesta = self.capturar_respuesta_verbal(item_num)
        if not respuesta:
            respuesta = "sin respuesta"
        
        # Evaluar respuesta inicial
        puntaje = self.evaluar_respuesta(item_num, respuesta)
        
        # Para items de 2 conceptos, pedir segundo concepto si es necesario
        if item["conceptos"] == 2 and puntaje < 2 and "pregunta_segundo_concepto" in item:
            # Mostrar instrucción para segundo concepto
            self.mostrar_instrucciones(f"{item['pregunta_segundo_concepto']}\n\nPresiona ESPACIO para responder.")
            
            # Capturar segunda respuesta
            segunda_respuesta = self.capturar_respuesta_verbal(item_num)
            if segunda_respuesta and segunda_respuesta != "sin respuesta":
                # Combinar respuestas para evaluación
                respuesta_combinada = respuesta + " " + segunda_respuesta
                puntaje_combinado = self.evaluar_respuesta(item_num, respuesta_combinada)
                
                if puntaje_combinado > puntaje:
                    respuesta = respuesta_combinada
                    puntaje = puntaje_combinado
        
        # Proceso de aclaración si la respuesta es vaga
        if puntaje == 0 and len(respuesta) > 5:  # Si hay respuesta pero no obtiene puntos
            self.mostrar_instrucciones("¿A qué te refieres? Dime más sobre eso.\n\nPresiona ESPACIO para responder nuevamente.")
            respuesta_aclaracion = self.capturar_respuesta_verbal(item_num)
            if respuesta_aclaracion and respuesta_aclaracion != "sin respuesta":
                respuesta = respuesta_aclaracion
                puntaje = self.evaluar_respuesta(item_num, respuesta)
        
        # Retroalimentación para items de aprendizaje
        if puntaje < 2 and "aprendizaje" in item and item["aprendizaje"]:
            self.mostrar_instrucciones(f"Retroalimentación: {item['retroalimentacion']}")
        
        # Guardar resultados
        self.resultados[item_num] = {
            'respuesta': respuesta,
            'puntaje': puntaje,
            'pregunta': item['pregunta'],
            'conceptos': item['conceptos']
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
    
    def ejecutar_secuencia_inversa(self, item_actual):
        """Ejecutar secuencia inversa si es necesario"""
        if self.edad >= 12 and item_actual in [3, 4]:
            # Verificar si necesita secuencia inversa
            primeros_dos_items = list(self.resultados.keys())[-2:]
            if len(primeros_dos_items) == 2:
                puntajes_primeros = [self.resultados[item]['puntaje'] for item in primeros_dos_items]
                if not all(puntaje == 2 for puntaje in puntajes_primeros):
                    # Ejecutar secuencia inversa
                    item_reversa = item_actual - 1
                    while item_reversa >= 1:
                        if self.criterio_suspension:
                            break
                        
                        self.administrar_item(item_reversa)
                        
                        # Verificar dos consecutivos perfectos
                        ultimos_items = list(self.resultados.keys())[-2:]
                        if len(ultimos_items) == 2:
                            ultimos_puntajes = [self.resultados[item]['puntaje'] for item in ultimos_items]
                            if all(puntaje == 2 for puntaje in ultimos_puntajes):
                                break
                        
                        item_reversa -= 1
    
    def ejecutar_prueba(self):
        """Ejecutar la prueba completa"""
        # Pantalla de inicio
        self.mostrar_instrucciones(
            "PRUEBA DE COMPRENSIÓN - WISC\n\n"
            "Instrucciones:\n"
            "• Voy a hacerte preguntas sobre situaciones de la vida\n"
            "• Responde lo mejor que puedas, explicando tu razonamiento\n"
            "• Si no entiendes una pregunta, puedo repetirla\n"
            "• Trabajaremos hasta completar la prueba\n\n"
            "Presiona ESPACIO para comenzar"
        )
        
        # Administrar items según secuencia
        item_actual = self.item_inicio
        
        while item_actual <= 20 and not self.criterio_suspension:
            self.administrar_item(item_actual)
            
            # Ejecutar secuencia inversa si es necesario
            if item_actual == self.item_inicio + 1:
                self.ejecutar_secuencia_inversa(item_actual)
            
            item_actual += 1
        
        # Calcular puntaje total
        self.puntaje_total = sum(resp['puntaje'] for resp in self.resultados.values())
        
        # Mostrar resultados
        self.mostrar_resultados()
    
    def mostrar_resultados(self):
        """Mostrar gráfico con los resultados"""
        # Crear figura
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
        
        # Gráfico 1: Puntaje por ítem
        items = list(self.resultados.keys())
        puntajes = [self.resultados[item]['puntaje'] for item in items]
        
        colors = []
        for p in puntajes:
            if p == 0:
                colors.append('red')
            elif p == 1:
                colors.append('yellow')
            else:
                colors.append('green')
        
        bars = ax1.bar(range(len(items)), puntajes, color=colors, alpha=0.7)
        ax1.set_title('Puntaje por Ítem')
        ax1.set_xlabel('Ítem')
        ax1.set_ylabel('Puntaje (0-2)')
        ax1.set_xticks(range(len(items)))
        ax1.set_xticklabels(items)
        ax1.set_ylim(0, 2.5)
        
        # Agregar valores en las barras
        for i, v in enumerate(puntajes):
            ax1.text(i, v + 0.1, str(v), ha='center', va='bottom')
        
        # Gráfico 2: Distribución de puntajes
        distribucion = [puntajes.count(0), puntajes.count(1), puntajes.count(2)]
        labels = ['0 puntos', '1 punto', '2 puntos']
        colors_dist = ['red', 'yellow', 'green']
        
        ax2.pie(distribucion, labels=labels, colors=colors_dist, autopct='%1.1f%%', startangle=90)
        ax2.set_title('Distribución de Puntajes')
        
        # Gráfico 3: Resumen general
        categorias = ['Puntaje Total', 'Ítems Correctos (1-2 pts)', 'Ítems Perfectos (2 pts)', 'Ítems Administrados']
        correctos = len([p for p in puntajes if p > 0])
        perfectos = len([p for p in puntajes if p == 2])
        total_items = len(items)
        valores = [self.puntaje_total, correctos, perfectos, total_items]
        maximos = [40, total_items, total_items, 20]
        
        bars_resumen = ax3.bar(categorias, valores, color=['blue', 'orange', 'green', 'gray'], alpha=0.7)
        ax3.set_title('Resumen de Resultados')
        ax3.set_ylabel('Cantidad')
        
        # Rotar etiquetas del eje x
        ax3.set_xticklabels(categorias, rotation=45, ha='right')
        
        # Agregar valores y máximos
        for i, (v, m) in enumerate(zip(valores, maximos)):
            ax3.text(i, v + 0.5, f'{v}/{m}', ha='center', va='bottom')
            if i == 0:  # Solo para puntaje total
                ax3.axhline(y=m, color='red', linestyle='--', alpha=0.5, label='Máximo (40)')
        
        ax3.legend()
        
        plt.suptitle(f'PRUEBA DE COMPRENSIÓN - WISC\n'
                    f'Edad: {self.edad} años | Puntaje: {self.puntaje_total}/40', 
                    fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        # Guardar resultados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"comprension_{self.nombre}_{timestamp}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        
        # Mostrar resumen detallado
        self.mostrar_resumen_detallado(filename)
    
    def mostrar_resumen_detallado(self, filename):
        """Mostrar resumen detallado de los resultados"""
        resumen_texto = f"""
        RESULTADOS FINALES - COMPRENSIÓN
        
        Participante: {self.nombre}
        Edad: {self.edad} años
        Ítem de inicio: {self.item_inicio}
        Criterio de suspensión: {'Sí' if self.criterio_suspension else 'No'}
        
        PUNTAJE TOTAL: {self.puntaje_total}/40
        
        Detalle por ítem:
        """
        
        # Agregar detalles de cada ítem
        for item_num in sorted(self.resultados.keys()):
            resp = self.resultados[item_num]
            resumen_texto += f"\n\nÍtem {item_num} ({resp['conceptos']} concepto(s)): {resp['puntaje']} punto(s)"
            resumen_texto += f"\n   Pregunta: {resp['pregunta']}"
            resumen_texto += f"\n   Respuesta: {resp['respuesta'][:80]}..."
            if len(resp['respuesta']) > 80:
                resumen_texto += f" (continúa)"
        
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
    prueba = ComprensionWISC()
    if prueba.obtener_datos_participante():
        prueba.ejecutar_prueba()
