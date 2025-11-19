import mysql.connector
from mysql.connector import errorcode
from datetime import datetime

from src.config import DB_CONFIG

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        try:
            # Tenta conectar diretamente ao banco especificado
            self.connection = mysql.connector.connect(**DB_CONFIG)
            if self.connection:
                print("[BD] Conexao com banco de dados estabelecida")
            else:
                print("[BD] Sem conexão com o banco; dados não serão armazenados.")
        except mysql.connector.Error as e:
            print(f"[BD] Erro ao conectar ao mysql.connector: {e}")
            self.connection = None

    def store_process_data(self, data):
        if not self.connection:
            self.connect()
            return
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """
                INSERT INTO historico 
                (time_stamp, temperatura_forno, pressao_carga, corrente_motor, altura_Matriz)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    data['time_stamp'],
                    data['temperatura_forno'],
                    data['pressao_carga'],
                    data['corrente_motor'],
                    data['altura_Matriz']
                ),
            )
            self.connection.commit()
        except mysql.connector.Error as e:
            print(f"[BD] Erro ao armazenar dados: {e}")
            
    def get_historical_data(self, start_date, end_date):
        if not self.connection:
            return []
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """
                SELECT * FROM historico 
                WHERE time_stamp BETWEEN %s AND %s
                ORDER BY time_stamp DESC
                """,
                (start_date, end_date),
            )
            return cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"[BD] Erro ao recuperar dados históricos: {e}")
            return []
            
    def close(self):
        if self.connection:
            self.connection.close()

