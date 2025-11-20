import snap7
import time
from datetime import datetime

from src.config import PLC_IP, PLC_RACK, PLC_SLOT
from src.config import DB_NUMBER,SB_STORE_FLAG,BN_STORE_FLAG,SB_ID_PROD,ML_ID_PROD,SB_COD_CORR,ML_COD_CORR,SB_TEMP_FORNO,SB_PRESSAO_CARGA,SB_CORRENTE_MOTOR,SB_ALTURA_MATRIZ

class PLCClient:
    def __init__(self, ip=PLC_IP, rack=PLC_RACK, slot=PLC_SLOT):
        self.CLP_client = snap7.client.Client()
        self.ip = ip
        self.rack = rack
        self.slot = slot
        self.CLPconnection = False
        self.connect()
        
    def connect(self):
        try:
            if self.CLP_client.connect(self.ip, self.rack, self.slot):
                print("[CLP] Conectado com sucesso.")
                self.CLPconnection = True
            else:
                print("[CLP] FALHA ao conectar clp.")
                self.CLPconnection = False
        except Exception as e:
            print(f"[CLP] ERRO ao conectar ao CLP: {e}")
            self.CLPconnection = False

    # def check_clp_connection(self):
    #     if not self.CLP_client.get_connected(): # Sometimes returns True, while connection is lost. Nao usar!!
    #         print("[CLP] Desconectado")
    #         self.CLPconnection = False
    #         try:
    #             print("[CLP] Tentando reconectar...")
    #             self.reconnect()
    #         except Exception as e:
    #             print(f"[CLP] ERRO ao reconectar ao CLP: {e}")
    #             self.CLPconnection = False
    #             self.reconnect()
    #     else:
    #         print("[CLP] Conectado")
    #         self.CLPconnection = True

    def read_process_variables(self):
        if not self.CLPconnection:
            self.connect()
            return
        try:
            # Leitura das variáveis do CLP SB_STORE_FLAG = 60
            # Os endereços e tipos de dados devem ser ajustados conforme configuração do CLP
            store_flag = self.read_bool(db_number=DB_NUMBER, start_byte=SB_STORE_FLAG, bit_number=BN_STORE_FLAG)
            IDProduto = self.read_string(db_number=DB_NUMBER, start_byte=SB_ID_PROD, max_length = ML_ID_PROD)
            CODCorrida = self.read_string(db_number=DB_NUMBER, start_byte=SB_COD_CORR,max_length = ML_COD_CORR)
            temperatura_forno = self.read_real(db_number=DB_NUMBER, start=SB_TEMP_FORNO)
            pressao_carga = self.read_real(db_number=DB_NUMBER, start=SB_PRESSAO_CARGA)
            corrente_motor = self.read_real(db_number=DB_NUMBER, start=SB_CORRENTE_MOTOR)
            altura_matriz = self.read_real(db_number=DB_NUMBER, start=SB_ALTURA_MATRIZ)

            #print all variables read
            #print(f"store_flag: {store_flag}, IDProduto: {IDProduto}, CODCorrida: {CODCorrida}, temperatura_forno: {temperatura_forno}, pressao_carga: {pressao_carga}, corrente_motor: {corrente_motor}, altura_matriz: {altura_matriz}")
            self.CLPconnection = True
            return {
                'time_stamp': datetime.now(),
                'store_flag': store_flag,
                'IDProduto': IDProduto,
                'CODCorrida': CODCorrida,
                'temperatura_forno': temperatura_forno,
                'pressao_carga': pressao_carga,
                'corrente_motor': corrente_motor,
                'altura_Matriz': altura_matriz
            }
            
        except Exception as e:
            self.CLPconnection = False
            print(f"[CLP] Erro na leitura das variaveis CLP: {e}")
            self.reconnect()
            return {
                'time_stamp': None,
                'store_flag': False,
                'IDProduto': None,
                'CODCorrida': None,
                'temperatura_forno': None,
                'pressao_carga': None,
                'corrente_motor': None,
                'altura_Matriz': None
            }
    




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
        data = self.CLP_client.db_read(db_number, start_byte, max_length + 2)
        return snap7.util.get_string(data, 0)
    
    def read_real(self, db_number, start):
        """
        Lê um valor real (REAL - 4 bytes, ponto flutuante IEEE 754) do DB no CLP Siemens.

        - db_number: número do DB
        - start_byte: byte inicial da variável
        """
        data = self.CLP_client.db_read(db_number, start, 4)
        return snap7.util.get_real(data, 0)
    
    def read_bool(self, db_number, start_byte, bit_number):
        """
        Lê um valor booleano (BOOL - 1 bit) do DB no CLP Siemens.

        - db_number: número do DB
        - start_byte: byte onde o bit está localizado
        - bit_number: número do bit (0 a 7) dentro do byte
        """
        data = self.CLP_client.db_read(db_number, start_byte, 1)
        return snap7.util.get_bool(data, 0, bit_number)
    
    def reconnect(self):
        print("[CLP] Tentando reconectar...")
        try:
            self.CLP_client.disconnect()
        except:
            pass
        time.sleep(5)  # Tempo de espera antes de tentar novamente
        self.connect()
    
    def disconnect(self):
        self.CLP_client.disconnect()
        self.CLPconnection = False

