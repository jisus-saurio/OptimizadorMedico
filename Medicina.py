import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

class SistemaOptimizacionSaludSalvador:
    """
    Sistema Avanzado de Optimización de Citas Médicas para El Salvador
    Aplicación de Funciones Cuadráticas e Inversas con Datos Reales 2024-2025
    """
    
    def __init__(self):
        # DATOS REALES ACTUALIZADOS 2024-2025
        self.poblacion_total = 6338193
        self.medicos_total_sistema = 4318
        self.tiempo_espera_consulta_actual = 4.2
        self.eficiencia_sistema_actual = 0.57
        self.ausentismo_promedio = 0.35
        
        # ESPECIALIDADES CRÍTICAS
        self.especialidades_criticas = {
            'gastroenterologia': {'disponibles': 6, 'necesarios': 25, 'tiempo_espera_meses': 8},
            'oftalmologia': {'disponibles': 12, 'necesarios': 45, 'tiempo_espera_meses': 18},
            'cardiologia': {'disponibles': 18, 'necesarios': 60, 'tiempo_espera_meses': 12},
            'dermatologia': {'disponibles': 8, 'necesarios': 30, 'tiempo_espera_meses': 10},
            'psiquiatria': {'disponibles': 55, 'necesarios': 120, 'tiempo_espera_meses': 6},
            'cirugia_general': {'disponibles': 85, 'necesarios': 150, 'tiempo_espera_meses': 6},
            'traumatologia': {'disponibles': 45, 'necesarios': 90, 'tiempo_espera_meses': 4},
            'ginecologia': {'disponibles': 68, 'necesarios': 100, 'tiempo_espera_meses': 5}
        }
        
        # PARÁMETROS FUNCIONES MATEMÁTICAS
        self.a_cuadratica = -0.8
        self.b_cuadratica = 25
        self.c_cuadratica = -40
        self.k_inversa = 180
        self.exponente_inversa = 0.85
        self.tiempo_base_minimo = 0.15
        
        # FACTORES ESTACIONALES
        self.factor_estacional = {
            'enero': 1.2, 'febrero': 1.1, 'marzo': 1.0, 'abril': 1.3,
            'mayo': 1.4, 'junio': 1.2, 'julio': 1.1, 'agosto': 1.2,
            'septiembre': 1.5, 'octubre': 1.3, 'noviembre': 1.1, 'diciembre': 0.9
        }
        
        # FACTORES POR DÍA
        self.factor_dia = {
            'lunes': 1.3, 'martes': 1.2, 'miercoles': 1.1, 'jueves': 1.1,
            'viernes': 1.15, 'sabado': 0.7, 'domingo': 0.5
        }
        
        # TIPOS DE CONSULTA
        self.tipos_consulta = {
            'emergencia': {'proporcion': 0.20, 'complejidad': 1.8},
            'especialidad_critica': {'proporcion': 0.25, 'complejidad': 1.6},
            'consulta_general': {'proporcion': 0.40, 'complejidad': 1.0},
            'seguimiento': {'proporcion': 0.15, 'complejidad': 0.8}
        }

    def demanda_cuadratica_avanzada(self, hora, dia_semana='lunes', mes='enero'):
        """Función cuadrática mejorada: y = ax² + bx + c + factores"""
        # Función base cuadrática
        demanda_base = (self.a_cuadratica * (hora ** 2) + 
                       self.b_cuadratica * hora + 
                       self.c_cuadratica)
        
        # Aplicar factores
        factor_d = self.factor_dia.get(dia_semana.lower(), 1.0)
        factor_m = self.factor_estacional.get(mes.lower(), 1.0)
        
        # Demanda final
        demanda_final = max(0, demanda_base) * factor_d * factor_m
        demanda_efectiva = demanda_final * (1 - self.ausentismo_promedio)
        
        return max(1, int(demanda_efectiva))

    def tiempo_espera_inverso_avanzado(self, num_medicos, demanda, tipo_consulta='consulta_general', especialidad=None):
        """Función inversa mejorada: T = k/m^n + base"""
        if num_medicos <= 0:
            return float('inf')
        
        # Función inversa base
        tiempo_base = (self.k_inversa / (num_medicos ** self.exponente_inversa)) + self.tiempo_base_minimo
        
        # Factor de complejidad
        factor_complejidad = self.tipos_consulta.get(tipo_consulta, {'complejidad': 1.0})['complejidad']
        
        # Factor por especialidad escasa
        factor_especialidad = 1.0
        if especialidad and especialidad in self.especialidades_criticas:
            escasez = self.especialidades_criticas[especialidad]
            ratio_deficit = escasez['necesarios'] / max(1, escasez['disponibles'])
            factor_especialidad = min(ratio_deficit, 5.0)
        
        # Factor de eficiencia
        factor_eficiencia = 1 / self.eficiencia_sistema_actual
        
        # Tiempo final
        tiempo_final = tiempo_base * factor_complejidad * factor_especialidad * factor_eficiencia
        
        return min(tiempo_final, 24.0)

    def calcular_medicos_optimos(self, demanda, tiempo_objetivo=2.0):
        """Calcula médicos óptimos por búsqueda"""
        mejor_medicos = 1
        mejor_error = float('inf')
        
        for m in range(1, min(300, demanda * 3)):
            tiempo_calc = self.tiempo_espera_inverso_avanzado(m, demanda)
            error = abs(tiempo_calc - tiempo_objetivo)
            
            if error < mejor_error:
                mejor_medicos = m
                mejor_error = error
            
            if tiempo_calc <= tiempo_objetivo:
                break
        
        return mejor_medicos

class InterfazAvanzadaSalud:
    """Interfaz gráfica avanzada para el Sistema de Optimización"""
    
    def __init__(self):
        self.sistema = SistemaOptimizacionSaludSalvador()
        self.root = tk.Tk()
        
        # Variables de control - INICIALIZAR ANTES
        self.var_hora = tk.IntVar(value=14)
        self.var_medicos = tk.IntVar(value=60)
        self.var_tipo_consulta = tk.StringVar(value='consulta_general')
        self.var_especialidad = tk.StringVar(value='ninguna')
        self.var_dia_semana = tk.StringVar(value='lunes')
        self.var_mes = tk.StringVar(value='enero')
        
        self.configurar_ventana()
        self.configurar_estilos()
        self.crear_interfaz_completa()
    
    def configurar_ventana(self):
        """Configuración inicial optimizada"""
        self.root.title("Sistema Avanzado de Optimización Médica - El Salvador")
        self.root.geometry("1600x1000")
        self.root.configure(bg='#f8f9fa')
        
        # Centrar ventana
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - 800
        y = (self.root.winfo_screenheight() // 2) - 500
        self.root.geometry(f"1600x1000+{x}+{y}")
        
        self.root.minsize(1400, 800)
    
    def configurar_estilos(self):
        """Configuración de colores y estilos modernos"""
        self.colores = {
            'primario': '#1e40af', 'secundario': '#059669', 'acento': '#dc2626',
            'warning': '#d97706', 'exito': '#16a34a', 'fondo': '#f8f9fa',
            'tarjeta': '#ffffff', 'texto': '#1f2937', 'texto_secundario': '#6b7280'
        }
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure('Titulo.TLabel', font=('Arial', 16, 'bold'), 
                           background=self.colores['tarjeta'], foreground=self.colores['texto'])
        self.style.configure('Tarjeta.TFrame', background=self.colores['tarjeta'], 
                           relief='solid', borderwidth=1)
    
    def crear_header_principal(self, parent):
        """Header con información del sistema"""
        header = tk.Frame(parent, bg=self.colores['primario'], height=120)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        contenido = tk.Frame(header, bg=self.colores['primario'])
        contenido.pack(expand=True, fill='both', padx=30, pady=20)
        
        titulo = tk.Label(contenido, text="Sistema de Optimización de Citas Médicas",
                         font=('Arial', 20, 'bold'), bg=self.colores['primario'], fg='white')
        titulo.pack(anchor='w')
        
        subtitulo = tk.Label(contenido, text="El Salvador • Funciones Cuadráticas e Inversas • Análisis de Datos Reales 2024-2025",
                           font=('Arial', 11), bg=self.colores['primario'], fg='#bfdbfe')
        subtitulo.pack(anchor='w')
        
        # Estadísticas
        stats_frame = tk.Frame(contenido, bg=self.colores['primario'])
        stats_frame.pack(side='right', anchor='ne')
        
        estadisticas = [
            (f"{self.sistema.poblacion_total:,}", "Habitantes"),
            (f"{self.sistema.medicos_total_sistema:,}", "Médicos"),
            (f"{self.sistema.tiempo_espera_consulta_actual}h", "Espera Actual"),
            (f"{int(self.sistema.eficiencia_sistema_actual*100)}%", "Eficiencia")
        ]
        
        for valor, etiqueta in estadisticas:
            stat_frame = tk.Frame(stats_frame, bg=self.colores['primario'])
            stat_frame.pack(side='left', padx=15)
            
            tk.Label(stat_frame, text=valor, font=('Arial', 14, 'bold'),
                   bg=self.colores['primario'], fg='white').pack()
            tk.Label(stat_frame, text=etiqueta, font=('Arial', 9),
                   bg=self.colores['primario'], fg='#bfdbfe').pack()
    
    def crear_panel_control_interactivo(self, parent):
        """Panel de controles para gráficas interactivas"""
        panel = ttk.Frame(parent, style='Tarjeta.TFrame', padding=20)
        panel.pack(fill='x', padx=20, pady=(20, 10))
        
        ttk.Label(panel, text="Controles Interactivos", style='Titulo.TLabel').pack(anchor='w', pady=(0, 15))
        
        # Controles organizados
        controles = tk.Frame(panel, bg=self.colores['tarjeta'])
        controles.pack(fill='x')
        
        # Fila 1: Controles básicos
        fila1 = tk.Frame(controles, bg=self.colores['tarjeta'])
        fila1.pack(fill='x', pady=5)
        
        # Hora
        tk.Label(fila1, text="Hora del día:", font=('Arial', 10), bg=self.colores['tarjeta']).pack(side='left')
        hora_scale = tk.Scale(fila1, from_=6, to=22, orient='horizontal', variable=self.var_hora,
                             length=120, command=self.actualizar_automatico)
        hora_scale.pack(side='left', padx=10)
        
        # Médicos
        tk.Label(fila1, text="Médicos:", font=('Arial', 10), bg=self.colores['tarjeta']).pack(side='left', padx=(20, 0))
        medicos_scale = tk.Scale(fila1, from_=1, to=200, orient='horizontal', variable=self.var_medicos,
                                length=120, command=self.actualizar_automatico)
        medicos_scale.pack(side='left', padx=10)
        
        # Fila 2: Controles avanzados
        fila2 = tk.Frame(controles, bg=self.colores['tarjeta'])
        fila2.pack(fill='x', pady=5)
        
        # Tipo
        tk.Label(fila2, text="Tipo:", font=('Arial', 10), bg=self.colores['tarjeta']).pack(side='left')
        combo_tipo = ttk.Combobox(fila2, textvariable=self.var_tipo_consulta, width=15,
                                 values=list(self.sistema.tipos_consulta.keys()), state='readonly')
        combo_tipo.pack(side='left', padx=10)
        combo_tipo.bind('<<ComboboxSelected>>', self.actualizar_automatico)
        
        # Especialidad
        tk.Label(fila2, text="Especialidad:", font=('Arial', 10), bg=self.colores['tarjeta']).pack(side='left', padx=(20, 0))
        especialidades = ['ninguna'] + list(self.sistema.especialidades_criticas.keys())
        combo_esp = ttk.Combobox(fila2, textvariable=self.var_especialidad, width=15,
                                values=especialidades, state='readonly')
        combo_esp.pack(side='left', padx=10)
        combo_esp.bind('<<ComboboxSelected>>', self.actualizar_automatico)
        
        # Día
        tk.Label(fila2, text="Día:", font=('Arial', 10), bg=self.colores['tarjeta']).pack(side='left', padx=(20, 0))
        dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
        combo_dia = ttk.Combobox(fila2, textvariable=self.var_dia_semana, width=10, values=dias, state='readonly')
        combo_dia.pack(side='left', padx=10)
        combo_dia.bind('<<ComboboxSelected>>', self.actualizar_automatico)
        
        # Mes
        tk.Label(fila2, text="Mes:", font=('Arial', 10), bg=self.colores['tarjeta']).pack(side='left', padx=(20, 0))
        meses = list(self.sistema.factor_estacional.keys())
        combo_mes = ttk.Combobox(fila2, textvariable=self.var_mes, width=10, values=meses, state='readonly')
        combo_mes.pack(side='left', padx=10)
        combo_mes.bind('<<ComboboxSelected>>', self.actualizar_automatico)
        
        # Botones
        botones_frame = tk.Frame(controles, bg=self.colores['tarjeta'])
        botones_frame.pack(side='right', fill='y', padx=20)
        
        # BOTÓN DE ACTUALIZACIÓN FORZOSA
        btn_actualizar = tk.Button(botones_frame, text="🔄 ACTUALIZAR GRÁFICAS",
                                  command=self.forzar_actualizacion,
                                  bg='#ff6b35', fg='white', font=('Arial', 11, 'bold'),
                                  relief='flat', cursor='hand2', padx=20, pady=8)
        btn_actualizar.pack(pady=5)
        
        # Botón simulación
        btn_simular = tk.Button(botones_frame, text="⚡ EJECUTAR SIMULACIÓN",
                               command=self.ejecutar_simulacion,
                               bg=self.colores['secundario'], fg='white', font=('Arial', 11, 'bold'),
                               relief='flat', cursor='hand2', padx=20, pady=8)
        btn_simular.pack(pady=5)
    
    def crear_area_graficas(self, parent):
        """Área para gráficas dinámicas con menú de pestañas"""
        area = ttk.Frame(parent, style='Tarjeta.TFrame', padding=20)
        area.pack(fill='both', expand=True, padx=20, pady=10)

        ttk.Label(area, text="Análisis Gráfico Interactivo", style='Titulo.TLabel').pack(anchor='w', pady=(0, 15))

        # Menú de pestañas para las gráficas
        self.tabs_graficas = ttk.Notebook(area)
        self.tabs_graficas.pack(fill='both', expand=True)

        # Crear un frame para cada gráfica
        self.tab_demanda = tk.Frame(self.tabs_graficas, bg='white')
        self.tab_tiempo = tk.Frame(self.tabs_graficas, bg='white')
        self.tab_tipo = tk.Frame(self.tabs_graficas, bg='white')
        self.tab_especialidad = tk.Frame(self.tabs_graficas, bg='white')

        self.tabs_graficas.add(self.tab_demanda, text="Demanda por Hora")
        self.tabs_graficas.add(self.tab_tiempo, text="Tiempo vs Médicos")
        self.tabs_graficas.add(self.tab_tipo, text="Distribución por Tipo")
        self.tabs_graficas.add(self.tab_especialidad, text="Déficit por Especialidad")

        # Inicializar cada gráfica
        self.actualizar_graficas()

    def actualizar_automatico(self, event=None):
        """Actualización automática cuando cambian controles"""
        # Pequeño delay para evitar actualizaciones excesivas
        if hasattr(self, '_after_id'):
            self.root.after_cancel(self._after_id)
        self._after_id = self.root.after(300, self.actualizar_graficas)
    
    def ampliar_graficas(self):
        """Abrir gráficas en ventana ampliada para mejor visualización"""
        try:
            # OBTENER VALORES ACTUALES
            hora = self.var_hora.get()
            medicos = self.var_medicos.get()
            tipo = self.var_tipo_consulta.get()
            especialidad = self.var_especialidad.get() if self.var_especialidad.get() != 'ninguna' else None
            dia = self.var_dia_semana.get()
            mes = self.var_mes.get()
            
            # Crear ventana ampliada
            ventana_ampliada = tk.Toplevel(self.root)
            ventana_ampliada.title("Gráficas Ampliadas - Sistema de Optimización Médica")
            ventana_ampliada.geometry("1400x900")
            ventana_ampliada.configure(bg='white')
            
            # Centrar ventana
            ventana_ampliada.transient(self.root)
            x = (ventana_ampliada.winfo_screenwidth() // 2) - 700
            y = (ventana_ampliada.winfo_screenheight() // 2) - 450
            ventana_ampliada.geometry(f"1400x900+{x}+{y}")
            
            # Frame para las gráficas ampliadas
            frame_ampliado = tk.Frame(ventana_ampliada, bg='white')
            frame_ampliado.pack(fill='both', expand=True, padx=20, pady=20)
            
            # Título de la ventana ampliada
            titulo_ampliado = tk.Label(frame_ampliado, 
                                     text=f"Análisis Detallado - {hora}:00h, {medicos} médicos, {dia.title()} de {mes.title()}",
                                     font=('Arial', 16, 'bold'), bg='white', fg='#1e40af')
            titulo_ampliado.pack(pady=(0, 20))
            
            print(f"Creando gráficas ampliadas con: {hora}h, {medicos}m, {tipo}, {especialidad}, {dia}, {mes}")
            
            # Crear figura más grande
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle(f'Sistema de Salud - ANÁLISIS DETALLADO: {hora}:00h, {medicos} médicos, {dia.title()}', 
                        fontsize=18, fontweight='bold')
            
            # GRÁFICA 1: Demanda por hora (AMPLIADA)
            horas_rango = np.linspace(6, 22, 100)
            demanda_pura = [max(0, self.sistema.a_cuadratica * h**2 + 
                               self.sistema.b_cuadratica * h + 
                               self.sistema.c_cuadratica) for h in horas_rango]
            demanda_real = [self.sistema.demanda_cuadratica_avanzada(h, dia, mes) for h in horas_rango]
            
            ax1.plot(horas_rango, demanda_pura, 'b--', linewidth=3, label='Función Cuadrática Pura', alpha=0.6)
            ax1.plot(horas_rango, demanda_real, 'r-', linewidth=4, label=f'Modelo Real ({dia}, {mes})')
            
            # PUNTO ACTUAL - EXTRA GRANDE
            demanda_actual = self.sistema.demanda_cuadratica_avanzada(hora, dia, mes)
            ax1.plot(hora, demanda_actual, 'ro', markersize=20, zorder=10)
            ax1.annotate(f'HORA SELECCIONADA: {hora}:00\n{demanda_actual} pacientes', 
                        (hora, demanda_actual), xytext=(30, 30), 
                        textcoords='offset points', fontsize=14, weight='bold',
                        bbox=dict(boxstyle="round,pad=0.7", facecolor="yellow", alpha=0.9),
                        arrowprops=dict(arrowstyle='->', color='red', lw=3))
            
            ax1.set_xlabel('Hora del Día', fontsize=14)
            ax1.set_ylabel('Pacientes', fontsize=14)
            ax1.set_title(f'Demanda por Hora - {dia.title()} en {mes.title()}\ny = -0.8x² + 25x - 40', fontsize=14)
            ax1.legend(fontsize=12)
            ax1.grid(True, alpha=0.3)
            ax1.set_xlim(6, 22)
            ax1.tick_params(labelsize=12)
            
            # GRÁFICA 2: Tiempo vs Médicos (AMPLIADA)
            medicos_rango = np.linspace(1, 250, 200)
            tiempos = [self.sistema.tiempo_espera_inverso_avanzado(m, demanda_actual, tipo, especialidad) 
                      for m in medicos_rango]
            
            ax2.plot(medicos_rango, tiempos, 'g-', linewidth=4, label=f'Tiempo - {tipo}')
            
            # PUNTO ACTUAL - EXTRA GRANDE
            tiempo_actual = self.sistema.tiempo_espera_inverso_avanzado(medicos, demanda_actual, tipo, especialidad)
            ax2.plot(medicos, tiempo_actual, 'go', markersize=20, zorder=10)
            ax2.annotate(f'MÉDICOS ASIGNADOS: {medicos}\n{tiempo_actual:.1f} horas de espera', 
                        (medicos, tiempo_actual), xytext=(30, 30), 
                        textcoords='offset points', fontsize=14, weight='bold',
                        bbox=dict(boxstyle="round,pad=0.7", facecolor="lightgreen", alpha=0.9),
                        arrowprops=dict(arrowstyle='->', color='green', lw=3))
            
            # Línea horizontal de tiempo mínimo teórico
            if demanda_actual > 0:
                tiempo_minimo = demanda_actual / medicos
                ax2.axhline(y=tiempo_minimo, color='orange', linestyle='--', linewidth=2, label='Tiempo mínimo teórico')
                ax2.annotate(
                    f"Tiempo mínimo teórico: {tiempo_minimo:.2f} h\n({demanda_actual} pacientes / {medicos} médicos)",
                    xy=(medicos, tiempo_minimo), xytext=(20, -30),
                    textcoords='offset points', color='orange', fontsize=10, weight='bold',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="orange", alpha=0.15),
                    arrowprops=dict(arrowstyle='->', color='orange', lw=2)
                )
            
            ax2.set_xlabel('Número de Médicos', fontsize=14)
            ax2.set_ylabel('Tiempo de Espera (horas)', fontsize=14)
            ax2.set_title(f'Tiempo de Espera - {tipo.replace("_", " ").title()}\nT = k/m^n + base', fontsize=14)
            ax2.legend(fontsize=12)
            ax2.grid(True, alpha=0.3)
            ax2.set_ylim(0, min(25, max(tiempos)))
            ax2.tick_params(labelsize=12)
            
            # GRÁFICA 3: Distribución consultas (AMPLIADA)
            tipos = list(self.sistema.tipos_consulta.keys())
            proporciones = [self.sistema.tipos_consulta[t]['proporcion'] for t in tipos]
            
            # Resaltar tipo actual
            colores = ['#ff4444' if t == tipo else '#cccccc' for t in tipos]
            explode = [0.3 if t == tipo else 0 for t in tipos]
            
            wedges, texts, autotexts = ax3.pie(proporciones, labels=[t.replace('_', '\n') for t in tipos], 
                                              autopct='%1.1f%%', colors=colores, explode=explode,
                                              textprops={'fontsize': 12})
            ax3.set_title(f'Distribución por Tipo de Consulta\n*** {tipo.replace("_", " ").title()} SELECCIONADO ***', 
                         fontsize=14, weight='bold')
            
            # GRÁFICA 4: Especialidad actual o resumen (AMPLIADA)
            if especialidad:
                esp_data = self.sistema.especialidades_criticas[especialidad]
                categorias = ['Disponibles', 'Necesarios', 'Déficit']
                valores = [esp_data['disponibles'], esp_data['necesarios'], 
                          esp_data['necesarios'] - esp_data['disponibles']]
                colores_esp = ['#dc2626', '#16a34a', '#f97316']
                
                bars = ax4.bar(categorias, valores, color=colores_esp, alpha=0.8, width=0.6)
                ax4.set_ylabel('Número de Médicos', fontsize=14)
                ax4.set_title(f'ESPECIALIDAD SELECCIONADA: {especialidad.replace("_", " ").title()}\n'
                             f'Tiempo de espera actual: {esp_data["tiempo_espera_meses"]} meses', fontsize=14)
                
                for bar, val in zip(bars, valores):
                    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                            f'{val}', ha='center', va='bottom', fontsize=14, weight='bold')
                ax4.grid(True, alpha=0.3, axis='y')
                ax4.tick_params(labelsize=12)
            else:
                # Resumen general ampliado
                especialidades = list(self.sistema.especialidades_criticas.keys())
                deficit_total = [self.sistema.especialidades_criticas[e]['necesarios'] - 
                               self.sistema.especialidades_criticas[e]['disponibles'] for e in especialidades]
                
                bars = ax4.bar(range(len(especialidades)), deficit_total, 
                              color=['#dc2626' if d > 30 else '#f97316' if d > 15 else '#22c55e' for d in deficit_total],
                              alpha=0.8)
                ax4.set_xlabel('Especialidades', fontsize=14)
                ax4.set_ylabel('Déficit de Médicos', fontsize=14)
                ax4.set_title('Déficit por Especialidad Médica', fontsize=14)
                ax4.set_xticks(range(len(especialidades)))
                ax4.set_xticklabels([e.replace('_', '\n') for e in especialidades], fontsize=10)
                ax4.grid(True, alpha=0.3, axis='y')
                ax4.tick_params(labelsize=12)
                
                # Agregar valores encima de las barras
                for i, val in enumerate(deficit_total):
                    ax4.text(i, val + 1, f'{val}', ha='center', va='bottom', fontsize=12, weight='bold')
            
            plt.tight_layout()
            
            # Integrar en la ventana ampliada
            canvas_ampliado = FigureCanvasTkAgg(fig, frame_ampliado)
            canvas_ampliado.draw()
            canvas_ampliado.get_tk_widget().pack(fill='both', expand=True)
            
            # Panel de información detallado
            info_detallado = tk.Frame(frame_ampliado, bg='#f0f8ff', relief='solid', bd=2)
            info_detallado.pack(fill='x', pady=(20, 0))
            
            tk.Label(info_detallado, text="📊 ANÁLISIS DETALLADO DE LOS PARÁMETROS SELECCIONADOS", 
                    font=('Arial', 16, 'bold'), bg='#f0f8ff', fg='#1e40af').pack(pady=10)
            
            # Calcular métricas adicionales
            medicos_optimos = self.sistema.calcular_medicos_optimos(demanda_actual, 2.0)
            eficiencia_asignacion = min(100, (medicos_optimos / medicos * 100)) if medicos > 0 else 0
            
            info_detallado_text = f"""
🕐 CONFIGURACIÓN TEMPORAL: {hora}:00 horas del {dia.title()} de {mes.title()}
👥 DEMANDA PROYECTADA: {demanda_actual} pacientes (Factor día: {self.sistema.factor_dia[dia]:.1f}x, Factor mes: {self.sistema.factor_estacional[mes]:.1f}x)
👨‍⚕️ RECURSOS ASIGNADOS: {medicos} médicos → Tiempo estimado: {tiempo_actual:.1f} horas
⚖️ OPTIMIZACIÓN: {medicos_optimos} médicos serían óptimos para 2h de espera (Eficiencia actual: {eficiencia_asignacion:.1f}%)
📋 TIPO DE CONSULTA: {tipo.replace('_', ' ').title()} (Complejidad: {self.sistema.tipos_consulta[tipo]['complejidad']}x)
🏥 ESPECIALIDAD: {(especialidad or 'General').replace('_', ' ').title()}
📈 CONTEXTO SISTEMA: Eficiencia {int(self.sistema.eficiencia_sistema_actual*100)}% • Ausentismo {int(self.sistema.ausentismo_promedio*100)}%
            """
            
            tk.Label(info_detallado, text=info_detallado_text.strip(), font=('Arial', 12),
                    bg='#f0f8ff', fg='#1e40af', justify='left').pack(pady=10, padx=20)
            
            # Botón para cerrar
            btn_cerrar = tk.Button(frame_ampliado, text="✖ Cerrar Ventana Ampliada",
                                  command=ventana_ampliada.destroy,
                                  bg='#dc2626', fg='white', font=('Arial', 12, 'bold'),
                                  relief='flat', cursor='hand2', padx=30, pady=10)
            btn_cerrar.pack(pady=20)
            
        except Exception as e:
            print(f"ERROR en ampliar_graficas: {e}")
            messagebox.showerror("Error", f"Error al ampliar gráficas:\n{e}")
    
    def forzar_actualizacion(self):
        """Fuerza actualización inmediata"""
        print(f"FORZANDO ACTUALIZACIÓN con valores:")
        print(f"  Hora: {self.var_hora.get()}")
        print(f"  Médicos: {self.var_medicos.get()}")
        print(f"  Tipo: {self.var_tipo_consulta.get()}")
        print(f"  Especialidad: {self.var_especialidad.get()}")
        print(f"  Día: {self.var_dia_semana.get()}")
        print(f"  Mes: {self.var_mes.get()}")
        
        self.actualizar_graficas()
        
        # Mensaje de confirmación
        messagebox.showinfo("Actualización Forzada", 
                          f"Gráficas actualizadas con:\n"
                          f"• Hora: {self.var_hora.get()}:00\n"
                          f"• Médicos: {self.var_medicos.get()}\n"
                          f"• Tipo: {self.var_tipo_consulta.get()}\n"
                          f"• Día: {self.var_dia_semana.get()}")
    
    def actualizar_graficas(self):
        """Actualiza todas las pestañas de gráficas"""
        self.actualizar_grafica_demanda()
        self.actualizar_grafica_tiempo()
        self.actualizar_grafica_tipo()
        self.actualizar_grafica_especialidad()

    def actualizar_grafica_demanda(self):
        """Gráfica: Demanda por hora"""
        for widget in self.tab_demanda.winfo_children():
            widget.destroy()
        hora = self.var_hora.get()
        dia = self.var_dia_semana.get()
        mes = self.var_mes.get()
        horas_rango = np.linspace(6, 22, 100)
        demanda_pura = [max(0, self.sistema.a_cuadratica * h**2 + self.sistema.b_cuadratica * h + self.sistema.c_cuadratica) for h in horas_rango]
        demanda_real = [self.sistema.demanda_cuadratica_avanzada(h, dia, mes) for h in horas_rango]
        demanda_actual = self.sistema.demanda_cuadratica_avanzada(hora, dia, mes)

        fig, ax = plt.subplots(figsize=(9, 5))
        ax.plot(horas_rango, demanda_pura, 'b--', linewidth=2, label='Función Cuadrática Pura', alpha=0.5)
        ax.plot(horas_rango, demanda_real, 'r-', linewidth=3, label=f'Modelo Real ({dia}, {mes})')
        ax.plot(hora, demanda_actual, 'ro', markersize=10, zorder=10)
        ax.annotate(f'{demanda_actual} pacientes', (hora, demanda_actual), xytext=(10, 10), 
                    textcoords='offset points', fontsize=11, weight='bold',
                    bbox=dict(boxstyle="round,pad=0.4", facecolor="yellow", alpha=0.8),
                    arrowprops=dict(arrowstyle='->', color='red', lw=2))
        ax.set_xlabel('Hora del Día', fontsize=12)
        ax.set_ylabel('Pacientes', fontsize=12)
        ax.set_title('Demanda por Hora', fontsize=14)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(6, 22)
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, self.tab_demanda)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def actualizar_grafica_tiempo(self):
        """Gráfica: Tiempo de espera vs médicos (mejorada, profesional y legible)"""
        for widget in self.tab_tiempo.winfo_children():
            widget.destroy()
        hora = self.var_hora.get()
        medicos = self.var_medicos.get()
        tipo = self.var_tipo_consulta.get()
        especialidad = self.var_especialidad.get() if self.var_especialidad.get() != 'ninguna' else None
        dia = self.var_dia_semana.get()
        mes = self.var_mes.get()
        demanda_actual = self.sistema.demanda_cuadratica_avanzada(hora, dia, mes)
        medicos_rango = np.linspace(1, 200, 200)
        tiempos = [self.sistema.tiempo_espera_inverso_avanzado(m, demanda_actual, tipo, especialidad) for m in medicos_rango]
        tiempo_actual = self.sistema.tiempo_espera_inverso_avanzado(medicos, demanda_actual, tipo, especialidad)

        # Tiempo mínimo teórico (todos los médicos trabajando sin pausa)
        tiempo_minimo = demanda_actual / medicos if medicos > 0 else float('inf')

        # Ajuste de límites para el eje Y
        valores_y = [*tiempos, tiempo_actual, tiempo_minimo]
        min_tiempo = min(val for val in valores_y if np.isfinite(val))
        max_tiempo = max(val for val in valores_y if np.isfinite(val))
        margen = (max_tiempo - min_tiempo) * 0.18 if max_tiempo > min_tiempo else 2
        y_min = max(0, min_tiempo - margen)
        y_max = max_tiempo + margen
        # Siempre deja espacio para etiquetas
        if y_max - y_min < 6:
            y_max = y_min + 6

        fig, ax = plt.subplots(figsize=(11, 6))
        # Curva principal
        ax.plot(medicos_rango, tiempos, color='#059669', linewidth=3, label=f'Tiempo - {tipo.replace("_", " ").title()}')
        # Punto actual
        ax.scatter([medicos], [tiempo_actual], color='#059669', s=140, edgecolor='black', zorder=10)
        ax.annotate(f'{tiempo_actual:.1f} h',
                    (medicos, tiempo_actual),
                    xytext=(0, 35), textcoords='offset points',
                    ha='center', va='bottom',
                    fontsize=13, weight='bold',
                    bbox=dict(boxstyle="round,pad=0.5", facecolor="#bbf7d0", alpha=0.95),
                    arrowprops=dict(arrowstyle='->', color='#059669', lw=2))

        # Línea horizontal de tiempo mínimo teórico
        if np.isfinite(tiempo_minimo):
            ax.axhline(y=tiempo_minimo, color='#f59e42', linestyle='--', linewidth=2, label='Tiempo mínimo teórico')
            # Etiqueta a la derecha, fuera de la curva
            ax.annotate(
                f"Teórico: {tiempo_minimo:.2f} h\n({demanda_actual} pacientes / {medicos} médicos)",
                xy=(medicos_rango[-1], tiempo_minimo),
                xytext=(-10, 30),
                textcoords='offset points',
                color='#b45309', fontsize=11, weight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#fde68a", alpha=0.8),
                ha='right', va='bottom'
            )

        # Mejoras visuales
        ax.set_xlabel('Número de Médicos', fontsize=13, fontweight='bold')
        ax.set_ylabel('Tiempo de Espera (horas)', fontsize=13, fontweight='bold')
        ax.set_title('⏳ Tiempo de Espera vs Médicos', fontsize=17, fontweight='bold', color='#1e40af', pad=15)
        ax.legend(fontsize=12, loc='upper right', frameon=True, facecolor='white')
        ax.grid(True, alpha=0.22)
        ax.set_ylim(y_min, y_max)
        ax.set_xlim(0, 205)
        ax.tick_params(labelsize=12)
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, self.tab_tiempo)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def actualizar_grafica_tipo(self):
        """Gráfica: Distribución por tipo de consulta (dinámica según hora y médicos)"""
        for widget in self.tab_tipo.winfo_children():
            widget.destroy()
        tipos = list(self.sistema.tipos_consulta.keys())
        tipo = self.var_tipo_consulta.get()
        hora = self.var_hora.get()
        medicos = self.var_medicos.get()

        # Demanda relativa (normalizada 0-1)
        demanda_max = max([self.sistema.demanda_cuadratica_avanzada(h, self.var_dia_semana.get(), self.var_mes.get()) for h in range(6, 23)])
        demanda_actual = self.sistema.demanda_cuadratica_avanzada(hora, self.var_dia_semana.get(), self.var_mes.get())
        demanda_rel = demanda_actual / demanda_max if demanda_max else 0.5

        # Médicos relativo (normalizado 0-1)
        medicos_rel = min(1.0, medicos / 200)

        # Ajuste dinámico de proporciones
        prop_emergencia = 0.15 + 0.15 * demanda_rel * (1 - medicos_rel)
        prop_especialidad = 0.20 + 0.15 * demanda_rel * (1 - medicos_rel)
        prop_general = 0.30 + 0.20 * (1 - demanda_rel) * medicos_rel
        prop_seguimiento = 1.0 - (prop_emergencia + prop_especialidad + prop_general)
        proporciones = [prop_emergencia, prop_especialidad, prop_general, max(0, prop_seguimiento)]

        # Normalizar para evitar errores de redondeo
        total = sum(proporciones)
        proporciones = [p / total for p in proporciones]

        colores = ['#ff4444' if t == tipo else '#cccccc' for t in tipos]
        explode = [0.2 if t == tipo else 0 for t in tipos]

        fig, ax = plt.subplots(figsize=(7, 5))
        wedges, texts, autotexts = ax.pie(proporciones, labels=[t.replace('_', '\n') for t in tipos], 
                                      autopct='%1.1f%%', colors=colores, explode=explode,
                                      textprops={'fontsize': 11})
        ax.set_title(f'Distribución por Tipo de Consulta\n*** {tipo.replace("_", " ").title()} SELECCIONADO ***', fontsize=13, weight='bold')
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, self.tab_tipo)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def actualizar_grafica_especialidad(self):
        """Gráfica: Déficit por especialidad"""
        for widget in self.tab_especialidad.winfo_children():
            widget.destroy()
        especialidad = self.var_especialidad.get() if self.var_especialidad.get() != 'ninguna' else None
        fig, ax = plt.subplots(figsize=(9, 5))
        if especialidad:
            esp_data = self.sistema.especialidades_criticas[especialidad]
            categorias = ['Disponibles', 'Necesarios', 'Déficit']
            valores = [esp_data['disponibles'], esp_data['necesarios'], esp_data['necesarios'] - esp_data['disponibles']]
            colores_esp = ['#dc2626', '#16a34a', '#f97316']
            bars = ax.bar(categorias, valores, color=colores_esp, alpha=0.8, width=0.6)
            ax.set_ylabel('Número de Médicos', fontsize=12)
            ax.set_title(f'ESPECIALIDAD: {especialidad.replace("_", " ").title()}\nTiempo de espera: {esp_data["tiempo_espera_meses"]} meses', fontsize=13)
            for bar, val in zip(bars, valores):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{val}', ha='center', va='bottom', fontsize=12, weight='bold')
            ax.grid(True, alpha=0.3, axis='y')
            ax.tick_params(labelsize=11)
        else:
            especialidades = list(self.sistema.especialidades_criticas.keys())
            deficit_total = [self.sistema.especialidades_criticas[e]['necesarios'] - self.sistema.especialidades_criticas[e]['disponibles'] for e in especialidades]
            bars = ax.bar(range(len(especialidades)), deficit_total, 
                          color=['#dc2626' if d > 30 else '#f97316' if d > 15 else '#22c55e' for d in deficit_total],
                          alpha=0.8)
            ax.set_xlabel('Especialidades', fontsize=12)
            ax.set_ylabel('Déficit de Médicos', fontsize=12)
            ax.set_title('Déficit por Especialidad Médica', fontsize=13)
            ax.set_xticks(range(len(especialidades)))
            ax.set_xticklabels([e.replace('_', '\n') for e in especialidades], fontsize=10)
            ax.grid(True, alpha=0.3, axis='y')
            ax.tick_params(labelsize=11)
            for i, val in enumerate(deficit_total):
                ax.text(i, val + 1, f'{val}', ha='center', va='bottom', fontsize=11, weight='bold')
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, self.tab_especialidad)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def ejecutar_simulacion(self):
        """Ejecutar simulación con parámetros actuales"""
        hora = self.var_hora.get()
        medicos = self.var_medicos.get()
        tipo = self.var_tipo_consulta.get()
        especialidad = self.var_especialidad.get() if self.var_especialidad.get() != 'ninguna' else None
        dia = self.var_dia_semana.get()
        mes = self.var_mes.get()
        
        # Calcular métricas específicas
        demanda = self.sistema.demanda_cuadratica_avanzada(hora, dia, mes)
        tiempo = self.sistema.tiempo_espera_inverso_avanzado(medicos, demanda, tipo, especialidad)
        medicos_optimos = self.sistema.calcular_medicos_optimos(demanda, 2.0)
        
        # Simulación rápida de 24 horas
        total_pacientes = 0
        tiempo_promedio = 0
        
        for h in range(6, 23):
            dem_h = self.sistema.demanda_cuadratica_avanzada(h, dia, mes)
            total_pacientes += dem_h
            tiempo_h = self.sistema.tiempo_espera_inverso_avanzado(medicos, dem_h, tipo, especialidad)
            tiempo_promedio += tiempo_h
        
        tiempo_promedio /= 17  # 17 horas de operación
        
        # Mostrar resultados
        mensaje = f"""✅ SIMULACIÓN COMPLETADA CON SUS PARÁMETROS

🎯 CONFIGURACIÓN UTILIZADA:
• Hora: {hora}:00 ({dia.title()} de {mes.title()})
• Médicos: {medicos} (óptimo recomendado: {medicos_optimos})
• Tipo: {tipo.replace('_', ' ').title()}
• Especialidad: {(especialidad or 'General').replace('_', ' ').title()}

📊 RESULTADOS ESPECÍFICOS:
• Demanda en hora {hora}: {demanda} pacientes
• Tiempo espera en hora {hora}: {tiempo:.1f} horas
• Eficiencia de asignación: {min(100, medicos_optimos/medicos*100):.0f}%

📈 SIMULACIÓN DIARIA COMPLETA:
• Total pacientes/día: {total_pacientes:,}
• Tiempo promedio/día: {tiempo_promedio:.1f} horas
• Mejora vs actual ({self.sistema.tiempo_espera_consulta_actual}h): {((self.sistema.tiempo_espera_consulta_actual - tiempo_promedio)/self.sistema.tiempo_espera_consulta_actual*100):.1f}%

Las gráficas muestran el análisis detallado de su configuración."""
        
        messagebox.showinfo("Simulación Personalizada", mensaje)
    
    def crear_interfaz_completa(self):
        """Crear la interfaz completa"""
        self.crear_header_principal(self.root)
        self.crear_panel_control_interactivo(self.root)
        self.crear_area_graficas(self.root)
    
    def ejecutar(self):
        """Ejecutar la aplicación"""
        try:
            # Esperar a que esté listo y hacer actualización inicial
            self.root.after(500, self.actualizar_graficas)
            self.root.mainloop()
        except Exception as e:
            print(f"Error al ejecutar: {e}")
            messagebox.showerror("Error", f"Error: {e}")

def main():
    """Función principal"""
    print("=== Sistema Avanzado de Optimización de Citas Médicas ===")
    print("El Salvador • Funciones Cuadráticas e Inversas • Python")
    print("Iniciando aplicación INTERACTIVA...")
    
    try:
        app = InterfazAvanzadaSalud()
        app.ejecutar()
    except Exception as e:
        print(f"Error al iniciar: {e}")
        input("Presione Enter para salir...")

if __name__ == "__main__":
    main()