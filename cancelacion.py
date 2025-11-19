from psychopy import visual, core, event, gui, data
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import random
import os

class CancelacionWISC:
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
        self.timer_text = visual.TextStim(self.win, color='red', height=40, pos=(0, 350))
        
        # Variables de la prueba
        self.nombre = ""
        self.tiempo_limite = 45  # 45 segundos por ítem
        self.resultados = {
            'item1': {'correctas': 0, 'incorrectas': 0, 'tiempo': 0, 'puntaje': 0},
            'item2': {'correctas': 0, 'incorrectas': 0, 'tiempo': 0, 'puntaje': 0}
        }
        
        # Configuración de la cuadrícula para los ítems
        self.configurar_estímulos()
        
    def configurar_estímulos(self):
        """Configurar los estímulos visuales para la prueba"""
        # Lista de animales y objetos (simplificados para la simulación)
        self.animales = ['🐱', '🐶', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🐨', '🐯', 
                        '🦁', '🐮', '🐷', '🐸', '🐵', '🐔', '🐦', '🐤', '🦆', '🦅']
        
        self.objetos = ['📱', '💻', '📚', '✏️', '📎', '🔑', '💡', '⏰', '🎈', '🎯',
                       '🏠', '🚗', '✈️', '🚲', '🎮', '🎸', '📷', '🛋️', '💎', '🔦']
        
        # Configuración de las cuadrículas
        self.filas = 8
        self.columnas = 10
        self.total_celdas = self.filas * self.columnas
        
    def obtener_datos_participante(self):
        """Obtener información del participante"""
        info_dialog = gui.Dlg(title="Cancelación - WISC")
        info_dialog.addField('Nombre:', 'Participante')
        info_dialog.show()
        
        if info_dialog.OK:
            self.nombre = info_dialog.data[0]
            return True
        return False
    
    def mostrar_instrucciones(self, texto):
        """Mostrar instrucciones en pantalla"""
        self.instruction.text = texto
        self.instruction.draw()
        self.win.flip()
        event.waitKeys(keyList=['space'])
    
    def crear_cuadricula_aleatoria(self):
        """Crear cuadrícula aleatoria para el ítem 1"""
        # Mezclar animales y objetos
        todos_estímulos = self.animales[:20] + self.objetos[:60]
        random.shuffle(todos_estímulos)
        
        cuadricula = []
        for i in range(self.filas):
            fila = []
            for j in range(self.columnas):
                if todos_estímulos:
                    fila.append(todos_estímulos.pop())
                else:
                    fila.append(" ")
            cuadricula.append(fila)
        
        return cuadricula
    
    def crear_cuadricula_estructurada(self):
        """Crear cuadrícula estructurada para el ítem 2"""
        # En una cuadrícula estructurada, los animales estarían agrupados
        cuadricula = []
        animales_disponibles = self.animales.copy()
        objetos_disponibles = self.objetos.copy()
        random.shuffle(animales_disponibles)
        random.shuffle(objetos_disponibles)
        
        # Crear patrones más estructurados
        for i in range(self.filas):
            fila = []
            for j in range(self.columnas):
                # Crear zonas con mayor densidad de animales
                if (i % 3 == 0 and j % 3 == 0) or (i % 3 == 1 and j % 3 == 1):
                    if animales_disponibles:
                        fila.append(animales_disponibles.pop())
                    else:
                        fila.append(objetos_disponibles.pop() if objetos_disponibles else " ")
                else:
                    if objetos_disponibles:
                        fila.append(objetos_disponibles.pop())
                    else:
                        fila.append(animales_disponibles.pop() if animales_disponibles else " ")
            cuadricula.append(fila)
        
        return cuadricula
    
    def dibujar_cuadricula(self, cuadricula, selecciones=None):
        """Dibujar la cuadrícula en pantalla"""
        if selecciones is None:
            selecciones = set()
        
        ancho_celda = 80
        alto_celda = 80
        inicio_x = -400
        inicio_y = 250
        
        # Dibujar cada celda
        for i, fila in enumerate(cuadricula):
            for j, estimulo in enumerate(fila):
                x = inicio_x + j * ancho_celda + ancho_celda / 2
                y = inicio_y - i * alto_celda - alto_celda / 2
                
                # Dibujar celda
                celda = visual.Rect(self.win, width=ancho_celda-5, height=alto_celda-5, 
                                  pos=(x, y), lineColor='black', fillColor=None)
                celda.draw()
                
                # Dibujar estímulo
                if estimulo != " ":
                    texto = visual.TextStim(self.win, text=estimulo, pos=(x, y), height=30)
                    texto.draw()
                
                # Dibujar marca si está seleccionado
                if (i, j) in selecciones:
                    linea1 = visual.Line(self.win, start=(x-25, y-25), end=(x+25, y+25), 
                                       lineColor='red', lineWidth=3)
                    linea2 = visual.Line(self.win, start=(x-25, y+25), end=(x+25, y-25), 
                                       lineColor='red', lineWidth=3)
                    linea1.draw()
                    linea2.draw()
    
    def administrar_ejemplo_practica(self):
        """Administrar ítems de ejemplo y práctica"""
        # Ítem de ejemplo
        self.mostrar_instrucciones(
            "EJEMPLO\n\n"
            "Voy a mostrarte cómo funciona la prueba.\n"
            "Verás diferentes dibujos: algunos son animales, otros son objetos.\n"
            "Tu tarea es marcar SOLO los animales con una línea diagonal.\n\n"
            "Presiona ESPACIO para ver el ejemplo."
        )
        
        # Mostrar ejemplo
        cuadricula_ejemplo = [
            ['🐱', '📱', '🐶', '💻'],
            ['📚', '🐭', '✏️', '🐹']
        ]
        
        self.mostrar_cuadricula_interactiva(cuadricula_ejemplo, modo_ejemplo=True)
        
        # Ítem de práctica
        self.mostrar_instrucciones(
            "PRÁCTICA\n\n"
            "Ahora practicarás tú.\n"
            "Marca SOLO los animales con una línea diagonal.\n"
            "Trabaja con cuidado.\n\n"
            "Presiona ESPACIO para comenzar la práctica."
        )
        
        cuadricula_practica = self.crear_cuadricula_aleatoria()[:4]  # Cuadrícula más pequeña para práctica
        
        correcto = self.mostrar_cuadricula_interactiva(cuadricula_practica, tiempo_limite=30, modo_practica=True)
        
        if correcto:
            self.mostrar_instrucciones("¡Excelente! Has entendido la tarea.\n\nPresiona ESPACIO para continuar con la prueba real.")
        else:
            self.mostrar_instrucciones("Recuerda: marca SOLO los animales.\nTrabaja rápido pero con cuidado.\n\nPresiona ESPACIO para continuar.")
        
        return True
    
    def mostrar_cuadricula_interactiva(self, cuadricula, tiempo_limite=None, modo_ejemplo=False, modo_practica=False):
        """Mostrar cuadrícula interactiva para que el participante marque estímulos"""
        selecciones = set()
        mouse = event.Mouse()
        timer = core.Clock()
        
        if tiempo_limite:
            timer.reset()
        
        while True:
            # Verificar tiempo límite
            if tiempo_limite and timer.getTime() >= tiempo_limite:
                break
            
            # Actualizar timer
            if tiempo_limite:
                tiempo_restante = tiempo_limite - timer.getTime()
                self.timer_text.text = f"Tiempo: {tiempo_restante:.1f}s"
            else:
                self.timer_text.text = ""
            
            # Dibujar todo
            self.timer_text.draw()
            self.dibujar_cuadricula(cuadricula, selecciones)
            
            # Instrucciones según modo
            if modo_ejemplo:
                instruccion = "EJEMPLO: Yo marco los animales"
            elif modo_practica:
                instruccion = "PRÁCTICA: Marca los animales - Click para marcar, ESPACIO para terminar"
            else:
                instruccion = "Marca los animales - Click para marcar"
            
            texto_inst = visual.TextStim(self.win, text=instruccion, pos=(0, -350), height=24)
            texto_inst.draw()
            
            self.win.flip()
            
            # Manejar eventos
            if mouse.getPressed()[0]:  # Click izquierdo
                pos = mouse.getPos()
                # Convertir posición a coordenadas de celda
                ancho_celda = 80
                alto_celda = 80
                inicio_x = -400
                inicio_y = 250
                
                col = int((pos[0] - inicio_x) / ancho_celda)
                fila = int((inicio_y - pos[1]) / alto_celda)
                
                if 0 <= fila < len(cuadricula) and 0 <= col < len(cuadricula[0]):
                    celda = (fila, col)
                    if celda in selecciones:
                        selecciones.remove(celda)
                    else:
                        selecciones.add(celda)
                
                core.wait(0.2)  # Evitar múltiples clics
            
            keys = event.getKeys()
            if 'space' in keys and (modo_practica or modo_ejemplo):
                break
            elif 'escape' in keys:
                return False
        
        # Evaluar práctica
        if modo_practica:
            return self.evaluar_selecciones(cuadricula, selecciones, solo_verificar=True)
        
        return True
    
    def evaluar_selecciones(self, cuadricula, selecciones, item_num=None):
        """Evaluar las selecciones del participante"""
        correctas = 0
        incorrectas = 0
        
        for fila, col in selecciones:
            if 0 <= fila < len(cuadricula) and 0 <= col < len(cuadricula[0]):
                estimulo = cuadricula[fila][col]
                if estimulo in self.animales:
                    correctas += 1
                else:
                    incorrectas += 1
        
        if item_num:
            self.resultados[item_num]['correctas'] = correctas
            self.resultados[item_num]['incorrectas'] = incorrectas
            self.resultados[item_num]['puntaje'] = max(0, correctas - incorrectas)
        
        return correctas, incorrectas
    
    def administrar_item(self, item_num, cuadricula):
        """Administrar un ítem completo"""
        self.mostrar_instrucciones(
            f"ÍTEM {item_num[-1]} - {'ALEATORIO' if item_num == 'item1' else 'ESTRUCTURADO'}\n\n"
            "Cuando diga EMPIEZA, marca CADA animal.\n"
            "NO marques nada más.\n"
            "Trabaja LO MÁS RÁPIDO QUE PUEDAS, sin equivocarte.\n\n"
            "Presiona ESPACIO cuando estés listo para comenzar."
        )
        
        # Preparar temporizador
        timer = core.CountdownTimer(self.tiempo_limite)
        selecciones = set()
        mouse = event.Mouse()
        
        # Pantalla de preparación
        self.message.text = "¡EMPIEZA!"
        self.message.draw()
        self.win.flip()
        core.wait(1)
        
        # Bucle principal del ítem
        timer.reset()
        while timer.getTime() > 0:
            tiempo_restante = timer.getTime()
            self.timer_text.text = f"Tiempo: {tiempo_restante:.1f}s"
            
            # Dibujar cuadrícula
            self.timer_text.draw()
            self.dibujar_cuadricula(cuadricula, selecciones)
            
            # Instrucción
            instruccion = visual.TextStim(self.win, text="Marca los animales - Trabaja rápido", pos=(0, -350), height=24)
            instruccion.draw()
            
            self.win.flip()
            
            # Manejar clics del mouse
            if mouse.getPressed()[0]:
                pos = mouse.getPos()
                ancho_celda = 80
                alto_celda = 80
                inicio_x = -400
                inicio_y = 250
                
                col = int((pos[0] - inicio_x) / ancho_celda)
                fila = int((inicio_y - pos[1]) / alto_celda)
                
                if 0 <= fila < len(cuadricula) and 0 <= col < len(cuadricula[0]):
                    celda = (fila, col)
                    if celda not in selecciones:
                        selecciones.add(celda)
                
                core.wait(0.1)
            
            # Verificar si quiere salir
            if 'escape' in event.getKeys():
                break
        
        # Registrar tiempo
        tiempo_usado = self.tiempo_limite - timer.getTime() if timer.getTime() > 0 else self.tiempo_limite
        self.resultados[item_num]['tiempo'] = tiempo_usado
        
        # Evaluar selecciones
        self.evaluar_selecciones(cuadricula, selecciones, item_num)
        
        # Mostrar mensaje de fin
        self.message.text = "¡TIEMPO!"
        self.message.draw()
        self.win.flip()
        core.wait(1)
    
    def ejecutar_prueba(self):
        """Ejecutar la prueba completa"""
        # Pantalla de inicio
        self.mostrar_instrucciones(
            "PRUEBA DE CANCELACIÓN - WISC\n\n"
            "En esta prueba verás diferentes dibujos.\n"
            "Tu tarea es encontrar y marcar SOLO los ANIMALES.\n"
            "Trabaja lo más rápido que puedas, pero con cuidado.\n\n"
            "Presiona ESPACIO para comenzar"
        )
        
        # Administrar ejemplo y práctica
        self.administrar_ejemplo_practica()
        
        # Ítem 1 - Aleatorio
        cuadricula_aleatoria = self.crear_cuadricula_aleatoria()
        self.administrar_item('item1', cuadricula_aleatoria)
        
        # Transición entre ítems
        self.mostrar_instrucciones(
            "Excelente trabajo en el primer ítem.\n\n"
            "Ahora continuaremos con el segundo ítem.\n"
            "Recuerda: marca SOLO los animales, trabaja rápido.\n\n"
            "Presiona ESPACIO para continuar"
        )
        
        # Ítem 2 - Estructurado
        cuadricula_estructurada = self.crear_cuadricula_estructurada()
        self.administrar_item('item2', cuadricula_estructurada)
        
        # Calcular puntajes finales
        self.calcular_puntajes_finales()
        
        # Mostrar resultados
        self.mostrar_resultados()
    
    def calcular_puntajes_finales(self):
        """Calcular puntajes finales de la prueba"""
        # Los puntajes ya se calcularon durante la administración
        # Sumar puntajes totales
        self.puntaje_total = (self.resultados['item1']['puntaje'] + 
                            self.resultados['item2']['puntaje'])
        
        # Puntajes de proceso
        self.cana = self.resultados['item1']['puntaje']  # Cancelación aleatorio
        self.cane = self.resultados['item2']['puntaje']  # Cancelación estructurado
    
    def mostrar_resultados(self):
        """Mostrar gráfico con los resultados"""
        # Crear figura
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Gráfico 1: Comparación entre ítems
        items = ['Aleatorio', 'Estructurado']
        puntajes = [self.resultados['item1']['puntaje'], self.resultados['item2']['puntaje']]
        maximos = [64, 64]
        
        bars = ax1.bar(items, puntajes, color=['lightcoral', 'lightblue'], alpha=0.7)
        ax1.set_title('Puntaje por Tipo de Cuadrícula')
        ax1.set_ylabel('Puntaje')
        ax1.set_ylim(0, 70)
        
        # Agregar valores y líneas de máximo
        for i, (v, m) in enumerate(zip(puntajes, maximos)):
            ax1.text(i, v + 1, f'{v}/{m}', ha='center', va='bottom')
            ax1.axhline(y=m, color='red', linestyle='--', alpha=0.3)
        
        # Gráfico 2: Tiempos de ejecución
        tiempos = [self.resultados['item1']['tiempo'], self.resultados['item2']['tiempo']]
        tiempo_limite = self.tiempo_limite
        
        bars_tiempo = ax2.bar(items, tiempos, color=['orange', 'green'], alpha=0.7)
        ax2.set_title('Tiempo de Ejecución por Ítem')
        ax2.set_ylabel('Tiempo (segundos)')
        ax2.set_ylim(0, 50)
        ax2.axhline(y=tiempo_limite, color='red', linestyle='--', label='Límite (45s)')
        ax2.legend()
        
        # Agregar valores
        for i, v in enumerate(tiempos):
            ax2.text(i, v + 1, f'{v:.1f}s', ha='center', va='bottom')
        
        # Gráfico 3: Eficiencia (puntaje por segundo)
        eficiencias = [puntajes[0]/tiempos[0] if tiempos[0] > 0 else 0,
                      puntajes[1]/tiempos[1] if tiempos[1] > 0 else 0]
        
        ax3.bar(items, eficiencias, color=['purple', 'brown'], alpha=0.7)
        ax3.set_title('Eficiencia (Puntaje por Segundo)')
        ax3.set_ylabel('Puntos por Segundo')
        
        # Agregar valores
        for i, v in enumerate(eficiencias):
            ax3.text(i, v + 0.01, f'{v:.2f}', ha='center', va='bottom')
        
        # Gráfico 4: Resumen general
        categorias = ['Puntaje Total', 'CANA', 'CANe']
        valores = [self.puntaje_total, self.cana, self.cane]
        maximos_totales = [128, 64, 64]
        
        ax4.bar(categorias, valores, color=['blue', 'red', 'green'], alpha=0.7)
        ax4.set_title('Puntajes de Proceso y Total')
        ax4.set_ylabel('Puntaje')
        
        # Agregar valores y máximos
        for i, (v, m) in enumerate(zip(valores, maximos_totales)):
            ax4.text(i, v + 2, f'{v}/{m}', ha='center', va='bottom')
            ax4.axhline(y=m, color='red', linestyle='--', alpha=0.3)
        
        plt.suptitle(f'PRUEBA DE CANCELACIÓN - WISC\n'
                    f'Participante: {self.nombre} | Puntaje Total: {self.puntaje_total}/128', 
                    fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        
        # Guardar resultados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cancelacion_{self.nombre}_{timestamp}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        
        # Mostrar resumen detallado
        self.mostrar_resumen_detallado(filename)
    
    def mostrar_resumen_detallado(self, filename):
        """Mostrar resumen detallado de los resultados"""
        resumen_texto = f"""
        RESULTADOS FINALES - CANCELACIÓN
        
        Participante: {self.nombre}
        
        PUNTAJE TOTAL: {self.puntaje_total}/128
        
        Detalle por ítem:
        
        ÍTEM 1 (Aleatorio):
        • Correctas: {self.resultados['item1']['correctas']}
        • Incorrectas: {self.resultados['item1']['incorrectas']}
        • Puntaje: {self.resultados['item1']['puntaje']}/64
        • Tiempo: {self.resultados['item1']['tiempo']:.1f}s
        
        ÍTEM 2 (Estructurado):
        • Correctas: {self.resultados['item2']['correctas']}
        • Incorrectas: {self.resultados['item2']['incorrectas']}
        • Puntaje: {self.resultados['item2']['puntaje']}/64
        • Tiempo: {self.resultados['item2']['tiempo']:.1f}s
        
        Puntajes de Proceso:
        • CANA (Aleatorio): {self.cana}/64
        • CANe (Estructurado): {self.cane}/64
        
        Gráfico guardado como: {filename}
        
        Presiona ESPACIO para finalizar
        """
        
        self.mostrar_instrucciones(resumen_texto)
        self.win.close()

# Ejecutar la prueba
if __name__ == "__main__":
    prueba = CancelacionWISC()
    if prueba.obtener_datos_participante():
        prueba.ejecutar_prueba()
