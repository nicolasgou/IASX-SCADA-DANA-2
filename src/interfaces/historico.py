import customtkinter as ctk
from datetime import datetime, timedelta
import pandas as pd
from tkinter import filedialog
import csv

class HistoricoFrame(ctk.CTkFrame):
    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.pack(expand=True, fill="both", padx=20, pady=20)
        self.db_manager = db_manager
        
        # Configuração do layout
        self.setup_ui()
        
    def setup_ui(self):
        # Frame de Controles
        control_frame = ctk.CTkFrame(self)
        control_frame.pack(fill="x", padx=10, pady=10)
        
        # Seleção de período
        ctk.CTkLabel(
            control_frame, 
            text="Período:"
        ).pack(side="left", padx=5)
        
        self.period_var = ctk.StringVar(value="1h")
        periods = ["1h", "6h", "12h", "24h", "7d", "30d"]
        
        period_menu = ctk.CTkOptionMenu(
            control_frame,
            values=periods,
            variable=self.period_var,
            command=self.update_data
        )
        period_menu.pack(side="left", padx=5)
        
        # Botão Exportar
        self.export_btn = ctk.CTkButton(
            control_frame,
            text="Exportar CSV",
            command=self.export_data
        )
        self.export_btn.pack(side="right", padx=5)
        
        # Frame para a tabela
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Cabeçalhos da tabela
        headers = ["Timestamp", "Temperatura", "Pressão", "Corrente", "Altura"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                self.table_frame,
                text=header,
                font=("Roboto", 12, "bold")
            ).grid(row=0, column=i, padx=5, pady=5, sticky="w")
        
        # Área de rolagem para os dados
        self.scrollable_frame = ctk.CTkScrollableFrame(self.table_frame)
        self.scrollable_frame.grid(row=1, column=0, columnspan=5, sticky="nsew")
        
        self.update_data()
        
    def update_data(self, *args):
        # Limpar dados anteriores
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        # Calcular período
        period_map = {
            "1h": timedelta(hours=1),
            "6h": timedelta(hours=6),
            "12h": timedelta(hours=12),
            "24h": timedelta(days=1),
            "7d": timedelta(days=7),
            "30d": timedelta(days=30)
        }
        
        end_date = datetime.now()
        start_date = end_date - period_map[self.period_var.get()]
        
        # Buscar dados
        data = self.db_manager.get_historical_data(start_date, end_date)
        
        # Exibir dados
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                if j == 0:  # Timestamp
                    text = value.strftime("%Y-%m-%d %H:%M:%S")
                else:  # Valores numéricos
                    text = f"{value:.2f}"
                    
                ctk.CTkLabel(
                    self.scrollable_frame,
                    text=text
                ).grid(row=i, column=j, padx=5, pady=2, sticky="w")
                
    def export_data(self):
        # Preparar nome do arquivo
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
        default_filename = f"tel-prensa-russa-{timestamp}.csv"
        
        # Diálogo para salvar arquivo
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialfile=default_filename,
            filetypes=[("CSV files", "*.csv")]
        )
        
        if filename:
            # Calcular período
            period_map = {
                "1h": timedelta(hours=1),
                "6h": timedelta(hours=6),
                "12h": timedelta(hours=12),
                "24h": timedelta(days=1),
                "7d": timedelta(days=7),
                "30d": timedelta(days=30)
            }
            
            end_date = datetime.now()
            start_date = end_date - period_map[self.period_var.get()]
            
            # Buscar dados
            data = self.db_manager.get_historical_data(start_date, end_date)
            
            # Escrever arquivo CSV
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    'Timestamp', 
                    'Temperatura do Forno', 
                    'Pressão de Carga',
                    'Corrente do Motor',
                    'Altura da Matriz'
                ])
                writer.writerows(data)