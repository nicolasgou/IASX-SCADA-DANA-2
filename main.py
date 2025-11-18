import customtkinter as ctk
from src.interfaces.monitor import MonitorFrame
from src.interfaces.historico import HistoricoFrame
from src.communication.plc_client import PLCClient
from src.database.db_manager import DatabaseManager
import threading
import time

ctk.set_appearance_mode("light")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.configure(fg_color="white")

        # Configuração da janela principal
        self.title("IASX-SCADA-DANA")
        self.geometry("1920x1080")  # Otimizado para TV 50"

        
        # Inicialização dos componentes
        self.plc_client = PLCClient()
        self.db_manager = DatabaseManager()
        
        # Criação das interfaces
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Abas principais
        self.tab_monitor = self.tabview.add("MONITOR")
        self.tab_historico = self.tabview.add("HISTÓRICO")
        
        # Frames principais
        self.monitor_frame = MonitorFrame(self.tab_monitor, self.plc_client)
        self.historico_frame = HistoricoFrame(self.tab_historico, self.db_manager)
        
        # Iniciar thread de aquisição de dados
        self.running = True
        self.data_thread = threading.Thread(target=self.data_acquisition_loop)
        self.data_thread.start()
        
    def data_acquisition_loop(self):
        while self.running:
            try:
                # Leitura das variáveis do CLP
                dados = self.plc_client.read_process_variables()
                
                # Atualização da interface
                self.monitor_frame.update_values(dados)
                
                # Armazenamento no banco de dados
                self.db_manager.store_process_data(dados)
                
                time.sleep(1)  # Intervalo de amostragem de 1 segundo
                
            except Exception as e:
                print(f"Erro na aquisição de dados: {e}")
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
