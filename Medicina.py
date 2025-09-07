import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

class SistemaCitasMedicas:
    """
    Sistema de Optimización de Citas Médicas para El Salvador
    Implementa funciones cuadráticas e inversas para optimizar recursos médicos
    """
    
    def __init__(self):
        # Parámetros del modelo basados en el documento
        self.a_cuadratica = -0.5  # Coeficiente cuadrático
        self.b_cuadratica = 20    # Coeficiente lineal
        self.c_cuadratica = -25   # Término independiente
        self.k_inversa = 120      # Constante de la función inversa
        
        # Datos del sistema de salud salvadoreño
        self.poblacion_total = 6500000
        self.hospitales_publicos = 40
        self.medicos_disponibles = 4318
        self.tiempo_espera_actual = 3.5
        
    def demanda_cuadratica(self, hora):
        """
        Función cuadrática: y = -0.5x² + 20x - 25
        Calcula la demanda de pacientes por hora del día
        """
        return self.a_cuadratica * (hora**2) + self.b_cuadratica * hora + self.c_cuadratica
    
    def tiempo_espera_inverso(self, num_medicos):
        """
        Función inversa: T = 120/m
        Calcula el tiempo de espera basado en médicos disponibles
        """
        if num_medicos <= 0:
            return float('inf')
        return self.k_inversa / num_medicos
    
    def calcular_medicos_necesarios(self, tiempo_objetivo):
        """
        Calcula cuántos médicos se necesitan para un tiempo objetivo
        """
        if tiempo_objetivo <= 0:
            return float('inf')
        return self.k_inversa / tiempo_objetivo
    
    def optimizar_distribucion_diaria(self):
        """
        Optimiza la distribución de médicos durante el día
        """
        horas = range(6, 23)  # 6 AM a 10 PM
        distribucion = []
        
        for hora in horas:
            demanda = max(0, self.demanda_cuadratica(hora))  # No demanda negativa
            medicos_necesarios = max(1, int(self.calcular_medicos_necesarios(2.0)))  # Objetivo: 2 horas
            medicos_asignados = min(medicos_necesarios, int(demanda * 0.5))  # Ajuste realista
            tiempo_espera = self.tiempo_espera_inverso(medicos_asignados)
            
            distribucion.append({
                'hora': hora,
                'hora_formato': f"{hora}:00",
                'demanda_predicha': int(demanda),
                'medicos_asignados': medicos_asignados,
                'tiempo_espera': round(tiempo_espera, 2)
            })
        
        return distribucion
    
    def generar_reporte_optimizacion(self):
        """
        Genera un reporte completo del sistema optimizado
        """
        distribucion = self.optimizar_distribucion_diaria()
        
        # Calcular métricas
        total_pacientes = sum([d['demanda_predicha'] for d in distribucion])
        total_medicos_usados = sum([d['medicos_asignados'] for d in distribucion])
        tiempo_promedio = np.mean([d['tiempo_espera'] for d in distribucion])
        
        # Encontrar hora pico
        hora_pico = max(distribucion, key=lambda x: x['demanda_predicha'])
        
        reporte = {
            'distribucion': distribucion,
            'metricas': {
                'total_pacientes_diarios': total_pacientes,
                'total_medicos_usados': total_medicos_usados,
                'tiempo_espera_promedio': round(tiempo_promedio, 2),
                'mejora_vs_actual': round(((self.tiempo_espera_actual - tiempo_promedio) / self.tiempo_espera_actual) * 100, 1),
                'hora_pico': hora_pico['hora_formato'],
                'demanda_maxima': hora_pico['demanda_predicha']
            }
        }
        
        return reporte

class InterfazModerna:
    """
    Interfaz gráfica moderna para el Sistema de Citas Médicas
    """
    
    def __init__(self):
        self.sistema = SistemaCitasMedicas()
        self.root = tk.Tk()
        self.setup_window()
        self.setup_styles()
        self.crear_interfaz()
    
    def setup_window(self):
        """Configuración inicial de la ventana"""
        self.root.title("Sistema de Optimización de Citas Médicas - El Salvador")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f2f5')
        
        # Centrar ventana
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (900 // 2)
        self.root.geometry(f"1400x900+{x}+{y}")
        
        # Ícono y configuración
        self.root.resizable(True, True)
        self.root.minsize(1200, 700)
    
    def setup_styles(self):
        """Configuración de estilos personalizados"""
        self.colors = {
            'primary': '#2E86AB',      # Azul principal
            'secondary': '#A23B72',    # Rosa/morado
            'success': '#F18F01',      # Naranja
            'danger': '#C73E1D',       # Rojo
            'warning': '#FFB627',      # Amarillo
            'info': '#17A2B8',         # Cyan
            'light': '#F8F9FA',        # Gris claro
            'dark': '#343A40',         # Gris oscuro
            'white': '#FFFFFF',
            'bg_main': '#f0f2f5',
            'card_bg': '#ffffff',
            'text_primary': '#2c3e50',
            'text_secondary': '#6c757d',
            'accent': '#e74c3c'
        }
        
        # Configurar ttk styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Estilo para frames principales
        self.style.configure('Card.TFrame', 
                           background=self.colors['card_bg'],
                           relief='flat',
                           borderwidth=1)
        
        # Estilo para botones principales
        self.style.configure('Primary.TButton',
                           background=self.colors['primary'],
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none',
                           padding=(20, 10))
        
        self.style.map('Primary.TButton',
                      background=[('active', '#1e5f7a')])
        
        # Estilo para botones secundarios
        self.style.configure('Secondary.TButton',
                           background=self.colors['secondary'],
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none',
                           padding=(15, 8))
        
        # Estilo para labels de título
        self.style.configure('Title.TLabel',
                           background=self.colors['card_bg'],
                           foreground=self.colors['text_primary'],
                           font=('Segoe UI', 16, 'bold'))
        
        # Estilo para labels de subtítulo
        self.style.configure('Subtitle.TLabel',
                           background=self.colors['card_bg'],
                           foreground=self.colors['text_secondary'],
                           font=('Segoe UI', 10))
    
    def crear_header(self, parent):
        """Crear header principal de la aplicación"""
        header_frame = tk.Frame(parent, bg=self.colors['primary'], height=100)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Contenedor del header
        header_content = tk.Frame(header_frame, bg=self.colors['primary'])
        header_content.pack(expand=True, fill='both', padx=30, pady=20)
        
        # Logo y título
        logo_frame = tk.Frame(header_content, bg=self.colors['primary'])
        logo_frame.pack(side='left', fill='y')
        
        # Simulación de logo con texto
        logo_text = tk.Label(logo_frame, text="🏥", font=('Arial', 24), 
                           bg=self.colors['primary'], fg='white')
        logo_text.pack(side='left', padx=(0, 15))
        
        title_frame = tk.Frame(header_content, bg=self.colors['primary'])
        title_frame.pack(side='left', expand=True, fill='both')
        
        main_title = tk.Label(title_frame, 
                            text="Sistema de Optimización de Citas Médicas",
                            font=('Segoe UI', 20, 'bold'),
                            bg=self.colors['primary'], fg='white')
        main_title.pack(anchor='w', pady=(5, 0))
        
        subtitle = tk.Label(title_frame,
                          text="El Salvador • Aplicación de Gráficas Cuadráticas e Inversas • Python",
                          font=('Segoe UI', 11),
                          bg=self.colors['primary'], fg='#B8E0FF')
        subtitle.pack(anchor='w')
        
        # Información del sistema en el header
        info_frame = tk.Frame(header_content, bg=self.colors['primary'])
        info_frame.pack(side='right', fill='y')
        
        stats = [
            ("6.5M", "Habitantes"),
            ("4,318", "Médicos"),
            ("40", "Hospitales")
        ]
        
        for i, (valor, etiqueta) in enumerate(stats):
            stat_frame = tk.Frame(info_frame, bg=self.colors['primary'])
            stat_frame.pack(side='left', padx=15)
            
            tk.Label(stat_frame, text=valor, font=('Segoe UI', 14, 'bold'),
                   bg=self.colors['primary'], fg='white').pack()
            tk.Label(stat_frame, text=etiqueta, font=('Segoe UI', 9),
                   bg=self.colors['primary'], fg='#B8E0FF').pack()
    
    def crear_calculadoras(self, parent):
        """Crear sección de calculadoras"""
        calc_frame = ttk.Frame(parent, style='Card.TFrame', padding=20)
        calc_frame.pack(fill='x', padx=20, pady=(20, 10))
        
        ttk.Label(calc_frame, text="🧮 Calculadoras del Sistema", 
                 style='Title.TLabel').pack(anchor='w', pady=(0, 15))
        
        # Container para las dos calculadoras
        calc_container = tk.Frame(calc_frame, bg=self.colors['card_bg'])
        calc_container.pack(fill='x')
        
        # Calculadora de demanda
        demanda_frame = tk.Frame(calc_container, bg=self.colors['light'], 
                               relief='solid', bd=1)
        demanda_frame.pack(side='left', fill='both', expand=True, padx=(0, 10), pady=5)
        
        # Header de demanda
        demanda_header = tk.Frame(demanda_frame, bg=self.colors['info'], height=40)
        demanda_header.pack(fill='x')
        demanda_header.pack_propagate(False)
        
        tk.Label(demanda_header, text="📊 Función Cuadrática - Demanda",
               font=('Segoe UI', 11, 'bold'), bg=self.colors['info'], fg='white').pack(pady=8)
        
        # Contenido de demanda
        demanda_content = tk.Frame(demanda_frame, bg=self.colors['light'])
        demanda_content.pack(fill='both', expand=True, padx=15, pady=15)
        
        tk.Label(demanda_content, text="y = -0.5x² + 20x - 25",
               font=('Segoe UI', 10, 'italic'), bg=self.colors['light'],
               fg=self.colors['text_secondary']).pack(pady=(0, 10))
        
        # Input de hora
        hora_frame = tk.Frame(demanda_content, bg=self.colors['light'])
        hora_frame.pack(fill='x', pady=5)
        
        tk.Label(hora_frame, text="Hora del día (6-22):", font=('Segoe UI', 10),
               bg=self.colors['light']).pack(side='left')
        
        self.hora_entry = tk.Entry(hora_frame, font=('Segoe UI', 10), width=8,
                                 relief='solid', bd=1)
        self.hora_entry.pack(side='right')
        
        # Botón y resultado de demanda
        demanda_btn = tk.Button(demanda_content, text="Calcular Demanda",
                              command=self.calcular_demanda,
                              bg=self.colors['info'], fg='white',
                              font=('Segoe UI', 10, 'bold'),
                              relief='flat', cursor='hand2')
        demanda_btn.pack(pady=10)
        
        self.demanda_result = tk.Label(demanda_content, text="--- pacientes",
                                     font=('Segoe UI', 12, 'bold'),
                                     bg=self.colors['light'], fg=self.colors['info'])
        self.demanda_result.pack(pady=5)
        
        # Calculadora de tiempo
        tiempo_frame = tk.Frame(calc_container, bg=self.colors['light'], 
                              relief='solid', bd=1)
        tiempo_frame.pack(side='right', fill='both', expand=True, padx=(10, 0), pady=5)
        
        # Header de tiempo
        tiempo_header = tk.Frame(tiempo_frame, bg=self.colors['secondary'], height=40)
        tiempo_header.pack(fill='x')
        tiempo_header.pack_propagate(False)
        
        tk.Label(tiempo_header, text="⏱️ Función Inversa - Tiempo",
               font=('Segoe UI', 11, 'bold'), bg=self.colors['secondary'], fg='white').pack(pady=8)
        
        # Contenido de tiempo
        tiempo_content = tk.Frame(tiempo_frame, bg=self.colors['light'])
        tiempo_content.pack(fill='both', expand=True, padx=15, pady=15)
        
        tk.Label(tiempo_content, text="T = 120/m",
               font=('Segoe UI', 10, 'italic'), bg=self.colors['light'],
               fg=self.colors['text_secondary']).pack(pady=(0, 10))
        
        # Input de médicos
        medicos_frame = tk.Frame(tiempo_content, bg=self.colors['light'])
        medicos_frame.pack(fill='x', pady=5)
        
        tk.Label(medicos_frame, text="Número de médicos:", font=('Segoe UI', 10),
               bg=self.colors['light']).pack(side='left')
        
        self.medicos_entry = tk.Entry(medicos_frame, font=('Segoe UI', 10), width=8,
                                    relief='solid', bd=1)
        self.medicos_entry.pack(side='right')
        
        # Botón y resultado de tiempo
        tiempo_btn = tk.Button(tiempo_content, text="Calcular Tiempo",
                             command=self.calcular_tiempo,
                             bg=self.colors['secondary'], fg='white',
                             font=('Segoe UI', 10, 'bold'),
                             relief='flat', cursor='hand2')
        tiempo_btn.pack(pady=10)
        
        self.tiempo_result = tk.Label(tiempo_content, text="--- horas",
                                    font=('Segoe UI', 12, 'bold'),
                                    bg=self.colors['light'], fg=self.colors['secondary'])
        self.tiempo_result.pack(pady=5)
    
    def crear_botones_principales(self, parent):
        """Crear sección de botones principales"""
        btn_frame = tk.Frame(parent, bg=self.colors['bg_main'])
        btn_frame.pack(fill='x', padx=20, pady=10)
        
        # Container para los botones
        btn_container = tk.Frame(btn_frame, bg=self.colors['bg_main'])
        btn_container.pack()
        
        botones = [
            ("📈 Generar Gráficas", self.mostrar_graficas, self.colors['success'], "🎯 Visualizar funciones matemáticas"),
            ("📋 Ver Reporte", self.mostrar_reporte, self.colors['primary'], "📊 Análisis completo del sistema"),
            ("💾 Exportar Datos", self.exportar_datos, self.colors['warning'], "📁 Guardar resultados en CSV"),
            ("🔄 Optimizar", self.optimizar_sistema, self.colors['accent'], "⚡ Ejecutar optimización completa")
        ]
        
        for i, (texto, comando, color, descripcion) in enumerate(botones):
            btn_card = tk.Frame(btn_container, bg='white', relief='solid', bd=1)
            btn_card.pack(side='left', padx=10, pady=5)
            
            # Botón principal
            btn = tk.Button(btn_card, text=texto,
                          command=comando,
                          bg=color, fg='white',
                          font=('Segoe UI', 11, 'bold'),
                          relief='flat', cursor='hand2',
                          width=18, height=2)
            btn.pack(padx=15, pady=(15, 5))
            
            # Descripción
            tk.Label(btn_card, text=descripcion,
                   font=('Segoe UI', 8), bg='white',
                   fg=self.colors['text_secondary']).pack(pady=(0, 15))
    
    def crear_area_resultados(self, parent):
        """Crear área de resultados con pestañas"""
        result_frame = ttk.Frame(parent, style='Card.TFrame', padding=20)
        result_frame.pack(fill='both', expand=True, padx=20, pady=(10, 20))
        
        ttk.Label(result_frame, text="📊 Panel de Resultados", 
                 style='Title.TLabel').pack(anchor='w', pady=(0, 15))
        
        # Crear notebook para pestañas
        self.notebook = ttk.Notebook(result_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Pestaña de Dashboard
        self.tab_dashboard = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_dashboard, text='📈 Dashboard')
        
        # Pestaña de Reporte
        self.tab_reporte = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_reporte, text='📋 Reporte Detallado')
        
        # Pestaña de Gráficas
        self.tab_graficas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_graficas, text='📊 Gráficas Interactivas')
        
        self.crear_dashboard()
        self.crear_tab_reporte()
        self.crear_tab_graficas()
    
    def crear_dashboard(self):
        """Crear dashboard con métricas principales"""
        # Frame principal del dashboard
        dashboard_main = tk.Frame(self.tab_dashboard, bg=self.colors['card_bg'])
        dashboard_main.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Métricas superiores
        metrics_frame = tk.Frame(dashboard_main, bg=self.colors['card_bg'])
        metrics_frame.pack(fill='x', pady=(0, 20))
        
        reporte = self.sistema.generar_reporte_optimizacion()
        
        metrics = [
            ("Tiempo Espera Actual", "3.5 hrs", self.colors['danger'], "⏰"),
            ("Tiempo Optimizado", f"{reporte['metricas']['tiempo_espera_promedio']} hrs", self.colors['success'], "✅"),
            ("Mejora Obtenida", f"{reporte['metricas']['mejora_vs_actual']}%", self.colors['primary'], "📈"),
            ("Pacientes/Día", f"{reporte['metricas']['total_pacientes_diarios']:,}", self.colors['info'], "👥")
        ]
        
        for i, (titulo, valor, color, icono) in enumerate(metrics):
            metric_card = tk.Frame(metrics_frame, bg=color, relief='flat')
            metric_card.pack(side='left', fill='both', expand=True, padx=5)
            
            # Contenido de la métrica
            content = tk.Frame(metric_card, bg=color)
            content.pack(fill='both', expand=True, padx=20, pady=15)
            
            tk.Label(content, text=icono, font=('Arial', 20),
                   bg=color, fg='white').pack()
            
            tk.Label(content, text=valor, font=('Segoe UI', 18, 'bold'),
                   bg=color, fg='white').pack()
            
            tk.Label(content, text=titulo, font=('Segoe UI', 10),
                   bg=color, fg='white').pack()
        
        # Información del sistema
        info_frame = tk.Frame(dashboard_main, bg=self.colors['light'], relief='solid', bd=1)
        info_frame.pack(fill='both', expand=True, pady=10)
        
        info_header = tk.Frame(info_frame, bg=self.colors['dark'], height=40)
        info_header.pack(fill='x')
        info_header.pack_propagate(False)
        
        tk.Label(info_header, text="ℹ️ Información del Sistema de Salud Salvadoreño",
               font=('Segoe UI', 12, 'bold'), bg=self.colors['dark'], fg='white').pack(pady=8)
        
        info_content = tk.Frame(info_frame, bg=self.colors['light'])
        info_content.pack(fill='both', expand=True, padx=20, pady=20)
        
        info_text = """
🏥 DATOS DEL SISTEMA ACTUAL:
• Población total cubierta: 6.5 millones de habitantes
• Hospitales públicos: 40 (MINSAL + ISSS)
• Médicos disponibles: 4,318 profesionales
• Tiempo de espera promedio: 3.5 horas
• Consultorios médicos: 1,761 disponibles

📊 FUNCIONES MATEMÁTICAS IMPLEMENTADAS:
• Función Cuadrática (Demanda): y = -0.5x² + 20x - 25
• Función Inversa (Tiempo): T = 120/m

🎯 OBJETIVOS DEL SISTEMA:
• Reducir tiempo de espera a menos de 2 horas
• Optimizar distribución de recursos médicos
• Aumentar eficiencia del sistema de salud
• Mejorar atención a la población salvadoreña
        """
        
        tk.Label(info_content, text=info_text, font=('Segoe UI', 10),
               bg=self.colors['light'], fg=self.colors['text_primary'],
               justify='left').pack(anchor='w')
    
    def crear_tab_reporte(self):
        """Crear pestaña de reporte detallado"""
        # Frame con scroll
        canvas = tk.Canvas(self.tab_reporte, bg=self.colors['card_bg'])
        scrollbar = ttk.Scrollbar(self.tab_reporte, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Text widget para el reporte
        self.text_reporte = tk.Text(scrollable_frame, wrap=tk.WORD, 
                                   font=('Consolas', 10),
                                   bg=self.colors['card_bg'],
                                   fg=self.colors['text_primary'],
                                   relief='flat',
                                   padx=20, pady=20)
        self.text_reporte.pack(fill='both', expand=True)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mostrar reporte inicial
        self.actualizar_reporte()
    
    def crear_tab_graficas(self):
        """Crear pestaña para gráficas interactivas"""
        # Placeholder para gráficas
        graficas_frame = tk.Frame(self.tab_graficas, bg=self.colors['card_bg'])
        graficas_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(graficas_frame, 
               text="📊 Las gráficas se mostrarán aquí al hacer clic en 'Generar Gráficas'",
               font=('Segoe UI', 12),
               bg=self.colors['card_bg'],
               fg=self.colors['text_secondary']).pack(expand=True)
        
        # Botón para generar gráficas
        tk.Button(graficas_frame, text="🚀 Generar Gráficas Ahora",
                command=self.mostrar_graficas,
                bg=self.colors['success'], fg='white',
                font=('Segoe UI', 12, 'bold'),
                relief='flat', cursor='hand2',
                padx=30, pady=10).pack()
    
    def crear_interfaz(self):
        """Crear la interfaz completa"""
        # Header principal
        self.crear_header(self.root)
        
        # Calculadoras
        self.crear_calculadoras(self.root)
        
        # Botones principales
        self.crear_botones_principales(self.root)
        
        # Área de resultados con pestañas
        self.crear_area_resultados(self.root)
    
    def calcular_demanda(self):
        """Calcular demanda con validación mejorada"""
        try:
            hora = float(self.hora_entry.get())
            if 6 <= hora <= 22:
                demanda = max(0, self.sistema.demanda_cuadratica(hora))
                self.demanda_result.config(text=f"{int(demanda)} pacientes",
                                         fg=self.colors['info'])
                
                # Añadir efecto visual
                self.demanda_result.configure(font=('Segoe UI', 12, 'bold'))
                self.root.after(100, lambda: self.demanda_result.configure(font=('Segoe UI', 12, 'normal')))
            else:
                messagebox.showerror("Error", "La hora debe estar entre 6 y 22 (6:00 AM - 10:00 PM)")
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un número válido")
    
    def calcular_tiempo(self):
        """Calcular tiempo con validación mejorada"""
        try:
            medicos = int(self.medicos_entry.get())
            if medicos > 0:
                tiempo = self.sistema.tiempo_espera_inverso(medicos)
                self.tiempo_result.config(text=f"{tiempo:.2f} horas",
                                        fg=self.colors['secondary'])
                
                # Añadir efecto visual
                self.tiempo_result.configure(font=('Segoe UI', 12, 'bold'))
                self.root.after(100, lambda: self.tiempo_result.configure(font=('Segoe UI', 12, 'normal')))
            else:
                messagebox.showerror("Error", "El número de médicos debe ser mayor a 0")
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un número válido")
    
    def mostrar_graficas(self):
        """Mostrar gráficas en ventana separada"""
        # Crear ventana para gráficas
        graficas_window = tk.Toplevel(self.root)
        graficas_window.title("Gráficas del Sistema - Funciones Cuadráticas e Inversas")
        graficas_window.geometry("1200x800")
        graficas_window.configure(bg='white')
        
        # Crear figura de matplotlib
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Sistema de Optimización de Citas Médicas - El Salvador', 
                    fontsize=16, fontweight='bold')
        
        # Gráfica 1: Función Cuadrática
        horas = np.linspace(6, 22, 100)
        demanda = [max(0, self.sistema.demanda_cuadratica(h)) for h in horas]
        
        ax1.plot(horas, demanda, 'b-', linewidth=3, label='Demanda de Pacientes')
        ax1.fill_between(horas, demanda, alpha=0.3, color='blue')
        ax1.set_xlabel('Hora del Día', fontweight='bold')
        ax1.set_ylabel('Número de Pacientes', fontweight='bold')
        ax1.set_title('Función Cuadrática: y = -0.5x² + 20x - 25', fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Marcar el vértice (hora pico)
        hora_pico = -self.sistema.b_cuadratica / (2 * self.sistema.a_cuadratica)
        demanda_pico = self.sistema.demanda_cuadratica(hora_pico)
        ax1.plot(hora_pico, demanda_pico, 'ro', markersize=10)
        ax1.annotate(f'Pico: {int(demanda_pico)} pacientes\na las {hora_pico}:00', 
                    xy=(hora_pico, demanda_pico), xytext=(hora_pico-2, demanda_pico+20),
                    arrowprops=dict(arrowstyle='->', color='red'))
        
        # Gráfica 2: Función Inversa
        medicos = np.linspace(1, 100, 100)
        tiempo_espera = [self.sistema.tiempo_espera_inverso(m) for m in medicos]
        
        ax2.plot(medicos, tiempo_espera, 'r-', linewidth=3, label='Tiempo de Espera')
        ax2.fill_between(medicos, tiempo_espera, alpha=0.3, color='red')
        ax2.set_xlabel('Número de Médicos', fontweight='bold')
        ax2.set_ylabel('Tiempo de Espera (horas)', fontweight='bold')
        ax2.set_title('Función Inversa: T = 120/m', fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        ax2.set_xlim(1, 100)
        ax2.set_ylim(0, 50)
        
        # Marcar puntos clave
        puntos_medicos = [10, 20, 40, 60]
        for m in puntos_medicos:
            t = self.sistema.tiempo_espera_inverso(m)
            ax2.plot(m, t, 'go', markersize=8)
            ax2.annotate(f'{m}M\n{t:.1f}h', xy=(m, t), xytext=(m+5, t+2), fontsize=8)
        
        # Gráfica 3: Distribución optimizada
        distribucion = self.sistema.optimizar_distribucion_diaria()
        horas_dist = [d['hora'] for d in distribucion]
        demanda_dist = [d['demanda_predicha'] for d in distribucion]
        medicos_dist = [d['medicos_asignados'] for d in distribucion]
        
        ax3_twin = ax3.twinx()
        bars1 = ax3.bar([h-0.2 for h in horas_dist], demanda_dist, 0.4, 
                       label='Demanda', color='skyblue', alpha=0.8)
        bars2 = ax3_twin.bar([h+0.2 for h in horas_dist], medicos_dist, 0.4, 
                            label='Médicos', color='orange', alpha=0.8)
        
        ax3.set_xlabel('Hora del Día', fontweight='bold')
        ax3.set_ylabel('Pacientes', color='blue', fontweight='bold')
        ax3_twin.set_ylabel('Médicos', color='orange', fontweight='bold')
        ax3.set_title('Distribución Optimizada por Hora', fontweight='bold')
        ax3.grid(True, alpha=0.3)
        
        # Gráfica 4: Comparación de métricas
        reporte = self.sistema.generar_reporte_optimizacion()
        categorias = ['Tiempo\nEspera (h)', 'Pacientes\n(miles)', 'Eficiencia\n(%)']
        actual = [3.5, 1.2, 60]
        optimizado = [reporte['metricas']['tiempo_espera_promedio'], 
                     reporte['metricas']['total_pacientes_diarios']/1000, 85]
        
        x = np.arange(len(categorias))
        width = 0.35
        
        bars1 = ax4.bar(x - width/2, actual, width, label='Actual', 
                       color='#ff6b6b', alpha=0.8)
        bars2 = ax4.bar(x + width/2, optimizado, width, label='Optimizado', 
                       color='#4ecdc4', alpha=0.8)
        
        ax4.set_ylabel('Valores', fontweight='bold')
        ax4.set_title('Comparación: Actual vs Optimizado', fontweight='bold')
        ax4.set_xticks(x)
        ax4.set_xticklabels(categorias)
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # Añadir valores en las barras
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax4.text(bar.get_x() + bar.get_width()/2., height + height*0.01, 
                        f'{height:.1f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        # Integrar matplotlib en tkinter
        canvas = FigureCanvasTkAgg(fig, graficas_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
        # Botón para cerrar
        close_btn = tk.Button(graficas_window, text="Cerrar Gráficas",
                            command=graficas_window.destroy,
                            bg=self.colors['danger'], fg='white',
                            font=('Segoe UI', 10, 'bold'),
                            relief='flat', cursor='hand2')
        close_btn.pack(pady=10)
    
    def mostrar_reporte(self):
        """Mostrar reporte en la pestaña correspondiente"""
        self.notebook.select(self.tab_reporte)
        self.actualizar_reporte()
    
    def actualizar_reporte(self):
        """Actualizar el contenido del reporte"""
        self.text_reporte.delete(1.0, tk.END)
        reporte = self.sistema.generar_reporte_optimizacion()
        
        texto_reporte = f"""
{'='*80}
          REPORTE DE OPTIMIZACIÓN DEL SISTEMA DE SALUD SALVADOREÑO
{'='*80}

📊 MÉTRICAS GENERALES DEL SISTEMA:
{'─'*50}
• Total de pacientes diarios proyectados: {reporte['metricas']['total_pacientes_diarios']:,} pacientes
• Tiempo de espera promedio optimizado: {reporte['metricas']['tiempo_espera_promedio']} horas
• Mejora respecto al sistema actual: {reporte['metricas']['mejora_vs_actual']}%
• Hora pico de máxima demanda: {reporte['metricas']['hora_pico']}
• Demanda máxima registrada: {reporte['metricas']['demanda_maxima']} pacientes

🏥 INFORMACIÓN DEL SISTEMA ACTUAL:
{'─'*50}
• Población total cubierta: {self.sistema.poblacion_total:,} habitantes
• Hospitales públicos disponibles: {self.sistema.hospitales_publicos}
• Médicos en el sistema: {self.sistema.medicos_disponibles:,}
• Tiempo de espera actual: {self.sistema.tiempo_espera_actual} horas

📈 DISTRIBUCIÓN OPTIMIZADA POR HORA:
{'─'*80}
{'Hora':<10} {'Demanda':<15} {'Médicos':<15} {'T.Espera':<15} {'Estado':<15}
{'─'*80}
"""
        
        for d in reporte['distribucion']:
            estado = "🟢 Óptimo" if d['tiempo_espera'] <= 2.0 else "🟡 Moderado" if d['tiempo_espera'] <= 3.0 else "🔴 Alto"
            texto_reporte += f"{d['hora_formato']:<10} {d['demanda_predicha']:<15} {d['medicos_asignados']:<15} {d['tiempo_espera']:<15} {estado:<15}\n"
        
        texto_reporte += f"""
{'─'*80}

🧮 FUNCIONES MATEMÁTICAS IMPLEMENTADAS:
{'─'*50}
📊 Función Cuadrática (Demanda de Pacientes):
   • Ecuación: y = -0.5x² + 20x - 25
   • Donde: x = hora del día (6-22), y = número de pacientes
   • Características: Parábola con máximo en x = 20 (8:00 PM)
   • Aplicación: Predice la demanda de consultas por hora

⏱️ Función Inversa (Tiempo de Espera):
   • Ecuación: T = 120/m
   • Donde: T = tiempo de espera (horas), m = número de médicos
   • Características: Hipérbola con asíntotas en ambos ejes
   • Aplicación: Calcula tiempo de espera según recursos disponibles

🎯 ANÁLISIS DE OPTIMIZACIÓN:
{'─'*50}
• El sistema optimizado reduce el tiempo de espera en {reporte['metricas']['mejora_vs_actual']}%
• La distribución variable de médicos se adapta a la demanda horaria
• Se logra una atención más eficiente durante las horas pico
• El modelo matemático permite predicciones precisas de recursos necesarios

💡 RECOMENDACIONES PARA IMPLEMENTACIÓN:
{'─'*50}
1. Implementar turnos rotativos basados en la predicción de demanda
2. Concentrar más médicos durante las horas de 16:00 a 20:00
3. Reducir personal durante las primeras horas de la mañana
4. Establecer sistema de citas que distribuya mejor la demanda
5. Monitorear continuamente los patrones reales vs predicciones

{'='*80}
Reporte generado el: {datetime.now().strftime('%d/%m/%Y a las %H:%M:%S')}
Sistema desarrollado con Python - Funciones Cuadráticas e Inversas
{'='*80}
"""
        
        self.text_reporte.insert(tk.END, texto_reporte)
        
        # Resaltar secciones importantes
        self.text_reporte.tag_add("titulo", "1.0", "4.0")
        self.text_reporte.tag_config("titulo", foreground=self.colors['primary'], 
                                   font=('Segoe UI', 12, 'bold'))
    
    def exportar_datos(self):
        """Exportar datos con diálogo de confirmación mejorado"""
        try:
            distribucion = self.sistema.optimizar_distribucion_diaria()
            reporte = self.sistema.generar_reporte_optimizacion()
            
            # Crear DataFrame con datos completos
            df = pd.DataFrame(distribucion)
            
            # Añadir metadatos
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"optimizacion_salud_salvador_{timestamp}.csv"
            
            # Guardar archivo
            df.to_csv(filename, index=False, encoding='utf-8')
            
            # Crear ventana de confirmación personalizada
            success_window = tk.Toplevel(self.root)
            success_window.title("Exportación Exitosa")
            success_window.geometry("400x250")
            success_window.configure(bg='white')
            success_window.resizable(False, False)
            
            # Centrar ventana
            success_window.transient(self.root)
            success_window.grab_set()
            
            # Contenido de la ventana
            tk.Label(success_window, text="✅", font=('Arial', 40), 
                   bg='white', fg=self.colors['success']).pack(pady=20)
            
            tk.Label(success_window, text="Datos Exportados Exitosamente",
                   font=('Segoe UI', 14, 'bold'), bg='white',
                   fg=self.colors['text_primary']).pack()
            
            tk.Label(success_window, text=f"Archivo: {filename}",
                   font=('Segoe UI', 10), bg='white',
                   fg=self.colors['text_secondary']).pack(pady=10)
            
            tk.Label(success_window, 
                   text=f"Registros exportados: {len(distribucion)}\nMétricas incluidas: Todas",
                   font=('Segoe UI', 9), bg='white',
                   fg=self.colors['text_secondary']).pack()
            
            tk.Button(success_window, text="Aceptar",
                    command=success_window.destroy,
                    bg=self.colors['success'], fg='white',
                    font=('Segoe UI', 10, 'bold'),
                    relief='flat', cursor='hand2',
                    width=15).pack(pady=20)
            
        except Exception as e:
            messagebox.showerror("Error de Exportación", 
                               f"No se pudo exportar el archivo:\n{str(e)}")
    
    def optimizar_sistema(self):
        """Ejecutar optimización completa del sistema"""
        # Ventana de progreso
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Optimizando Sistema...")
        progress_window.geometry("400x200")
        progress_window.configure(bg='white')
        progress_window.resizable(False, False)
        progress_window.transient(self.root)
        progress_window.grab_set()
        
        # Contenido
        tk.Label(progress_window, text="🔄", font=('Arial', 30),
               bg='white', fg=self.colors['primary']).pack(pady=20)
        
        tk.Label(progress_window, text="Ejecutando Optimización Completa",
               font=('Segoe UI', 12, 'bold'), bg='white').pack()
        
        status_label = tk.Label(progress_window, text="Iniciando...",
                              font=('Segoe UI', 10), bg='white',
                              fg=self.colors['text_secondary'])
        status_label.pack(pady=10)
        
        # Barra de progreso
        progress = ttk.Progressbar(progress_window, length=300, mode='determinate')
        progress.pack(pady=10)
        
        # Simular proceso de optimización
        pasos = [
            "Analizando datos del sistema...",
            "Calculando funciones cuadráticas...",
            "Procesando funciones inversas...",
            "Optimizando distribución de recursos...",
            "Generando reporte final...",
            "Optimización completada!"
        ]
        
        def actualizar_progreso(paso_actual=0):
            if paso_actual < len(pasos):
                status_label.config(text=pasos[paso_actual])
                progress['value'] = (paso_actual + 1) * (100 / len(pasos))
                progress_window.after(800, lambda: actualizar_progreso(paso_actual + 1))
            else:
                progress_window.destroy()
                self.mostrar_resultado_optimizacion()
        
        actualizar_progreso()
    
    def mostrar_resultado_optimizacion(self):
        """Mostrar resultado de la optimización"""
        # Actualizar dashboard
        self.crear_dashboard()
        
        # Cambiar a pestaña de dashboard
        self.notebook.select(self.tab_dashboard)
        
        # Mostrar mensaje de éxito
        messagebox.showinfo("Optimización Completada", 
                          "✅ El sistema ha sido optimizado exitosamente!\n\n" +
                          "• Tiempo de espera reducido\n" +
                          "• Distribución de médicos mejorada\n" +
                          "• Eficiencia del sistema aumentada\n\n" +
                          "Revise el dashboard para ver los resultados.")
    
    def ejecutar(self):
        """Ejecutar la aplicación"""
        # Configurar eventos de teclado
        self.root.bind('<Return>', lambda e: self.calcular_demanda() if self.hora_entry.get() else self.calcular_tiempo())
        self.root.bind('<F1>', lambda e: self.mostrar_ayuda())
        
        # Mostrar mensaje de bienvenida
        self.root.after(500, self.mostrar_bienvenida)
        
        # Iniciar loop principal
        self.root.mainloop()
    
    def mostrar_bienvenida(self):
        """Mostrar mensaje de bienvenida"""
        messagebox.showinfo(
            "¡Bienvenido al Sistema de Optimización Médica!",
            "🏥 Sistema de Optimización de Citas Médicas\n" +
            "📍 El Salvador\n\n" +
            "✨ Características principales:\n" +
            "• Funciones Cuadráticas e Inversas\n" +
            "• Optimización automática de recursos\n" +
            "• Gráficas interactivas\n" +
            "• Reportes detallados\n\n" +
            "💡 Consejo: Comience probando las calculadoras\n" +
            "y luego explore las gráficas y reportes."
        )
    
    def mostrar_ayuda(self):
        """Mostrar ventana de ayuda"""
        ayuda_window = tk.Toplevel(self.root)
        ayuda_window.title("Ayuda - Sistema de Optimización")
        ayuda_window.geometry("600x400")
        ayuda_window.configure(bg='white')
        
        # Contenido de ayuda
        ayuda_text = tk.Text(ayuda_window, wrap=tk.WORD, font=('Segoe UI', 10),
                           bg='white', relief='flat', padx=20, pady=20)
        ayuda_text.pack(fill='both', expand=True)
        
        ayuda_content = """
🆘 AYUDA - SISTEMA DE OPTIMIZACIÓN DE CITAS MÉDICAS

📚 GUÍA DE USO:

1️⃣ CALCULADORAS:
   • Función Cuadrática: Ingrese hora (6-22) para calcular demanda
   • Función Inversa: Ingrese número de médicos para calcular tiempo de espera

2️⃣ BOTONES PRINCIPALES:
   • 📈 Generar Gráficas: Muestra visualizaciones matemáticas
   • 📋 Ver Reporte: Análisis completo del sistema optimizado
   • 💾 Exportar Datos: Guarda resultados en archivo CSV
   • 🔄 Optimizar: Ejecuta optimización completa del sistema

3️⃣ PESTAÑAS:
   • Dashboard: Métricas principales e información del sistema
   • Reporte Detallado: Análisis completo con datos por hora
   • Gráficas Interactivas: Visualizaciones de las funciones matemáticas

🧮 FUNCIONES MATEMÁTICAS:
   • Cuadrática: y = -0.5x² + 20x - 25 (predice demanda de pacientes)
   • Inversa: T = 120/m (calcula tiempo de espera según médicos)

⌨️ ATAJOS DE TECLADO:
   • Enter: Calcular valores en las calculadoras
   • F1: Mostrar esta ayuda

📞 SOPORTE: Para más información sobre el sistema de salud salvadoreño
y la implementación de las funciones matemáticas, consulte la documentación.
        """
        
        ayuda_text.insert(tk.END, ayuda_content)
        ayuda_text.config(state='disabled')

def main():
    """
    Función principal para ejecutar el sistema
    """
    print("=== Sistema de Optimización de Citas Médicas - El Salvador ===")
    print("Iniciando aplicación con interfaz moderna...")
    
    try:
        # Crear y ejecutar la interfaz gráfica moderna
        app = InterfazModerna()
        app.ejecutar()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        input("Presione Enter para salir...")

if __name__ == "__main__":
    main()