import snap7
from datetime import datetime

class PLCClient:
    def __init__(self, ip='192.168.0.1', rack=0, slot=1):
        self.client = snap7.client.Client()
        self.ip = ip
        self.rack = rack
        self.slot = slot
        self.connected = False
        
    def connect(self):
        try:
            self.client.connect(self.ip, self.rack, self.slot)
            self.connected = True
            print("Conectado ao CLP com sucesso")
        except Exception as e:
            print(f"Erro ao conectar ao CLP: {e}")
            self.connected = False
    
    def read_process_variables(self):
        if not self.connected:
            self.connect()
        
        try:
            # Leitura das variáveis do CLP
            # Os endereços e tipos de dados devem ser ajustados conforme configuração do CLP
            temperatura_forno = self.read_real(db_number=1, start=0)
            pressao_carga = self.read_real(db_number=1, start=4)
            corrente_motor = self.read_real(db_number=1, start=8)
            altura_matriz = self.read_real(db_number=1, start=12)
            
            return {
                'time_stamp': datetime.now(),
                'temperatura_forno': temperatura_forno,
                'pressao_carga': pressao_carga,
                'corrente_motor': corrente_motor,
                'altura_Matriz': altura_matriz
            }
            
        except Exception as e:
            print(f"Erro na leitura do CLP: {e}")
            self.connected = False
            return None
    
    def read_real(self, db_number, start):
        """Lê um valor REAL (Float) do CLP"""
        data = self.client.db_read(db_number, start, 4)
        return snap7.util.get_real(data, 0)
    
    def disconnect(self):
        if self.connected:
            self.client.disconnect()
            self.connected = False