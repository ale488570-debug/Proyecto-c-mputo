import pygame
import sys
import time
import matplotlib.pyplot as plt
from datetime import datetime

class AritmeticaWISC:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 700))
        pygame.display.set_caption("Prueba de Aritmética - WISC")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        self.small_font = pygame.font.SysFont('Arial', 18)
        
        # Colores
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 100, 255)
        self.GREEN = (0, 150, 0)
        self.RED = (255, 0, 0)
        
        # Datos de la prueba
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
        
        self.resultados = {}
        self.item_actual = None
        self.estado = "inicio"
        self.tiempo_inicio = 0
        self.tiempo_restante = 30
        self.input_text = ""
        self.edad = 0
        self.sospecha_di = False
        
    def dibujar_texto(self, texto, x, y, color=BLACK, font=None):
        if font is None:
            font = self.font
            
        lineas = texto.split('\n')
        for i, linea in enumerate(lineas):
            texto_surface = font.render(linea, True, color)
            self.screen.blit(texto_surface, (x, y + i * 30))
            
    def obtener_inicio_por_edad(self, edad, sospecha_di):
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
            
    def ejecutar_prueba(self):
        running = True
        
        while running:
            self.screen.fill(self.WHITE)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if self.estado == "ingreso_datos":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            try:
                                self.edad = int(self.input_text)
                                self.estado = "pregunta_sospecha"
                                self.input_text = ""
                            except:
                                pass
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            self.input_text += event.unicode
                            
                elif self.estado == "pregunta_sospecha":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:
                            self.sospecha_di = True
                            self.iniciar_prueba()
                        elif event.key == pygame.K_n:
                            self.sospecha_di = False
                            self.iniciar_prueba()
                            
                elif self.estado == "prueba":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.procesar_respuesta()
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        elif event.key == pygame.K_r and 20 <= self.item_actual <= 34:
                            # Repetición permitida para ítems 20-34
                            pass
                        else:
                            self.input_text += event.unicode
                            
                elif self.estado == "resultados":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_s:
                            self.guardar_resultados()
                        elif event.key == pygame.K_q:
                            running = False
            
            # Dibujar según el estado actual
            if self.estado == "inicio":
                self.dibujar_pantalla_inicio()
            elif self.estado == "ingreso_datos":
                self.dibujar_ingreso_datos()
            elif self.estado == "pregunta_sospecha":
                self.dibujar_pregunta_sospecha()
            elif self.estado == "prueba":
                self.dibujar_prueba()
            elif self.estado == "resultados":
                self.dibujar_resultados()
                
            pygame.display.flip()
            self.clock.tick(60)
            
        pygame.quit()
        
    def dibujar_pantalla_inicio(self):
        titulo = "PRUEBA DE ARITMÉTICA - WISC"
        instrucciones = "Presiona ESPACIO para comenzar"
        
        self.dibujar_texto(titulo, 350, 200, self.BLUE, pygame.font.SysFont('Arial', 32))
        self.dibujar_texto(instrucciones, 350, 300)
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.estado = "ingreso_datos"
                
    def dibujar_ingreso_datos(self):
        titulo = "DATOS DEL EVALUADO"
        instruccion = "Ingresa la edad del niño (6-16 años):"
        
        self.dibujar_texto(titulo, 350, 200, self.BLUE)
        self.dibujar_texto(instruccion, 350, 250)
        
        # Dibujar cuadro de entrada
        pygame.draw.rect(self.screen, self.BLACK, (350, 300, 200, 40), 2)
        self.dibujar_texto(self.input_text, 360, 305)
        
    def dibujar_pregunta_sospecha(self):
        pregunta = "¿Existe sospecha de discapacidad intelectual o menor rendimiento cognitivo? (Y/N)"
        self.dibujar_texto(pregunta, 250, 300)
        
    def iniciar_prueba(self):
        inicio = self.obtener_inicio_por_edad(self.edad, self.sospecha_di)
        self.item_actual = inicio
        self.estado = "prueba"
        self.tiempo_inicio = time.time()
        self.input_text = ""
        
    def dibujar_prueba(self):
        # Calcular tiempo restante
        tiempo_transcurrido = time.time() - self.tiempo_inicio
        self.tiempo_restante = max(0, 30 - int(tiempo_transcurrido))
        
        # Verificar si se acabó el tiempo
        if tiempo_transcurrido >= 30:
            self.procesar_respuesta()
            return
            
        # Dibujar información del ítem
        item_info = f"Ítem {self.item_actual}"
        tipo_item = f"Tipo: {self.items[self.item_actual]['tipo']}"
        tiempo_texto = f"Tiempo: {self.tiempo_restante}s"
        
        self.dibujar_texto(item_info, 50, 50, self.BLUE)
        self.dibujar_texto(tipo_item, 50, 80)
        self.dibujar_texto(tiempo_texto, 50, 110, self.RED if self.tiempo_restante < 10 else self.BLACK)
        
        # Dibujar el texto del ítem
        texto_item = self.items[self.item_actual]['texto']
        self.dibujar_texto(texto_item, 50, 180)
        
        # Instrucciones de repetición para ítems 20-34
        if 20 <= self.item_actual <= 34:
            repeticion_texto = "Presiona R para repetir el ítem (una sola vez)"
            self.dibujar_texto(repeticion_texto, 50, 400, self.BLUE)
        
        # Dibujar cuadro de entrada
        instruccion_respuesta = "Ingresa la respuesta (ENTER para enviar):"
        self.dibujar_texto(instruccion_respuesta, 50, 450)
        
        pygame.draw.rect(self.screen, self.BLACK, (50, 490, 300, 40), 2)
        self.dibujar_texto(self.input_text, 60, 495)
        
        # Recordatorio a los 20 segundos
        if tiempo_transcurrido >= 20 and tiempo_transcurrido < 21:
            recordatorio = "¿Tienes alguna respuesta?"
            self.dibujar_texto(recordatorio, 50, 550, self.RED)
            
    def procesar_respuesta(self):
        tiempo_utilizado = min(30, int(time.time() - self.tiempo_inicio))
        
        # Verificar si la respuesta es correcta
        try:
            respuesta_usuario = int(self.input_text) if self.input_text else None
            respuesta_correcta = self.items[self.item_actual]['respuesta']
            es_correcta = (respuesta_usuario == respuesta_correcta)
            puntaje = 1 if es_correcta else 0
        except:
            puntaje = 0
            es_correcta = False
            
        # Guardar resultado
        self.resultados[self.item_actual] = {
            'puntaje': puntaje,
            'tiempo': tiempo_utilizado,
            'respuesta_usuario': self.input_text,
            'correcta': es_correcta
        }
        
        # Verificar criterio de suspensión (3 ceros consecutivos)
        if self.verificar_suspension():
            self.estado = "resultados"
            return
            
        # Determinar siguiente ítem
        self.determinar_siguiente_item()
        
        # Reiniciar temporizador y entrada
        self.tiempo_inicio = time.time()
        self.input_text = ""
        
    def verificar_suspension(self):
        # Verificar si hay 3 ceros consecutivos
        items_ordenados = sorted(self.resultados.keys())
        if len(items_ordenados) >= 3:
            ultimos_tres = items_ordenados[-3:]
            if all(self.resultados[item]['puntaje'] == 0 for item in ultimos_tres):
                return True
        return False
        
    def determinar_siguiente_item(self):
        # Lógica para determinar el siguiente ítem según las reglas del WISC
        if self.item_actual < 34:
            self.item_actual += 1
        else:
            self.estado = "resultados"
            
    def dibujar_resultados(self):
        titulo = "RESULTADOS DE LA PRUEBA"
        self.dibujar_texto(titulo, 350, 50, self.BLUE, pygame.font.SysFont('Arial', 32))
        
        # Calcular estadísticas
        puntaje_total = sum(resultado['puntaje'] for resultado in self.resultados.values())
        total_items = len(self.resultados)
        porcentaje_correctas = (puntaje_total / total_items * 100) if total_items > 0 else 0
        
        # Mostrar estadísticas
        stats = [
            f"Edad del evaluado: {self.edad} años",
            f"Ítems administrados: {total_items}",
            f"Puntaje total: {puntaje_total}/34",
            f"Porcentaje de aciertos: {porcentaje_correctas:.1f}%",
            "",
            "Presiona S para guardar resultados",
            "Presiona Q para salir"
        ]
        
        for i, stat in enumerate(stats):
            self.dibujar_texto(stat, 350, 150 + i * 40)
            
        # Mostrar detalles por ítem
        y_pos = 400
        self.dibujar_texto("Detalle por ítem:", 50, y_pos, self.BLUE)
        y_pos += 40
        
        for item, resultado in sorted(self.resultados.items()):
            estado = "✓" if resultado['correcta'] else "✗"
            color = self.GREEN if resultado['correcta'] else self.RED
            texto_item = f"Ítem {item}: {resultado['respuesta_usuario']} ({estado}) - {resultado['tiempo']}s"
            self.dibujar_texto(texto_item, 50, y_pos, color)
            y_pos += 25
            
            if y_pos > 650:  # Paginación simple
                break
                
    def guardar_resultados(self):
        # Crear gráfico de resultados
        items = sorted(self.resultados.keys())
        puntajes = [self.resultados[item]['puntaje'] for item in items]
        tiempos = [self.resultados[item]['tiempo'] for item in items]
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Gráfico de puntajes
        ax1.bar(items, puntajes, color=['green' if p == 1 else 'red' for p in puntajes])
        ax1.set_title('Puntajes por Ítem')
        ax1.set_xlabel('Ítem')
        ax1.set_ylabel('Puntaje (0-1)')
        ax1.set_ylim(0, 1)
        
        # Gráfico de tiempos
        ax2.bar(items, tiempos, color='blue', alpha=0.7)
        ax2.set_title('Tiempo por Ítem (segundos)')
        ax2.set_xlabel('Ítem')
        ax2.set_ylabel('Tiempo (s)')
        ax2.set_ylim(0, 35)
        
        plt.tight_layout()
        
        # Guardar gráfico
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"resultados_aritmetica_{timestamp}.png"
        plt.savefig(filename)
        plt.show()
        
        # Guardar datos en archivo de texto
        with open(f"datos_aritmetica_{timestamp}.txt", "w") as f:
            f.write(f"PRUEBA DE ARITMÉTICA WISC - {datetime.now()}\n")
            f.write(f"Edad: {self.edad} años\n")
            f.write(f"Sospecha DI: {self.sospecha_di}\n")
            f.write(f"Puntaje total: {sum(puntajes)}/34\n\n")
            
            for item in items:
                resultado = self.resultados[item]
                f.write(f"Ítem {item}: {resultado['respuesta_usuario']} | "
                       f"Correcta: {resultado['correcta']} | "
                       f"Tiempo: {resultado['tiempo']}s\n")
        
        mensaje = f"Resultados guardados como {filename}"
        print(mensaje)

# Ejecutar la prueba
if __name__ == "__main__":
    prueba = AritmeticaWISC()
    prueba.ejecutar_prueba()
