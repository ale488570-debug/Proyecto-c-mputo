import pandas as pd
import matplotlib.pyplot as plt
from psychopy import visual, core, event, gui, data
import numpy as np
import os
from datetime import datetime

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
                'descripcion': 'Reproducción de diseños con cubos'
            },
            'analogias': {
                'nombre': 'Analogías Verbales',
                'clase': PruebaAnalogias,
                'descripcion': 'Identificación de semejanzas entre conceptos'
            }
            # Las otras 13 pruebas se agregarán aquí
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
            menu_texto += f"Edad: {self.datos_participante['edad']} años\n\n"
            menu_texto += "PRUEBAS DISPONIBLES:\n\n"
            
            for i, (key, prueba) in enumerate(self.pruebas.items(), 1):
                menu_texto += f"{i}. {prueba['nombre']} - {prueba['descripcion']}\n"
            
            menu_texto += f"\n{len(self.pruebas) + 1}. EJECUTAR SECUENCIA COMPLETA"
            menu_texto += f"\n{len(self.pruebas) + 2}. SALIR"
            menu_texto += "\n\nSeleccione una opción (número):"
            
            texto_menu = visual.TextStim(self.win, text=menu_texto, height=20, 
                                       color='white', wrapWidth=1000)
            texto_menu.draw()
            self.win.flip()
            
            # Esperar selección
            teclas = event.waitKeys(keyList=[str(i) for i in range(1, len(opciones) + 1)])
            if teclas:
                seleccion = int(teclas[0]) - 1
                if seleccion < len(self.pruebas):
                    # Ejecutar prueba individual
                    clave_prueba = list(self.pruebas.keys())[seleccion]
                    self.ejecutar_prueba_individual(clave_prueba)
                elif seleccion == len(self.pruebas):
                    # Secuencia completa
                    self.ejecutar_secuencia_completa()
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
                prueba.win = self.win  # Reutilizar ventana
                prueba.datos_participante = self.datos_participante
                prueba.administrar_prueba()
                resultados = prueba.calcular_puntajes_totales()
            elif clave_prueba == 'analogias':
                resultados = prueba.ejecutar_prueba(self.win, self.datos_participante)
            
            # Guardar resultados
            self.resultados_totales[clave_prueba] = resultados
            print(f"Prueba {clave_prueba} completada. Resultados: {resultados}")
            
        except Exception as e:
            print(f"Error en prueba {clave_prueba}: {e}")
    
    def ejecutar_secuencia_completa(self):
        """Ejecuta todas las pruebas en secuencia"""
        texto_info = visual.TextStim(self.win, 
                                   text="INICIANDO SECUENCIA COMPLETA\n\nSe ejecutarán todas las pruebas en orden.\n\nPresione ESPACIO para comenzar...",
                                   height=24, color='white', wrapWidth=1000)
        texto_info.draw()
        self.win.flip()
        event.waitKeys(keyList=['space'])
        
        for clave_prueba in self.pruebas.keys():
            self.ejecutar_prueba_individual(clave_prueba)
            
            # Pausa entre pruebas
            if list(self.pruebas.keys()).index(clave_prueba) < len(self.pruebas) - 1:
                texto_pausa = visual.TextStim(self.win, 
                                            text="Prueba completada.\n\nPreparando siguiente prueba...\n\nPresione ESPACIO para continuar...",
                                            height=24, color='white', wrapWidth=1000)
                texto_pausa.draw()
                self.win.flip()
                event.waitKeys(keyList=['space'])
        
        # Mostrar resumen final
        self.mostrar_resumen_final()
    
    def mostrar_resumen_final(self):
        """Muestra un resumen de todos los resultados"""
        if not self.resultados_totales:
            return
            
        resumen_texto = "RESUMEN FINAL - TODAS LAS PRUEBAS\n\n"
        
        for prueba, resultados in self.resultados_totales.items():
            nombre_prueba = self.pruebas[prueba]['nombre']
            resumen_texto += f"{nombre_prueba}:\n"
            
            if isinstance(resultados, dict):
                for key, value in resultados.items():
                    if isinstance(value, (int, float)):
                        resumen_texto += f"  • {key}: {value}\n"
            else:
                resumen_texto += f"  • Resultado: {resultados}\n"
            
            resumen_texto += "\n"
        
        resumen_texto += "Presione ESPACIO para volver al menú principal..."
        
        texto_resumen = visual.TextStim(self.win, text=resumen_texto, 
                                      height=20, color='white', wrapWidth=1000)
        texto_resumen.draw()
        self.win.flip()
        event.waitKeys(keyList=['space'])
    
    def ejecutar_sistema(self):
        """Ejecuta el sistema completo"""
        try:
            self.obtener_datos_participante()
            
            if self.datos_participante['modalidad'] == 'Secuencia Completa':
                self.ejecutar_secuencia_completa()
            else:
                self.menu_principal()
                
        except Exception as e:
            print(f"Error en el sistema: {e}")
        finally:
            self.win.close()
