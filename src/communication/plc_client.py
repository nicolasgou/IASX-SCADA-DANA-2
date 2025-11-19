import snap7
import time
from datetime import datetime

from src.config import PLC_IP, PLC_RACK, PLC_SLOT
from src.config import DB_NUMBER 

class PLCClient:
    def __init__(self, ip=PLC_IP, rack=PLC_RACK, slot=PLC_SLOT):
        self.client = snap7.client.Client()
        self.ip = ip
        self.rack = rack
        self.slot = slot
        self.connected = False
        self.connect()
        
    def connect(self):
        try:
            self.client.connect(self.ip, self.rack, self.slot)
            if self.client.get_connected():
                print("[CLP] Conectado com sucesso.")
                self.connected = True
            else:
                print("[CLP] FALHA ao ao conectar clp.")
                self.connected = False
                self.reconnect()
        except Exception as e:
            print(f"[CLP] ERRO ao conectar ao CLP: {e}")
            self.connected = False
            self.reconnect()


    def read_process_variables(self):
        if not self.connected:
            self.connect()
            return
        
        try:
            # Leitura das variáveis do CLP
            # Os endereços e tipos de dados devem ser ajustados conforme configuração do CLP
            store_flag = self.read_bool(db_number=DB_NUMBER, start_byte=60, bit_number=0)
            IDProdlVal = self.read_string(db_number=DB_NUMBER, start_byte=0, max_length = 20)
            CODCorrVal = self.read_string(db_number=DB_NUMBER, start_byte=22,max_length = 20)
            temperatura_forno = self.read_real(db_number=DB_NUMBER, start=52)
            pressao_carga = self.read_real(db_number=DB_NUMBER, start=44)
            corrente_motor = self.read_real(db_number=DB_NUMBER, start=48)
            altura_matriz = self.read_real(db_number=DB_NUMBER, start=56)

            #print all variables read
            print(f"store_flag: {store_flag}, IDProdlVal: {IDProdlVal}, CODCorrVal: {CODCorrVal}, temperatura_forno: {temperatura_forno}, pressao_carga: {pressao_carga}, corrente_motor: {corrente_motor}, altura_matriz: {altura_matriz}")
            
            return {
                'time_stamp': datetime.now(),
                'store_flag': store_flag,
                'IDProdlVal': IDProdlVal,
                'CODCorrVal': CODCorrVal,
                'temperatura_forno': temperatura_forno,
                'pressao_carga': pressao_carga,
                'corrente_motor': corrente_motor,
                'altura_Matriz': altura_matriz
            }
            
        except Exception as e:
            print(f"[CLP] Erro na leitura das variaveis CLP: {e}")
            self.connected = False
            return None
    




    def read_string(self, db_number, start_byte, max_length=254):
        """
        Lê uma string do DB no CLP Siemens utilizando a função utilitária get_string.

        - db_number: número do DB
        - start_byte: byte inicial da string
        - max_length: número máximo de caracteres definidos para a string (default = 254)

        Retorna:
            String lida a partir do DB.
        """
        # +2 bytes de cabeçalho padrão do tipo STRING no Siemens (max_length + atual_length)
        data = self.client.db_read(db_number, start_byte, max_length + 2)
        return snap7.util.get_string(data, 0)
    
    def read_real(self, db_number, start):
        """
        Lê um valor real (REAL - 4 bytes, ponto flutuante IEEE 754) do DB no CLP Siemens.

        - db_number: número do DB
        - start_byte: byte inicial da variável
        """
        data = self.client.db_read(db_number, start, 4)
        return snap7.util.get_real(data, 0)
    
    def read_bool(self, db_number, start_byte, bit_number):
        """
        Lê um valor booleano (BOOL - 1 bit) do DB no CLP Siemens.

        - db_number: número do DB
        - start_byte: byte onde o bit está localizado
        - bit_number: número do bit (0 a 7) dentro do byte
        """
        data = self.client.db_read(db_number, start_byte, 1)
        return snap7.util.get_bool(data, 0, bit_number)
    
    def reconnect(self):
        print("[CLP] Tentando reconectar...")
        try:
            self.client.disconnect()
        except:
            pass
        time.sleep(5)  # Tempo de espera antes de tentar novamente
        self.connect()
    
    def disconnect(self):
        if self.connected:
            self.client.disconnect()
            self.connected = False