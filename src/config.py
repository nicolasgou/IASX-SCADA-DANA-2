# PLC Configuration
PLC_IP = '192.168.0.10'   # CPL Siemens bancada
PLC_RACK = 0                 # geralmente 0 para S7-1200
PLC_SLOT = 1                 #geralmente 1 para S7-1200
DB_NUMBER = 2              # DB onde as variáveis do processo estão armazenadas


#BD configuration
BD_USER="root",
BD_PASSWORD="T3cn0log!@",
BD_HOST="localhost",
BD_DATABASE="scada_dana"

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'T3cn0log!@',
    'database': 'scada_dana'
}


#App Configuration

TIMER = 1               #periodicidade da atualizacao de dados em segs
FRAME_WIDTH = 300
APP_SIZE = (1920, 1080)
IMAGE_SIZE = (640, 480)
IMAGE_SIZE_TRAIN = (64, 64)
CLASS_DIR_PATH = "./data/classes"
FEATURES_PATH = './data/features.csv'