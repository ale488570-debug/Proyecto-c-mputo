import pygame
import sys
import time
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

class RetencionImagenes:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Prueba de Retención de Imágenes - WISC")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Colores
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.BLUE = (100, 100, 255)
        self.GREEN = (100, 255, 100)
        self.RED = (255, 100, 100)
        
        # Datos de la prueba
        self.respuestas_correctas = {
            'PA': ['B'],
            '1': ['A'],
            '2': ['C'],
            '3': ['E'],
            'PB': ['B', 'A'],
            'PC': ['D', 'A'],
            '4': ['C', 'D'],
            '5': ['B', 'A'],
            '6': ['A', 'E'],
            '7': ['F', 'B'],
            '8': ['A', 'B', 'E'],
            '9': ['B', 'E', 'D'],
            '10': ['D', 'F', 'C'],
            '11': ['A', 'F', 'E'],
            '12': ['F', 'C', 'B'],
            '13': ['B', 'H', 'C'],
            '14': ['A', 'C', 'E', 'F'],
            '15': ['B', 'C', 'F', 'D'],
            '16': ['G', 'B', 'D', 'F'],
            '17': ['G', 'D', 'B', 'A'],
            '18': ['C', 'B', 'I', 'H'],
            '19': ['D', 'G', 'A', 'I'],
            '20': ['E', 'F', 'H', 'B', 'A'],
            '21': ['E', 'G', 'B', 'C', 'H'],
            '22': ['F', 'B', 'I', 'H', 'D'],
            '23': ['A', 'C', 'F', 'H', 'K', 'E'],
            '24': ['L', 'B', 'H', 'L', 'J', 'D'],
            '25': ['H', 'B', 'L', 'G', 'C', 'E', 'J'],
            '26': ['G', 'A', 'K', 'C', 'F', 'D', 'I', 'B']
        }
        
        # Puntajes RImse y RImsr
        self.puntajes_proceso = {
            '1': {'RImse': 1, 'RImsr': 2},
            '2': {'RImse': 1, 'RImsr': 4},
            '3': {'RImse': 1, 'RImsr': 5},
            '4': {'RImse': 2, 'RImsr': 4},
            '5': {'RImse': 2, 'RImsr': 4},
            '6': {'RImse': 2, 'RImsr': 6},
            '7': {'RImse': 2, 'RImsr': 6},
            '8': {'RImse': 3, 'RImsr': 6},
            '9': {'RImse': 3, 'RImsr': 6},
            '10': {'RImse': 3, 'RImsr': 6},
            '11': {'RImse': 3, 'RImsr': 6},
            '12': {'RImse': 3, 'RImsr': 6},
            '13': {'RImse': 3, 'RImsr': 8},
            '14': {'RImse': 4, 'RImsr': 6},
            '15': {'RImse': 4, 'RImsr': 6},
            '16': {'RImse': 4, 'RImsr': 8},
            '17': {'RImse': 4, 'RImsr': 8},
            '18': {'RImse': 4, 'RImsr': 10},
            '19': {'RImse': 4, 'RImsr': 10},
            '20': {'RImse': 5, 'RImsr': 8},
            '21': {'RImse': 5, 'RImsr': 8},
            '22': {'RImse': 5, 'RImsr': 10},
            '23': {'RImse': 6, 'RImsr': 12},
            '24': {'RImse': 6, 'RImsr': 12},
            '25': {'RImse': 7, 'RImsr': 12},
            '26': {'RImse': 8, 'RImsr': 12}
        }
        
        # Variables de estado
        self.resultados = {}
        self.respuestas_actual = []
        self.item_actual = None
        self.estado = "inicio"
        self.tiempo_inicio = 0
        self.tiempo_exposicion = 0
        self.intento_actual = 1
        self.puntaje_total = 0
        self.puntajes_consecutivos_cero = 0
        self.rImse = 0
        self.rImsr = 0
        
    def mostrar_texto(self, texto, x=600, y=400, color=BLACK, fuente=None):
        if fuente is None:
            fuente = self.font
        lineas = texto.split('\n')
        for i, linea in enumerate(lineas):
            texto_surface = fuente.render(linea, True, color)
            texto_rect = texto_surface.get_rect(center=(x, y + i * 40))
            self.screen.blit(texto_surface, texto_rect)
        pygame.display.flip()
    
    def esperar_tecla(self):
        esperando = True
        while esperando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        esperando = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
    
    def mostrar_estimulo(self, item, tiempo_exposicion):
        self.screen.fill(self.WHITE)
        self.mostrar_texto(f"Ítem {item}\n\nMira las imágenes atentamente\n\nTiempo: {tiempo_exposicion} segundos")
        
        # En una implementación real, aquí cargarías las imágenes reales
        # Por ahora mostramos un placeholder
        pygame.draw.rect(self.screen, self.GRAY, (400, 300, 400, 200))
        self.mostrar_texto(f"ESTÍMULO {item}", 600, 400, self.BLACK, self.small_font)
        
        pygame.display.flip()
        time.sleep(tiempo_exposicion)
    
    def mostrar_pagina_respuestas(self, item):
        self.screen.fill(self.WHITE)
        self.mostrar_texto(f"Ítem {item}\n\nSeñala las imágenes en el orden correcto\n\nUsa las teclas A-L para seleccionar")
        
        # Mostrar opciones de respuesta (en una implementación real serían imágenes)
        opciones = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
        for i, opcion in enumerate(opciones[:8]):  # Mostrar primeras 8 opciones
            x = 200 + (i % 4) * 200
            y = 300 + (i // 4) * 150
            pygame.draw.rect(self.screen, self.GRAY, (x, y, 100, 100))
            self.mostrar_texto(opcion, x + 50, y + 50, self.BLACK, self.font)
        
        # Mostrar respuestas seleccionadas
        if self.respuestas_actual:
            resp_texto = "Respuestas: " + " - ".join(self.respuestas_actual)
            self.mostrar_texto(resp_texto, 600, 600, self.BLUE, self.small_font)
        
        self.mostrar_texto("ENTER: Terminar - BACKSPACE: Borrar última", 600, 700, self.BLACK, self.small_font)
        pygame.display.flip()
    
    def capturar_respuestas(self, item):
        self.respuestas_actual = []
        capturando = True
        
        while capturando:
            self.mostrar_pagina_respuestas(item)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        capturando = False
                    elif event.key == pygame.K_BACKSPACE:
                        if self.respuestas_actual:
                            self.respuestas_actual.pop()
                    elif pygame.K_a <= event.key <= pygame.K_l:
                        letra = chr(event.key).upper()
                        if letra not in self.respuestas_actual:
                            self.respuestas_actual.append(letra)
    
    def calcular_puntaje(self, item, respuestas):
        correctas = self.respuestas_correctas.get(str(item), [])
        
        if item in ['PA', '1', '2', '3']:
            # Ítems 1-3: 1 punto si correcto, 0 si incorrecto
            if respuestas == correctas:
                return 1
            else:
                return 0
        else:
            # Ítems 4-26: 2 puntos si orden correcto, 1 punto si imágenes correctas pero orden incorrecto
            if respuestas == correctas:
                return 2
            elif set(respuestas) == set(correctas):
                return 1
            else:
                return 0
    
    def administrar_item_practica(self, item, intentos_max=2):
        for intento in range(1, intentos_max + 1):
            self.intento_actual = intento
            
            # Mostrar estímulo
            if item in ['PA', '1', '2', '3']:
                self.mostrar_estimulo(item, 3)
            else:
                self.mostrar_estimulo(item, 5)
            
            # Capturar respuestas
            self.capturar_respuestas(item)
            
            # Calcular puntaje
            puntaje = self.calcular_puntaje(item, self.respuestas_actual)
            
            # Retroalimentación
            self.screen.fill(self.WHITE)
            if puntaje > 0:
                self.mostrar_texto("¡Correcto!", color=self.GREEN)
                time.sleep(1)
                return True
            else:
                if intento < intentos_max:
                    self.mostrar_texto("Incorrecto. Intentemos de nuevo.", color=self.RED)
                else:
                    self.mostrar_texto("Incorrecto. Continuemos.", color=self.RED)
                time.sleep(2)
        
        return False
    
    def administrar_item_regular(self, item):
        # Determinar tiempo de exposición
        if item in ['1', '2', '3']:
            tiempo_exposicion = 3
        else:
            tiempo_exposicion = 5
        
        # Mostrar estímulo
        self.mostrar_estimulo(item, tiempo_exposicion)
        
        # Capturar respuestas
        self.capturar_respuestas(item)
        
        # Calcular puntaje
        puntaje = self.calcular_puntaje(item, self.respuestas_actual)
        
        # Guardar resultados
        self.resultados[item] = {
            'respuestas': self.respuestas_actual.copy(),
            'puntaje': puntaje,
            'correctas': self.respuestas_correctas.get(str(item), [])
        }
        
        # Actualizar contador de ceros consecutivos
        if puntaje == 0:
            self.puntajes_consecutivos_cero += 1
        else:
            self.puntajes_consecutivos_cero = 0
            
            # Actualizar RImse y RImsr si es puntaje perfecto
            if puntaje == 2 or (item in ['1', '2', '3'] and puntaje == 1):
                if str(item) in self.puntajes_proceso:
                    self.rImse = self.puntajes_proceso[str(item)]['RImse']
                    self.rImsr = self.puntajes_proceso[str(item)]['RImsr']
        
        # Retroalimentación para ítems de aprendizaje
        if item in ['1', '2', '4', '5'] and puntaje == 0:
            self.screen.fill(self.WHITE)
            self.mostrar_texto("Retroalimentación correctiva")
            time.sleep(2)
    
    def ejecutar_prueba(self):
        # Pantalla de inicio
        self.screen.fill(self.WHITE)
        self.mostrar_texto("PRUEBA DE RETENCIÓN DE IMÁGENES\n\nWISC\n\nPresiona ESPACIO para comenzar")
        self.esperar_tecla()
        
        # Ítems de práctica A
        self.screen.fill(self.WHITE)
        self.mostrar_texto("Ítem de Práctica A\n\nPresiona ESPACIO para continuar")
        self.esperar_tecla()
        self.administrar_item_practica('PA')
        
        # Ítems 1-3
        for item in ['1', '2', '3']:
            if self.puntajes_consecutivos_cero >= 3:
                break
                
            self.screen.fill(self.WHITE)
            self.mostrar_texto(f"Ítem {item}\n\nPresiona ESPACIO para continuar")
            self.esperar_tecla()
            self.administrar_item_regular(item)
        
        # Ítems de práctica B y C
        self.screen.fill(self.WHITE)
        self.mostrar_texto("Ítem de Práctica B\n\nPresiona ESPACIO para continuar")
        self.esperar_tecla()
        self.administrar_item_practica('PB')
        
        self.screen.fill(self.WHITE)
        self.mostrar_texto("Ítem de Práctica C\n\nPresiona ESPACIO para continuar")
        self.esperar_tecla()
        self.administrar_item_practica('PC')
        
        # Ítems 4-26
        for item in range(4, 27):
            if self.puntajes_consecutivos_cero >= 3:
                break
                
            self.screen.fill(self.WHITE)
            self.mostrar_texto(f"Ítem {item}\n\nPresiona ESPACIO para continuar")
            self.esperar_tecla()
            self.administrar_item_regular(str(item))
        
        # Calcular puntaje total
        self.puntaje_total = sum(resultado['puntaje'] for resultado in self.resultados.values())
        
        # Mostrar resultados
        self.mostrar_resultados()
    
    def mostrar_resultados(self):
        # Crear gráfico
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Gráfico 1: Puntaje por ítem
        items = list(self.resultados.keys())
        puntajes = [self.resultados[item]['puntaje'] for item in items]
        
        ax1.bar(items, puntajes, color=['red' if p == 0 else 'green' for p in puntajes])
        ax1.set_title('Puntaje por Ítem')
        ax1.set_xlabel('Ítem')
        ax1.set_ylabel('Puntaje')
        ax1.set_ylim(0, 2)
        
        # Gráfico 2: Puntajes de proceso
        categorias = ['Puntaje Total', 'RImse', 'RImsr']
        valores = [self.puntaje_total, self.rImse, self.rImsr]
        maximos = [49, 8, 12]  # Máximos según el manual
        
        ax2.bar(categorias, valores, color=['blue', 'orange', 'green'])
        for i, (v, m) in enumerate(zip(valores, maximos)):
            ax2.text(i, v + 0.1, f'{v}/{m}', ha='center', va='bottom')
        
        ax2.set_title('Puntajes de Proceso')
        ax2.set_ylabel('Puntaje')
        
        plt.tight_layout()
        
        # Guardar gráfico
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"resultados_retencion_imagenes_{timestamp}.png"
        plt.savefig(filename)
        plt.show()
        
        # Mostrar resumen en pantalla
        self.screen.fill(self.WHITE)
        resumen_texto = f"""
        RESULTADOS FINALES
        
        Puntaje Total: {self.puntaje_total}/49
        RImse: {self.rImse}/8
        RImsr: {self.rImsr}/12
        
        Gráfico guardado como: {filename}
        
        Presiona ESPACIO para salir
        """
        self.mostrar_texto(resumen_texto)
        self.esperar_tecla()
        
        pygame.quit()

# Ejecutar la prueba
if __name__ == "__main__":
    prueba = RetencionImagenes()
    prueba.ejecutar_prueba()
