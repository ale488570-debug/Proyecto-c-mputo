class PruebaMatrices:
    def __init__(self):
        self.nombre = "Matrices de Razonamiento"
        self.descripcion = "Completar patrones de matrices y series"
        self.resultados = []
        
    def ejecutar_prueba(self, win, datos_participante):
        """Ejecuta la prueba de matrices integrada en el sistema"""
        try:
            # Configurar elementos visuales específicos para esta prueba
            instrucciones = visual.TextStim(win, text='', color='white', height=24, wrapWidth=1000)
            pregunta_text = visual.TextStim(win, text='', color='white', height=22, pos=(0, 200), wrapWidth=1100)
            opciones_text = visual.TextStim(win, text='', color='white', height=20, pos=(0, 0), wrapWidth=1100)
            temporizador_text = visual.TextStim(win, text='', color='yellow', height=18, pos=(0, -150))
            continuar_text = visual.TextStim(win, text='Presione 1-5 para seleccionar respuesta | ESC para salir', 
                                           color='white', height=18, pos=(0, -200))
            
            # Determinar ítem de inicio según edad
            edad = datos_participante['edad']
            if 6 <= edad <= 8:
                item_inicio = 1
            elif 9 <= edad <= 11:
                item_inicio = 5
            elif 12 <= edad <= 16:
                item_inicio = 9
            else:
                item_inicio = 1
            
            # Respuestas correctas (versión simplificada para integración)
            respuestas_correctas = {
                1: 3, 2: 4, 3: 4, 4: 3, 5: 5, 6: 2, 7: 2, 8: 1, 9: 5, 10: 5,
                11: 1, 12: 2, 13: 4, 14: 1, 15: 5, 16: 2, 17: 3, 18: 2, 19: 1,
                20: 5, 21: 3, 22: 4, 23: 5, 24: 2, 25: 1, 26: 3, 27: 3, 28: 4,
                29: 3, 30: 1, 31: 5, 32: 4
            }
            
            # Mostrar instrucciones iniciales
            instrucciones.text = """MATRICES DE RAZONAMIENTO

En esta prueba, verás matrices o series de figuras incompletas.
Debes seleccionar la opción que completa correctamente el patrón.

Usa las teclas 1-5 para seleccionar tu respuesta.
Tienes aproximadamente 30 segundos por ítem.

Presiona ESPACIO para comenzar."""
            instrucciones.draw()
            win.flip()
            event.waitKeys(keyList=['space'])
            
            # Administrar prueba principal
            resultados = []
            item_actual = item_inicio
            ceros_consecutivos = 0
            
            while item_actual <= 32 and ceros_consecutivos < 3:
                # Administrar ítem
                puntaje, tiempo = self.administrar_item(
                    item_actual, win, pregunta_text, opciones_text, 
                    temporizador_text, continuar_text, respuestas_correctas
                )
                
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
                
                # Pausa entre ítems (excepto el último)
                if item_actual <= 32 and ceros_consecutivos < 3:
                    instrucciones.text = "Presiona ESPACIO para continuar con el siguiente ítem."
                    instrucciones.draw()
                    win.flip()
                    event.waitKeys(keyList=['space'])
            
            # Calcular resultados finales
            if resultados:
                total_puntos = sum(r['puntaje'] for r in resultados)
                total_items = len(resultados)
                porcentaje = (total_puntos / total_items) * 100 if total_items > 0 else 0
                tiempo_promedio = np.mean([r['tiempo'] for r in resultados])
                
                resultados_finales = {
                    'puntaje_total': total_puntos,
                    'total_items': total_items,
                    'porcentaje_aciertos': porcentaje,
                    'tiempo_promedio': tiempo_promedio,
                    'items_correctos': total_puntos,
                    'puntaje_maximo': 32
                }
                
                # Guardar resultados detallados
                self.resultados = resultados
                
                # Mostrar resumen rápido
                instrucciones.text = f"""PRUEBA FINALIZADA

Resultados:
- Ítems respondidos: {total_items}
- Puntaje total: {total_puntos}/32
- Porcentaje de aciertos: {porcentaje:.1f}%

Presiona ESPACIO para continuar."""
                instrucciones.draw()
                win.flip()
                event.waitKeys(keyList=['space'])
                
                return resultados_finales
            
            return {'error': 'No se completaron ítems'}
            
        except Exception as e:
            print(f"Error en prueba de matrices: {e}")
            return {'error': str(e)}
    
    def administrar_item(self, item_num, win, pregunta_text, opciones_text, 
                        temporizador_text, continuar_text, respuestas_correctas):
        """Administra un ítem individual"""
        # Descripción del ítem
        pregunta_text.text = f"Ítem {item_num}: Completa el patrón de la matriz/serie\n\n¿Cuál opción completa correctamente el patrón?"
        
        # Opciones de respuesta
        opciones_text.text = "Opciones:\n1. Opción 1\n2. Opción 2\n3. Opción 3\n4. Opción 4\n5. Opción 5"
        
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
        
        # Calificar respuesta
        if respuesta == respuestas_correctas.get(item_num, 0):
            puntaje = 1
        else:
            puntaje = 0
        
        return puntaje, tiempo_respuesta

class SistemaPruebasCognitivas:
    def __init__(self):
        self.win = None
        self.configurar_ventana()
        self.pruebas = {}
        self.resultados_totales = {}
        self.datos_participante = {}
        self.configurar_pruebas()
        
    def configurar_ventana(self):
        """Configura la ventana principal del sistema"""
        self.win = visual.Window(
            size=[1200, 800],
            units='pix',
            fullscr=False,
            color='gray',
            winType='pyglet',
            allowGUI=True
        )
    
    def configurar_pruebas(self):
        """Registra todas las pruebas disponibles"""
        self.pruebas = {
            'cubos': {
                'nombre': 'Construcción con Cubos - WISC',
                'clase': PruebaCubos,
                'descripcion': 'Reproducción de diseños con cubos',
                'completada': False
            },
            'analogias': {
                'nombre': 'Analogías Verbales',
                'clase': PruebaAnalogias,
                'descripcion': 'Identificación de semejanzas entre conceptos',
                'completada': False
            },
            'matrices': {
                'nombre': 'Matrices de Razonamiento',
                'clase': PruebaMatrices,
                'descripcion': 'Completar patrones de matrices y series',
                'completada': False
            }
            # Las otras 12 pruebas se agregarán aquí
        }
    
    def obtener_datos_participante(self):
        """Obtiene información general del participante"""
        info_dialog = gui.Dlg(title="Sistema de Pruebas Cognitivas")
        info_dialog.addField('ID del Participante:')
        info_dialog.addField('Edad:', 25)
        info_dialog.addField('Género:', choices=['Masculino', 'Femenino', 'Otro/Prefiero no decir'])
        info_dialog.addField('Evaluador:')
        info_dialog.addField('Modalidad:', choices=['Secuencia Completa', 'Pruebas Individuales'])

        if info_dialog.show() == False:
            core.quit()

        self.datos_participante = {
            'id': info_dialog.data[0],
            'edad': info_dialog.data[1],
            'genero': info_dialog.data[2],
            'evaluador': info_dialog.data[3],
            'modalidad': info_dialog.data[4],
            'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def menu_principal(self):
        """Muestra el menú principal del sistema"""
        while True:
            opciones = list(self.pruebas.keys())
            opciones.append('secuencia_completa')
            opciones.append('salir')
            
            menu_texto = "SISTEMA DE PRUEBAS COGNITIVAS\n\n"
            menu_texto += f"Participante: {self.datos_participante['id']}\n"
            menu_texto += f"Edad: {self.datos_participante['edad']} años\n"
            menu_texto += f"Modalidad: {self.datos_participante['modalidad']}\n\n"
            menu_texto += "PRUEBAS DISPONIBLES:\n\n"
            
            for i, (key, prueba) in enumerate(self.pruebas.items(), 1):
                estado = "✓ COMPLETADA" if prueba['completada'] else "○ PENDIENTE"
                menu_texto += f"{i}. {prueba['nombre']} - {estado}\n"
                menu_texto += f"   {prueba['descripcion']}\n\n"
            
            menu_texto += f"{len(self.pruebas) + 1}. EJECUTAR SECUENCIA COMPLETA"
            menu_texto += f"\n{len(self.pruebas) + 2}. VER RESUMEN GENERAL"
            menu_texto += f"\n{len(self.pruebas) + 3}. SALIR"
            menu_texto += "\n\nSeleccione una opción (número):"
            
            texto_menu = visual.TextStim(self.win, text=menu_texto, height=20, 
                                       color='white', wrapWidth=1000)
            texto_menu.draw()
            self.win.flip()
            
            # Esperar selección
            teclas = event.waitKeys(keyList=[str(i) for i in range(1, len(opciones) + 2)])
            if teclas:
                seleccion = int(teclas[0]) - 1
                if seleccion < len(self.pruebas):
                    # Ejecutar prueba individual
                    clave_prueba = list(self.pruebas.keys())[seleccion]
                    self.ejecutar_prueba_individual(clave_prueba)
                elif seleccion == len(self.pruebas):
                    # Secuencia completa
                    self.ejecutar_secuencia_completa()
                elif seleccion == len(self.pruebas) + 1:
                    # Resumen general
                    self.mostrar_resumen_final()
                else:
                    # Salir
                    break
    
    def ejecutar_prueba_individual(self, clave_prueba):
        """Ejecuta una prueba individual"""
        prueba_info = self.pruebas[clave_prueba]
        
        # Mostrar información de la prueba
        texto_info = visual.TextStim(self.win, 
                                   text=f"Iniciando: {prueba_info['nombre']}\n\n{prueba_info['descripcion']}\n\nPresione ESPACIO para comenzar...",
                                   height=24, color='white', wrapWidth=1000)
        texto_info.draw()
        self.win.flip()
        event.waitKeys(keyList=['space'])
        
        # Ejecutar prueba
        try:
            prueba = prueba_info['clase']()
            
            if clave_prueba == 'cubos':
                prueba.win = self.win
                prueba.datos_participante = self.datos_participante
                prueba.administrar_prueba()
                resultados = prueba.calcular_puntajes_totales()
            elif clave_prueba == 'analogias':
                resultados = prueba.ejecutar_prueba(self.win, self.datos_participante)
            elif clave_prueba == 'matrices':
                resultados = prueba.ejecutar_prueba(self.win, self.datos_participante)
            
            # Guardar resultados y marcar como completada
            self.resultados_totales[clave_prueba] = resultados
            self.pruebas[clave_prueba]['completada'] = True
            
            print(f"Prueba {clave_prueba} completada. Resultados: {resultados}")
            
        except Exception as e:
            print(f"Error en prueba {clave_prueba}: {e}")
            texto_error = visual.TextStim(self.win, 
                                        text=f"Error en la prueba: {e}\n\nPresione ESPACIO para continuar...",
                                        height=24, color='red', wrapWidth=1000)
            texto_error.draw()
            self.win.flip()
            event.waitKeys(keyList=['space'])
