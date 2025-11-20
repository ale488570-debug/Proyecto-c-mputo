class PruebaAritmetica:
    def __init__(self):
        self.nombre = "Aritmética - WISC"
        self.descripcion = "Razonamiento aritmético y cálculo mental"
        self.categoria = "Razonamiento"
        self.duracion_estimada = "15-25 min"
        self.resultados = {}
        
        # Base de datos de ítems (versión adaptada para PsychoPy)
        self.items = {
            1: {"texto": "Cuenta estos perros con tu dedo. Hazlo en voz alta.", "respuesta": 3, "tipo": "ilustrado"},
            2: {"texto": "Cuenta estos pollitos con tu dedo. Hazlo en voz alta.", "respuesta": 5, "tipo": "ilustrado"},
            3: {"texto": "Cuenta estos árboles con tu dedo. Hazlo en voz alta.", "respuesta": 10, "tipo": "ilustrado"},
            4: {"texto": "¿Cuántas mariposas y grillos hay? Suma las mariposas y los grillos y dime cuántos hay en total.", "respuesta": 9, "tipo": "ilustrado"},
            5: {"texto": "¿Cuántas nueces quedarán si cada ardilla se come una?", "respuesta": 2, "tipo": "ilustrado"},
            6: {"texto": "Ana tiene 6 libros. Si pierde 1, ¿cuántos libros le quedan?", "respuesta": 5, "tipo": "verbal"},
            7: {"texto": "Igna tiene 5 manzanas. Si le da 1 a Marce y 1 a Sole, ¿cuántas manzanas le quedan?", "respuesta": 3, "tipo": "verbal"},
            8: {"texto": "Daniel tiene 2 juguetes. Si le regalan 3 más, ¿cuántos juguetes va a tener en total?", "respuesta": 5, "tipo": "verbal"},
            9: {"texto": "Carlos tiene 4 lápices. Su mamá le da 3 más. ¿Cuántos lápices tiene ahora en total?", "respuesta": 7, "tipo": "verbal"},
            10: {"texto": "María tiene 3 uvas en cada mano. ¿Cuántas uvas tiene en total?", "respuesta": 6, "tipo": "verbal"},
            11: {"texto": "Marcos tiene 12 amigos y hace 3 más. ¿Cuántos amigos tiene en total?", "respuesta": 15, "tipo": "verbal"},
            12: {"texto": "Ale tiene 8 muñecas y le dan 6 más. ¿Cuántas muñecas tiene en total?", "respuesta": 14, "tipo": "verbal"},
            13: {"texto": "Jorge tiene 11 globos y pierde 3. ¿Cuántos globos le quedan?", "respuesta": 8, "tipo": "verbal"},
            14: {"texto": "Luis jugó 10 partidos el lunes y 15 partidos el martes. ¿Cuántos partidos jugó en total?", "respuesta": 25, "tipo": "verbal"},
            15: {"texto": "Dentro de una laguna hay 3 ranas. Si llegan 4 ranas más que se meten a la laguna y luego 2 se salen, ¿cuántas ranas quedan en la laguna?", "respuesta": 5, "tipo": "verbal"},
            16: {"texto": "Hay 8 pájaros en la tierra. Si 4 salen volando y otros 2 aterrizan, ¿cuántos pájaros hay en la tierra ahora?", "respuesta": 6, "tipo": "verbal"},
            17: {"texto": "Tom tiene 12 boletos y su tío le da 2 más. Si vende 5, ¿cuántos le quedan?", "respuesta": 9, "tipo": "verbal"},
            18: {"texto": "Pablo tiene 100 lápices. Si le da 40 lápices a cada uno de sus 2 hermanos, ¿cuántos lápices le quedan?", "respuesta": 20, "tipo": "verbal"},
            19: {"texto": "Karen contó 17 postes de luz en una calle y 15 en otra. ¿Cuántos postes de luz contó en total?", "respuesta": 32, "tipo": "verbal"},
            20: {"texto": "Cata tiene 30 minutos de tiempo libre, pero dedica la mitad de este tiempo para limpiar su cuarto. Si 1 canción dura 5 minutos, ¿cuántas canciones alcanza a escuchar en el tiempo libre que le queda?", "respuesta": 3, "tipo": "verbal"},
            21: {"texto": "Cada niño corre 1 sola vuelta en una carrera que tiene 8 vueltas. Si tres niños corren juntos en cada vuelta, ¿cuántos niños están participando en total en la carrera?", "respuesta": 24, "tipo": "verbal"},
            22: {"texto": "Un club de fútbol tiene 30 niños. Después de una semana, 11 niños dejan el club y se unen 2 nuevos. ¿Cuántos niños hay en el club?", "respuesta": 21, "tipo": "verbal"},
            23: {"texto": "Rosa le da 2 anillos a cada una de sus 3 amigas. A su mamá le da 7 anillos. ¿Cuántos anillos le quedan si al principio tenía 20?", "respuesta": 7, "tipo": "verbal"},
            24: {"texto": "En una escuela hay 25 estudiantes en cada sala. Si hay 500 estudiantes en toda la escuela, ¿cuántas salas de clases hay?", "respuesta": 20, "tipo": "verbal"},
            25: {"texto": "Pame pasa 3 horas armando un puzle el día lunes. El martes, ella lo termina luego de armarlo por 2 horas más. El puzle tiene 300 piezas. En promedio, ¿cuántas piezas colocó correctamente cada hora?", "respuesta": 60, "tipo": "verbal"},
            26: {"texto": "Román prepara 12 pasteles entre las 4 y las 8 am. Luego prepara 9 pasteles entre 8 y 11 am. En promedio, ¿cuántos pasteles prepara cada hora?", "respuesta": 3, "tipo": "verbal"},
            27: {"texto": "Elisa tiene dos tercios del número de revistas que tiene Ramón. Si Elisa tiene 20 revistas, ¿cuántas revistas tiene Ramón?", "respuesta": 30, "tipo": "verbal"},
            28: {"texto": "Hay 71 niños en un bus. En la primera parada se bajan 17, en la siguiente se bajan 11 y en la última se bajan 32. ¿Cuántos niños quedan en el bus?", "respuesta": 11, "tipo": "verbal"},
            29: {"texto": "Un estudiante escribió 14 informes. Otro estudiante escribió 11 informes. Luego, otros 25 estudiantes escribieron 5 informes cada uno, y otros 2 estudiantes escribieron 1 informe cada uno. ¿Cuántos informes escribieron todos los estudiantes?", "respuesta": 152, "tipo": "verbal"},
            30: {"texto": "Si 6 personas pueden lavar 40 autos en un 4 días, ¿cuántas personas se necesitan para lavar 40 autos en medio día?", "respuesta": 48, "tipo": "verbal"},
            31: {"texto": "En un curso de 40 estudiantes, el 15% son mujeres. ¿Cuántos estudiantes son hombres?", "respuesta": 34, "tipo": "verbal"},
            32: {"texto": "Lucas comienza a plantar semillas 1 hora antes que Vale. Lucas planta 40 semillas cada hora y Vale planta 60 cada hora. Si ya han pasado 5 horas desde que Lucas empezó a plantar, ¿cuántas semillas más ha plantado Vale que Lucas?", "respuesta": 40, "tipo": "verbal"},
            33: {"texto": "Nico tiene una rutina de ejercicios para los sábados. Esta rutina incluye natación, bicicleta y trote. Primero nada por 25 minutos, luego hace elongaciones por 10 minutos y luego vuelve a nadar por otros 45 minutos. Después de un descanso de 5 minutos, anda en bicicleta cuesta arriba por 20, en terreno plano por 45 y luego en bajada por 15 minutos. Después de una pausa de 5 minutos, trota por 120 minutos y corre intensamente por 10 minutos más. Si Nico comienza su ejercicio a las 6:30, ¿qué hora será cuando termine?", "respuesta": 1130, "tipo": "verbal"},
            34: {"texto": "Un juego tiene 20 niveles. Joaquín debe obtener 300 puntos para pasar de nivel y debe superar cada nivel para poder continuar con el siguiente. Si Joaquín obtiene 1.500 puntos por hora y juega sin parar durante 2 horas y 15 minutos, ¿cuántos niveles le quedarán para terminar el juego?", "respuesta": 9, "tipo": "verbal"}
        }

    def obtener_inicio_por_edad(self, edad, sospecha_di):
        """Determina el ítem de inicio según la edad y sospecha de DI"""
        if sospecha_di:
            return 1
        elif 6 <= edad <= 7:
            return 3
        elif 8 <= edad <= 9:
            return 8
        elif 10 <= edad <= 16:
            return 11
        else:
            return 1

    def ejecutar_prueba(self, win, datos_participante):
        """Ejecuta la prueba de aritmética integrada en el sistema"""
        try:
            # Configurar elementos visuales
            instrucciones = visual.TextStim(win, text='', color='white', height=24, wrapWidth=1000)
            pregunta_text = visual.TextStim(win, text='', color='cyan', height=28, pos=(0, 100), wrapWidth=1100)
            respuesta_input = visual.TextBox2(win, pos=(0, -50), size=(800, 100), color='white', 
                                            lineColor='cyan', text='', placeholder='Escriba la respuesta numérica aquí...')
            continuar_text = visual.TextStim(win, text='Presione ENTER para enviar respuesta | ESC para salir', 
                                           color='white', height=18, pos=(0, -150))
            item_text = visual.TextStim(win, text='', color='yellow', height=20, pos=(0, -200))
            tiempo_text = visual.TextStim(win, text='', color='red', height=20, pos=(400, -200))
            
            edad = datos_participante['edad']
            
            # Preguntar sobre sospecha de DI
            sospecha_di = self.preguntar_sospecha_di(win, instrucciones)
            
            # Determinar ítem de inicio
            item_inicio = self.obtener_inicio_por_edad(edad, sospecha_di)
            
            # Mostrar instrucciones iniciales
            instrucciones.text = """ARITMÉTICA - WISC

Voy a hacerte preguntas de matemáticas y problemas aritméticos.
Responde con el número correcto. Tienes 30 segundos por cada pregunta.

Presiona ESPACIO para comenzar."""
            instrucciones.draw()
            win.flip()
            event.waitKeys(keyList=['space'])
            
            # Administrar prueba
            resultados = self.administrar_prueba(
                win, item_inicio, instrucciones, pregunta_text, 
                respuesta_input, continuar_text, item_text, tiempo_text
            )
            
            # Calcular resultados finales
            if resultados:
                puntaje_total = sum(r['puntaje'] for r in resultados)
                items_administrados = len(resultados)
                porcentaje_aciertos = (puntaje_total / items_administrados) * 100
                
                resultados_finales = {
                    'puntaje_total': puntaje_total,
                    'maximo_puntaje': 34,
                    'items_administrados': items_administrados,
                    'porcentaje_aciertos': porcentaje_aciertos,
                    'criterio_suspension': any(r.get('suspension', False) for r in resultados),
                    'sospecha_di': sospecha_di
                }
                
                self.resultados = resultados
                
                # Mostrar resumen
                instrucciones.text = f"""PRUEBA COMPLETADA

Resultados - Aritmética:
- Puntaje Total: {puntaje_total}/34
- Ítems Administrados: {items_administrados}
- Porcentaje de Aciertos: {porcentaje_aciertos:.1f}%
- Sospecha DI considerada: {'Sí' if sospecha_di else 'No'}

Presiona ESPACIO para continuar."""
                instrucciones.draw()
                win.flip()
                event.waitKeys(keyList=['space'])
                
                return resultados_finales
            
            return {'error': 'No se completaron ítems'}
            
        except Exception as e:
            print(f"Error en prueba de aritmética: {e}")
            return {'error': str(e)}

    def preguntar_sospecha_di(self, win, instrucciones):
        """Pregunta si existe sospecha de discapacidad intelectual"""
        instrucciones.text = """¿Existe sospecha de discapacidad intelectual 
o menor rendimiento cognitivo?

Presiona S para Sí
Presiona N para No"""
        instrucciones.draw()
        win.flip()
        
        keys = event.waitKeys(keyList=['s', 'n'])
        return 's' in keys

    def administrar_prueba(self, win, item_inicio, instrucciones, pregunta_text, 
                          respuesta_input, continuar_text, item_text, tiempo_text):
        """Administra la secuencia completa de la prueba"""
        resultados = []
        item_actual = item_inicio
        ceros_consecutivos = 0
        criterio_suspension = False
        
        while item_actual <= 34 and not criterio_suspension:
            # Administrar ítem actual
            resultado_item = self.administrar_item(
                win, item_actual, instrucciones, pregunta_text, 
                respuesta_input, continuar_text, item_text, tiempo_text
            )
            
            if resultado_item is None:  # Usuario presionó ESC
                break
                
            resultados.append(resultado_item)
            
            # Actualizar contador de ceros consecutivos
            if resultado_item['puntaje'] == 0:
                ceros_consecutivos += 1
            else:
                ceros_consecutivos = 0
            
            # Verificar criterio de suspensión (3 ceros consecutivos)
            if ceros_consecutivos >= 3:
                criterio_suspension = True
                resultado_item['suspension'] = True
            
            item_actual += 1
            
            # Pausa entre ítems (excepto si hay suspensión)
            if item_actual <= 34 and not criterio_suspension:
                instrucciones.text = "Presiona ESPACIO para continuar con la siguiente pregunta."
                instrucciones.draw()
                win.flip()
                event.waitKeys(keyList=['space'])
        
        return resultados

    def administrar_item(self, win, item_num, instrucciones, pregunta_text, 
                        respuesta_input, continuar_text, item_text, tiempo_text):
        """Administra un ítem individual con temporizador"""
        if item_num not in self.items:
            return None
            
        item_info = self.items[item_num]
        
        # Configurar elementos visuales
        instrucciones.text = f"Ítem {item_num}"
        pregunta_text.text = item_info['texto']
        respuesta_input.text = ''
        item_text.text = f"Ítem {item_num}/34 - Tipo: {item_info['tipo']}"
        
        # Temporizador
        tiempo_limite = 30  # 30 segundos por ítem
        timer = core.Clock()
        respuesta_recibida = False
        respuesta_usuario = ""
        
        while timer.getTime() < tiempo_limite and not respuesta_recibida:
            tiempo_restante = max(0, tiempo_limite - timer.getTime())
            tiempo_text.text = f"Tiempo: {tiempo_restante:.1f}s"
            
            # Recordatorio a los 20 segundos
            if 20 <= timer.getTime() < 21:
                instrucciones.text = f"Ítem {item_num} - ¿Tienes alguna respuesta?"
            
            # Dibujar todos los elementos
            instrucciones.draw()
            pregunta_text.draw()
            respuesta_input.draw()
            continuar_text.draw()
            item_text.draw()
            tiempo_text.draw()
            win.flip()
            
            # Verificar entrada del usuario
            keys = event.getKeys()
            if 'return' in keys and respuesta_input.text.strip():
                respuesta_recibida = True
                respuesta_usuario = respuesta_input.text.strip()
                break
            if 'escape' in keys:
                return None
            if 'r' in keys and 20 <= item_num <= 34:
                # Permitir repetición para ítems 20-34
                instrucciones.text = f"Repitiendo ítem {item_num}"
                instrucciones.draw()
                win.flip()
                core.wait(1)
        
        # Evaluar respuesta
        try:
            respuesta_num = int(respuesta_usuario) if respuesta_usuario else None
            es_correcta = (respuesta_num == item_info['respuesta'])
            puntaje = 1 if es_correcta else 0
        except:
            puntaje = 0
            es_correcta = False
        
        return {
            'item': item_num,
            'pregunta': item_info['texto'],
            'respuesta_usuario': respuesta_usuario,
            'respuesta_correcta': item_info['respuesta'],
            'puntaje': puntaje,
            'correcta': es_correcta,
            'tiempo': timer.getTime(),
            'tipo': item_info['tipo']
        }

class SistemaPruebasCognitivas:
    def __init__(self):
        self.win = None
        self.configurar_ventana()
        self.pruebas = {}
        self.resultados_totales = {}
        self.datos_participante = {}
        self.configurar_pruebas()
        
    def configurar_pruebas(self):
        """Registra todas las pruebas disponibles"""
        self.pruebas = {
            'cubos': {
                'nombre': 'Construcción con Cubos - WISC',
                'clase': PruebaCubos,
                'descripcion': 'Reproducción de diseños con cubos',
                'completada': False,
                'categoria': 'Perceptual',
                'duracion_estimada': '10-15 min'
            },
            'analogias': {
                'nombre': 'Analogías Verbales',
                'clase': PruebaAnalogias,
                'descripcion': 'Identificación de semejanzas entre conceptos',
                'completada': False,
                'categoria': 'Verbal',
                'duracion_estimada': '8-12 min'
            },
            'matrices': {
                'nombre': 'Matrices de Razonamiento',
                'clase': PruebaMatrices,
                'descripcion': 'Completar patrones de matrices y series',
                'completada': False,
                'categoria': 'Razonamiento',
                'duracion_estimada': '15-20 min'
            },
            'digitos': {
                'nombre': 'Retención de Dígitos',
                'clase': PruebaDigitos,
                'descripcion': 'Memoria auditiva de secuencias numéricas',
                'completada': False,
                'categoria': 'Memoria',
                'duracion_estimada': '10-15 min'
            },
            'claves': {
                'nombre': 'Prueba de Claves',
                'clase': PruebaClaves,
                'descripcion': 'Velocidad de procesamiento y coordinación visomotora',
                'completada': False,
                'categoria': 'Velocidad de Procesamiento',
                'duracion_estimada': '5-8 min'
            },
            'vocabulario': {
                'nombre': 'Vocabulario - WISC',
                'clase': PruebaVocabulario,
                'descripcion': 'Definición de palabras e identificaciónde objetos',
                'completada': False,
                'categoria': 'Verbal',
                'duracion_estimada': '10-15 min'
            },
            'balanzas': {
                'nombre': 'Balanzas - WISC',
                'clase': PruebaBalanzas,
                'descripcion': 'Razonamiento lógico con balanzas desequilibradas',
                'completada': False,
                'categoria': 'Razonamiento',
                'duracion_estimada': '15-20 min'
            },
            'rompecabezas': {
                'nombre': 'Rompecabezas Visuales - WISC',
                'clase': PruebaRompecabezas,
                'descripcion': 'Selección de piezas para formar rompecabezas completos',
                'completada': False,
                'categoria': 'Perceptual',
                'duracion_estimada': '12-18 min'
            },
            'retencion_imagenes': {
                'nombre': 'Retención de Imágenes - WISC',
                'clase': PruebaRetencionImagenes,
                'descripcion': 'Memoria visual de secuencias de imágenes',
                'completada': False,
                'categoria': 'Memoria',
                'duracion_estimada': '15-25 min'
            },
            'busqueda_simbolos': {
                'nombre': 'Búsqueda de Símbolos - WISC',
                'clase': PruebaBusquedaSimbolos,
                'descripcion': 'Velocidad de procesamiento y atención visual',
                'completada': False,
                'categoria': 'Velocidad de Procesamiento',
                'duracion_estimada': '5-8 min'
            },
            'informacion': {
                'nombre': 'Información - WISC',
                'clase': PruebaInformacion,
                'descripcion': 'Conocimientos generales y cultura',
                'completada': False,
                'categoria': 'Verbal',
                'duracion_estimada': '10-15 min'
            },
            'secuenciacion_letras_numeros': {
                'nombre': 'Secuenciación Letras-Números - WISC',
                'clase': PruebaSecuenciacionLetrasNumeros,
                'descripcion': 'Memoria de trabajo y secuenciación auditiva',
                'completada': False,
                'categoria': 'Memoria',
                'duracion_estimada': '10-15 min'
            },
            'comprension': {
                'nombre': 'Comprensión - WISC',
                'clase': PruebaComprension,
                'descripcion': 'Comprensión de situaciones sociales y razonamiento práctico',
                'completada': False,
                'categoria': 'Verbal',
                'duracion_estimada': '12-18 min'
            },
            'semejanzas': {
                'nombre': 'Semejanzas - WISC',
                'clase': PruebaSemejanzas,
                'descripcion': 'Identificación de relaciones conceptuales',
                'completada': False,
                'categoria': 'Verbal',
                'duracion_estimada': '10-15 min'
            },
            'aritmetica': {
                'nombre': 'Aritmética - WISC',
                'clase': PruebaAritmetica,
                'descripcion': 'Razonamiento aritmético y cálculo mental',
                'completada': False,
                'categoria': 'Razonamiento',
                'duracion_estimada': '15-25 min'
            }
        }

    # ... (el resto de los métodos de SistemaPruebasCognitivas se mantienen igual)
