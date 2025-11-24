import threading
import time

import customtkinter as ctk

from src.communication.plc_client import PLCClient
from src.config import APP_SIZE, TIMER
from src.database.db_manager import DatabaseManager
from src.interfaces.historico import HistoricoFrame
from src.interfaces.monitor import MonitorFrame

ctk.set_appearance_mode("light")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.configure(fg_color="white")

        # Configuracao da janela principal
        self.title("IASX-SCADA-DANA")
        self.geometry(f"{APP_SIZE[0]}x{APP_SIZE[1]}")  # Ajustavel via .config

        # Inicializacao dos componentes
        self.plc_client = PLCClient()
        self.db_manager = DatabaseManager()

        # Criacao das interfaces
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(expand=True, fill="both", padx=10, pady=10)

        # Abas principais
        self.tab_monitor = self.tabview.add("MONITOR")
        self.tab_historico = self.tabview.add("HISTORICO")

        # Frames principais
        self.monitor_frame = MonitorFrame(self.tab_monitor, self.plc_client, self.db_manager)
        self.historico_frame = HistoricoFrame(self.tab_historico, self.db_manager)

        # Iniciar thread de aquisicao de dados
        self.running = True
        self.data_thread = threading.Thread(target=self.data_acquisition_loop)
        self.data_thread.start()

    def data_acquisition_loop(self):
        while self.running:
            try:
                True
                # Leitura das variaveis do CLP
                dados = self.plc_client.read_process_variables()
                
                # Atualizacao da interface
                self.monitor_frame.update_values(dados)
                
                # Se a store flag estiver ativa, armazena os dados
                if dados['store_flag']:
                    self.db_manager.store_process_data(dados)
                
                time.sleep(TIMER)
            except Exception as e:
                print(f"[App] Erro na aquisicao de dados: {e}")
                time.sleep(5)  # Tempo de espera antes de tentar novamente

    def on_closing(self):
        self.running = False
        self.data_thread.join()
        self.db_manager.close()
        self.plc_client.disconnect()
        self.quit()


if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
