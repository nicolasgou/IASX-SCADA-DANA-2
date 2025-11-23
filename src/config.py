###############################################################################
### PLC Configuration
###############################################################################
PLC_IP = '192.168.15.9' # IP CPL Siemens
PLC_RACK = 0            # geralmente 0 para S7-1200
PLC_SLOT = 1            # geralmente 1 para S7-1200
DB_NUMBER = 2           # DB onde as variáveis do processo estão armazenadas

SB_STORE_FLAG = 60      # Start byte for STORE_FLAG boolean 
BN_STORE_FLAG=0         # Bit number for STORE_FLAG boolean

SB_ID_PROD = 0          # Start byte for ID_PROD string
ML_ID_PROD=20           # Max length for ID_PROD string

SB_COD_CORR = 22        # Start byte for COD_CORR string
ML_COD_CORR=20          # Max length for COD_CORR string

SB_TEMP_FORNO = 52      # Start byte for Real variable temperature
SB_PRESSAO_CARGA = 44   # Start byte for Real variable pressure
SB_CORRENTE_MOTOR = 48  # Start byte for Real variable current
SB_ALTURA_MATRIZ = 56   # Start byte for Real variable height

###############################################################################
### BD configuration
###############################################################################
BD_USER="root",
BD_PASSWORD="T3cn0log!@",
BD_HOST="192.168.0.130",
BD_DATABASE="scada_dana"

DB_CONFIG = {
    'host': '192.168.0.130',
    'user': 'root',
    'password': 'T3cn0log!@',
    'database': 'scada_dana'
}

###############################################################################
### App Configuration
###############################################################################
TIMER = 1               #periodicidade da atualizacao de dados em segs
FRAME_WIDTH = 300
APP_SIZE = (1920, 1080)


FONT_FACTOR = 1         # somente numeros inteiros positivos
PV_FONT_SIZE = 18       # Tamanho da fonte para os valores das variáveis de processo, ORI: 18    
UNIT_FONT_SIZE = 14     # Tamanho da fonte para as unidades das variáveis de processo, ORI: 14

TITLE_FONT_SIZE = 20    # Tamanho da fonte para os títulos das seções, ORI: 20



FRA_PROC_ATUAL_WIDTH = 160  # Largura do frame de processo atual, ORI: 20
FRA_TEMP_FORNO_WIDTH = 100    # Largura do frame de temperatura do forno, ORI: 20
FRA_PRESS_CARG_WIDTH = 100    # Largura do frame de pressão da carga, ORI: 20
FRA_MOTOR_AMPS_WIDTH = 100    # Largura do frame de corrente do motor,  ORI: 20
FRA_MATRIX_ALT_WIDTH = 100    # Largura do frame de altura da matriz,       ORI: 20
