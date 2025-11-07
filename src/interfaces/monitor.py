import customtkinter as ctk
from datetime import datetime

class MonitorFrame(ctk.CTkFrame):
    def __init__(self, parent, plc_client):
        super().__init__(parent)
        self.pack(expand=True, fill="both", padx=20, pady=20)
        self.plc_client = plc_client
        
        # Configuração do grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Título
        self.title_label = ctk.CTkLabel(
            self, 
            text="Monitoramento em Tempo Real", 
            font=("Roboto", 24, "bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Criação dos displays de variáveis
        self.create_variable_displays()
        
    def create_variable_displays(self):
        # Temperatura do Forno
        self.temp_frame = self.create_variable_frame(
            "Temperatura do Forno (°C)",
            row=1, column=0
        )
        
        # Pressão de Carga
        self.pressao_frame = self.create_variable_frame(
            "Pressão de Carga (bar)",
            row=1, column=1
        )
        
        # Corrente do Motor
        self.corrente_frame = self.create_variable_frame(
            "Corrente do Motor (A)",
            row=2, column=0
        )
        
        # Altura da Matriz
        self.altura_frame = self.create_variable_frame(
            "Altura da Matriz (mm)",
            row=2, column=1
        )
        
        # Status da Conexão
        self.status_label = ctk.CTkLabel(
            self,
            text="Status: Conectado",
            font=("Roboto", 16)
        )
        self.status_label.grid(row=3, column=0, columnspan=2, pady=20)
        
    def create_variable_frame(self, title, row, column):
        frame = ctk.CTkFrame(self)
        frame.grid(row=row, column=column, padx=20, pady=20, sticky="nsew")
        
        # Título da variável
        label = ctk.CTkLabel(
            frame,
            text=title,
            font=("Roboto", 18)
        )
        label.pack(pady=10)
        
        # Valor da variável
        value_label = ctk.CTkLabel(
            frame,
            text="0.0",
            font=("Roboto", 36, "bold")
        )
        value_label.pack(pady=20)
        
        return {"frame": frame, "title": label, "value": value_label}
    
    def update_values(self, data):
        if data:
            self.temp_frame["value"].configure(
                text=f"{data['temperatura_forno']:.1f}"
            )
            self.pressao_frame["value"].configure(
                text=f"{data['pressao_carga']:.1f}"
            )
            self.corrente_frame["value"].configure(
                text=f"{data['corrente_motor']:.1f}"
            )
            self.altura_frame["value"].configure(
                text=f"{data['altura_Matriz']:.1f}"
            )
            self.status_label.configure(
                text=f"Status: Conectado - Última atualização: {data['time_stamp'].strftime('%H:%M:%S')}"
            )
        else:
            self.status_label.configure(text="Status: Desconectado")