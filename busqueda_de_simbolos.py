from psychopy import visual, core, event, gui, data
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
from datetime import datetime
import os

class BusquedaSimbolos:
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
        
        # Variables de la prueba
        self.edad = None
        self.forma = None  # 'A' o 'B'
        self.tiempo_inicio = None
        self.tiempo_ejecucion = 0
        self.respuestas_correctas = 0
        self.respuestas_incorrectas = 0
        self.errores_disposicion = 0
        self.errores_rotacion = 0
        self.items_completados = 0
        
        # Símbolos para la prueba (ejemplos simplificados)
        self.simbolos_base = [
            ['▲', '●', '■', '★', '◆'],  # Formas básicas
            ['⌂', '⌘', '☀', '☁', '☂'],  # Símbolos especiales
            ['♠', '♣', '♥', '♦', '♫'],  # Símbolos diversos
        ]
        
    def obtener_datos_participante(self):
        """Obtener información del participante"""
        info_dialog = gui.Dlg(title="Búsqueda de Símbolos - WISC")
        info_dialog.addField('Edad del participante:', 8)
        info_dialog.addField('Nombre:', 'Participante')
        info_dialog.show()
        
        if info_dialog.OK:
            self.edad = int(info_dialog.data[0])
            self.nombre = info_dialog.data[1]
            
            # Determinar forma según edad
            if self.edad in [6, 7]:
                self.forma = 'A'
                self.total_items = 40
                self.max_puntaje = 42
            else:
                self.forma = 'B'
                self.total_items = 60
                self.max_puntaje = 60
            return True
        return False
    
    def mostrar_instrucciones(self, texto):
        """Mostrar instrucciones en pantalla"""
        self.instruction.text = texto
        self.instruction.draw()
        self.win.flip()
        event.waitKeys(keyList=['space'])
    
    def crear_item_busqueda(self, item_num):
        """Crear un ítem de búsqueda de símbolos"""
        # En una implementación real, aquí cargarías imágenes reales
        grupo = visual.ElementArrayStim(
            self.win,
            nElements=5,
            sizes=50,
            fieldPos=[0, -100],
            elementTex='sin',
            elementMask=None
        )
        
        objetivo = visual.ElementArrayStim(
            self.win,
            nElements=1 if self.forma == 'A' else 2,
            sizes=50,
            fieldPos=[0, 100],
            elementTex='sin',
            elementMask=None
        )
        
        return grupo, objetivo
    
    def administrar_ejemplo(self):
        """Administrar ítems de ejemplo"""
        if self.forma == 'A':
            texto_ejemplo = """
            ÍTEMS DE EJEMPLO - FORMA A
            
            Voy a mostrarte cómo funciona la prueba:
            
            • Verás un símbolo objetivo arriba
            • Abajo hay 5 símbolos en el grupo de búsqueda
            • Si el símbolo objetivo está en el grupo, márcalo con una línea
            • Si NO está, marca la casilla "NO"
            • No marques símbolos que estén rotados o sean parecidos
            
            Presiona ESPACIO para ver los ejemplos
            """
        else:
            texto_ejemplo = """
            ÍTEMS DE EJEMPLO - FORMA B
            
            Voy a mostrarte cómo funciona la prueba:
            
            • Verás DOS símbolos objetivo arriba
            • Abajo hay 5 símbolos en el grupo de búsqueda
            • Si ALGUNO de los símbolos objetivos está en el grupo, márcalo
            • Si NINGUNO está, marca la casilla "NO"
            • No marques símbolos que estén rotados o sean parecidos
            
            Presiona ESPACIO para ver los ejemplos
            """
        
        self.mostrar_instrucciones(texto_ejemplo)
        
        # Mostrar ejemplos interactivos
        for i in range(2):  # Dos ejemplos
            self.mostrar_item_ejemplo(i)
    
    def mostrar_item_ejemplo(self, num_ejemplo):
        """Mostrar un ítem de ejemplo interactivo"""
        # Simulación de ítem de ejemplo
        self.message.text = f"Ejemplo {num_ejemplo + 1}\n\nObserva atentamente"
        self.message.draw()
        self.win.flip()
        core.wait(3)
        
        # Mostrar retroalimentación
        if num_ejemplo == 0:
            self.mostrar_instrucciones("¡Correcto! Así se hace el ejercicio.")
        else:
            self.mostrar_instrucciones("Recuerda: no marques símbolos rotados, marca 'NO' si no está el símbolo exacto.")
    
    def administrar_practica(self):
        """Administrar ítems de práctica"""
        texto_practica = """
        ÍTEMS DE PRÁCTICA
        
        Ahora practicarás con algunos ítems.
        
        Instrucciones:
        1. Mira el símbolo objetivo (arriba)
        2. Busca en el grupo de abajo
        3. Si está exactamente igual, márcalo
        4. Si no está, marca "NO"
        5. Trabaja con cuidado pero rápido
        
        Presiona ESPACIO para comenzar la práctica
        """
        self.mostrar_instrucciones(texto_practica)
        
        # Ítems de práctica simulados
        items_practica = 3
        practica_correcta = 0
        
        for i in range(items_practica):
            correcto = self.mostrar_item_practica(i)
            if correcto:
                practica_correcta += 1
        
        # Verificar comprensión
        if practica_correcta >= 2:
            self.mostrar_instrucciones("¡Excelente! Has entendido la tarea.\n\nPresiona ESPACIO para comenzar la prueba real.")
            return True
        else:
            self.mostrar_instrucciones("Vamos a repasar las instrucciones...\n\nPresiona ESPACIO para repetir la práctica.")
            return False
    
    def mostrar_item_practica(self, num_item):
        """Mostrar un ítem de práctica interactivo"""
        # Simulación de respuesta (en realidad sería con entrada del usuario)
        self.message.text = f"Práctica {num_item + 1}\n\nResponde según lo aprendido"
        self.message.draw()
        self.win.flip()
        
        # Esperar respuesta simulada
        keys = event.waitKeys(keyList=['y', 'n', 'space'], maxWait=10)
        
        if keys and keys[0] == 'y':
            self.mostrar_instrucciones("¡Correcto!")
            return True
        else:
            self.mostrar_instrucciones("Recuerda las reglas:\n- Marca solo símbolos idénticos\n- Si no está, marca 'NO'\n- Ignora símbolos rotados")
            return False
    
    def ejecutar_prueba_principal(self):
        """Ejecutar la prueba principal con tiempo límite"""
        texto_inicio = """
        PRUEBA PRINCIPAL
        
        Instrucciones finales:
        • Trabaja LO MÁS RÁPIDO QUE PUEDAS
        • Sin saltarte ningún ítem
        • En orden de arriba hacia abajo
        • Sin equivocarte
        • Tienes 2 minutos (120 segundos)
        
        Cuando estés listo, presiona ESPACIO para comenzar
        """
        self.mostrar_instrucciones(texto_inicio)
        
        # Iniciar temporizador
        self.tiempo_inicio = core.getTime()
        timer = core.CountdownTimer(120)  # 2 minutos
        
        # Bucle principal de la prueba
        item_actual = 0
        self.respuestas_correctas = 0
        self.respuestas_incorrectas = 0
        
        while timer.getTime() > 0 and item_actual < self.total_items:
            item_actual += 1
            
            # Mostrar ítem actual
            correcto = self.mostrar_item_prueba(item_actual, timer)
            
            if correcto is not None:
                if correcto:
                    self.respuestas_correctas += 1
                else:
                    self.respuestas_incorrectas += 1
            
            # Verificar si el usuario quiere salir
            if 'escape' in event.getKeys():
                break
        
        # Calcular tiempo de ejecución
        self.tiempo_ejecucion = 120 - timer.getTime() if timer.getTime() > 0 else 120
        self.items_completados = item_actual
    
    def mostrar_item_prueba(self, num_item, timer):
        """Mostrar un ítem de la prueba principal"""
        # Crear estímulo visual del ítem
        self.message.text = f"Ítem {num_item}/{self.total_items}\n\nTiempo restante: {timer.getTime():.1f}s"
        self.message.draw()
        
        # Dibujar símbolo objetivo (simulación)
        if self.forma == 'A':
            objetivo_text = visual.TextStim(self.win, text="▲", pos=(0, 200), color='black', height=60)
        else:
            objetivo_text = visual.TextStim(self.win, text="▲ ●", pos=(0, 200), color='black', height=60)
        
        objetivo_text.draw()
        
        # Dibujar grupo de búsqueda (simulación)
        for i in range(5):
            simbolo = visual.TextStim(self.win, text=["▲", "●", "■", "★", "◆"][i], 
                                    pos=(-200 + i*100, -100), color='black', height=40)
            simbolo.draw()
        
        # Dibujar opción "NO"
        no_text = visual.TextStim(self.win, text="NO", pos=(0, -200), color='black', height=30)
        no_text.draw()
        
        self.win.flip()
        
        # Capturar respuesta (simulación simplificada)
        keys = event.waitKeys(keyList=['1','2','3','4','5','n','escape'], maxWait=1)
        
        if keys:
            if keys[0] == 'escape':
                return None
            # En una implementación real, aquí verificarías la respuesta correcta
            return random.choice([True, False])  # Simulación
        
        return None
    
    def calcular_puntaje(self):
        """Calcular puntaje final según las reglas del WISC"""
        if self.forma == 'A':
            # Forma A: Correctas - Incorrectas + Bonificación por tiempo
            puntaje_bruto = self.respuestas_correctas - self.respuestas_incorrectas
            
            # Bonificación por tiempo si es puntaje perfecto
            if self.respuestas_correctas == 40:
                if self.tiempo_ejecucion <= 110:
                    puntaje_bruto += 2
                elif self.tiempo_ejecucion <= 119:
                    puntaje_bruto += 1
            
            # Asegurar mínimo de 0
            puntaje_bruto = max(0, puntaje_bruto)
            
        else:
            # Forma B: Correctas - Incorrectas
            puntaje_bruto = self.respuestas_correctas - self.respuestas_incorrectas
            puntaje_bruto = max(0, puntaje_bruto)
        
        return puntaje_bruto
    
    def mostrar_resultados(self):
        """Mostrar gráfico con los resultados"""
        puntaje_bruto = self.calcular_puntaje()
        
        # Crear figura con subgráficos
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
        
        # Gráfico 1: Puntaje bruto vs máximo
        categorias = ['Puntaje Bruto', 'Máximo Posible']
        valores = [puntaje_bruto, self.max_puntaje]
        colores = ['blue', 'gray']
        
        ax1.bar(categorias, valores, color=colores, alpha=0.7)
        ax1.set_title('Puntaje Bruto Total')
        ax1.set_ylabel('Puntos')
        for i, v in enumerate(valores):
            ax1.text(i, v + 0.5, str(v), ha='center', va='bottom')
        
        # Gráfico 2: Distribución de respuestas
        labels = ['Correctas', 'Incorrectas', 'No contestadas']
        valores_resp = [
            self.respuestas_correctas,
            self.respuestas_incorrectas,
            self.total_items - self.items_completados
        ]
        colores_resp = ['green', 'red', 'gray']
        
        ax2.pie(valores_resp, labels=labels, colors=colores_resp, autopct='%1.1f%%')
        ax2.set_title('Distribución de Respuestas')
        
        # Gráfico 3: Tiempo y eficiencia
        metrics = ['Tiempo (s)', 'Ítems/min']
        valores_met = [
            self.tiempo_ejecucion,
            (self.items_completados / self.tiempo_ejecucion * 60) if self.tiempo_ejecucion > 0 else 0
        ]
        
        ax3.bar(metrics, valores_met, color=['orange', 'purple'], alpha=0.7)
        ax3.set_title('Velocidad y Eficiencia')
        for i, v in enumerate(valores_met):
            ax3.text(i, v + 0.5, f'{v:.1f}', ha='center', va='bottom')
        
        # Gráfico 4: Puntajes de proceso
        if self.errores_disposicion > 0 or self.errores_rotacion > 0:
            errores = ['Disposición', 'Rotación']
            valores_err = [self.errores_disposicion, self.errores_rotacion]
            ax4.bar(errores, valores_err, color=['red', 'darkred'], alpha=0.7)
            ax4.set_title('Errores de Proceso')
            for i, v in enumerate(valores_err):
                ax4.text(i, v + 0.1, str(v), ha='center', va='bottom')
        else:
            ax4.text(0.5, 0.5, 'Sin errores de proceso\nregistrados', 
                    ha='center', va='center', transform=ax4.transAxes, fontsize=12)
            ax4.set_title('Errores de Proceso')
        
        plt.suptitle(f'BÚSQUEDA DE SÍMBOLOS - FORMA {self.forma}\n'
                    f'Edad: {self.edad} años | Tiempo: {self.tiempo_ejecucion:.1f}s', 
                    fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        # Guardar resultados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"busqueda_simbolos_{self.nombre}_{timestamp}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        
        # Mostrar resumen en PsychoPy
        resumen_texto = f"""
        RESULTADOS FINALES
        
        Forma: {self.forma}
        Edad: {self.edad} años
        Tiempo de ejecución: {self.tiempo_ejecucion:.1f} segundos
        
        PUNTUAJE BRUTO: {puntaje_bruto}/{self.max_puntaje}
        
        Detalle:
        • Respuestas correctas: {self.respuestas_correctas}
        • Respuestas incorrectas: {self.respuestas_incorrectas}
        • Ítems completados: {self.items_completados}/{self.total_items}
        
        Gráfico guardado como: {filename}
        
        Presiona ESPACIO para finalizar
        """
        
        self.mostrar_instrucciones(resumen_texto)
        
        return puntaje_bruto
    
    def ejecutar_prueba_completa(self):
        """Ejecutar la prueba completa"""
        if not self.obtener_datos_participante():
            return
        
        # Administrar ejemplo
        self.administrar_ejemplo()
        
        # Administrar práctica (repetir hasta que entienda)
        while not self.administrar_practica():
            pass
        
        # Ejecutar prueba principal
        self.ejecutar_prueba_principal()
        
        # Mostrar resultados
        self.mostrar_resultados()
        
        # Cerrar
        self.win.close()

# Ejecutar la prueba
if __name__ == "__main__":
    prueba = BusquedaSimbolos()
    prueba.ejecutar_prueba_completa()
