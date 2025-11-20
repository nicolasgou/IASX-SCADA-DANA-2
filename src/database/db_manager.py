import mysql.connector
from mysql.connector import errorcode
from datetime import datetime

from src.config import DB_CONFIG

class DatabaseManager:
    def __init__(self):
        self.DB_client = None
        self.DBconnection = False
        self.connect()
    
    def connect(self):
        try:
            # Tenta conectar diretamente ao banco especificado
            self.DB_client = mysql.connector.connect(**DB_CONFIG)
            if self.DB_client:
                print("[BD] Conexao com banco de dados estabelecida")
                self.DBconnection = True
            else:
                print("[BD] Sem conexão com o banco; dados não serão armazenados.")
                self.DBconnection = False
        except mysql.connector.Error as e:
            print(f"[BD] Erro ao conectar ao mysql.connector: {e}")
            self.DBconnection = False

    def check_db_connection(self):
        if not self.DB_client.is_connected():
            print("[BD] Disconected")
            self.DBconnection = False
            try:
                print("[BD] Trying to reconnect...")
                self.DB_client.reconnect(attempts=3, delay=2)
                self.DBconnection = True
                print("[BD] Reconnected!")
            except:
                self.DBconnection = False
                print("[BD] Reconnection failed.")
        else:
            #print("[BD] Connected")
            self.DBconnection = True


    def store_process_data(self, data):
        if not self.DB_client:
            self.connect()
            return
        try:
            cursor = self.DB_client.cursor()
            cursor.execute(
                """
                INSERT INTO historico 
                (time_stamp, IDProduto, CODCorrida, temperatura_forno, pressao_carga, corrente_motor, altura_Matriz)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    data['time_stamp'],
                    data['IDProduto'],
                    data['CODCorrida'],
                    data['temperatura_forno'],
                    data['pressao_carga'],
                    data['corrente_motor'],
                    data['altura_Matriz']
                ),
            )
            self.DB_client.commit()
            print(f"[BD] Dados Armazenados com sucesso")
        except mysql.connector.Error as e:
            print(f"[BD] Erro ao armazenar dados: {e}")
            
    def get_historical_data(self, start_date, end_date):
        if not self.DB_client:
            return []
        try:
            cursor = self.DB_client.cursor()
            cursor.execute(
                """
                SELECT * FROM historico 
                WHERE time_stamp BETWEEN %s AND %s
                ORDER BY time_stamp DESC
                """,
                (start_date, end_date),
            )
            print(f"[BD] Dados obtidos com sucesso")
            return cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"[BD] Erro ao recuperar dados históricos: {e}")
            return []
            
    def close(self):
        if self.DB_client:
            self.DB_client.close()

