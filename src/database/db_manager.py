import mysql.connector
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                user="user",
                password="password",
                host="localhost",
                database="scada_dana"
            )
            print("Conexão com banco de dados estabelecida")
        except mysql.connector.Error as e:
            print(f"Erro ao conectar ao mysql.connector: {e}")
            
    def create_tables(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS historico (
                    time_stamp DATETIME PRIMARY KEY,
                    temperatura_forno FLOAT,
                    pressao_carga FLOAT,
                    corrente_motor FLOAT,
                    altura_Matriz FLOAT
                )
            """)
            self.connection.commit()
        except mysql.connector.Error as e:
            print(f"Erro ao criar tabela: {e}")
            
    def store_process_data(self, data):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO historico 
                (time_stamp, temperatura_forno, pressao_carga, corrente_motor, altura_Matriz)
                VALUES (?, ?, ?, ?, ?)
            """, (
                data['time_stamp'],
                data['temperatura_forno'],
                data['pressao_carga'],
                data['corrente_motor'],
                data['altura_Matriz']
            ))
            self.connection.commit()
        except mysql.connector.Error as e:
            print(f"Erro ao armazenar dados: {e}")
            
    def get_historical_data(self, start_date, end_date):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT * FROM historico 
                WHERE time_stamp BETWEEN ? AND ?
                ORDER BY time_stamp DESC
            """, (start_date, end_date))
            return cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Erro ao recuperar dados históricos: {e}")
            return []
            
    def close(self):
        if self.connection:
            self.connection.close()