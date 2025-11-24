"""
Carrega as configuracoes da aplicacao a partir de um arquivo externo ".config"
localizado no mesmo diretorio do executavel. Se o arquivo nao existir ou se
algum valor nao puder ser convertido, os padroes deste arquivo sao usados.
"""
from pathlib import Path
from typing import Any, Callable, Dict
import sys


def _app_dir() -> Path:
    """Retorna o diretorio do executavel ou do script principal."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(sys.argv[0]).resolve().parent


def _parse_tuple_ints(value: str) -> tuple[int, int]:
    parts = value.replace("x", ",").split(",")
    nums = [int(p.strip()) for p in parts if p.strip()]
    if len(nums) != 2:
        raise ValueError("Esperado dois inteiros separados por ',' ou 'x'")
    return nums[0], nums[1]


def _load_file(config_path: Path) -> Dict[str, str]:
    if not config_path.is_file():
        print(f"[Config] Arquivo {config_path} nao encontrado; usando padroes.")
        return {}

    data: Dict[str, str] = {}
    for line in config_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith(";"):
            continue
        if "=" not in stripped:
            continue
        key, raw_value = stripped.split("=", 1)
        data[key.strip()] = raw_value.strip().strip('"').strip("'")
    return data


def _apply_casts(defaults: Dict[str, Any], overrides: Dict[str, str]) -> Dict[str, Any]:
    casters: Dict[str, Callable[[str], Any]] = {
        # PLC
        "PLC_IP": str,
        "PLC_RACK": int,
        "PLC_SLOT": int,
        "DB_NUMBER": int,
        "SB_STORE_FLAG": int,
        "BN_STORE_FLAG": int,
        "SB_ID_PROD": int,
        "ML_ID_PROD": int,
        "SB_COD_CORR": int,
        "ML_COD_CORR": int,
        "SB_TEMP_FORNO": int,
        "SB_PRESSAO_CARGA": int,
        "SB_CORRENTE_MOTOR": int,
        "SB_ALTURA_MATRIZ": int,
        # DB
        "BD_USER": str,
        "BD_PASSWORD": str,
        "BD_HOST": str,
        "BD_DATABASE": str,
        # App
        "TIMER": int,
        "APP_SIZE": _parse_tuple_ints,
        "PV_FONT_SIZE": int,
        "UNIT_FONT_SIZE": int,
        "TITLE_FONT_SIZE": int,
        "FRA_PROC_ATUAL_WIDTH": int,
        "FRA_TEMP_FORNO_WIDTH": int,
        "FRA_PRESS_CARG_WIDTH": int,
        "FRA_MOTOR_AMPS_WIDTH": int,
        "FRA_MATRIX_ALT_WIDTH": int,
    }

    final = defaults.copy()
    for key, raw in overrides.items():
        if key not in defaults:
            continue
        caster = casters.get(key, str)
        try:
            final[key] = caster(raw)
        except Exception:
            print(f"[CONFIG] Falha ao converter '{key}'='{raw}'. Usando padrao.")
    return final


###############################################################################
### Valores padrao
###############################################################################
DEFAULTS: Dict[str, Any] = {
    # PLC
    "PLC_IP": "192.168.0.10",
    "PLC_RACK": 0,
    "PLC_SLOT": 1,
    "DB_NUMBER": 2,
    "SB_STORE_FLAG": 60,
    "BN_STORE_FLAG": 0,
    "SB_ID_PROD": 0,
    "ML_ID_PROD": 20,
    "SB_COD_CORR": 22,
    "ML_COD_CORR": 20,
    "SB_TEMP_FORNO": 52,
    "SB_PRESSAO_CARGA": 44,
    "SB_CORRENTE_MOTOR": 48,
    "SB_ALTURA_MATRIZ": 56,
    # DB
    "BD_USER": "root",
    "BD_PASSWORD": "T3cn0log!@",
    "BD_HOST": "localhost",
    "BD_DATABASE": "scada_dana",
    # App
    "TIMER": 5,
    "APP_SIZE": (1920, 1080),
    "PV_FONT_SIZE": 18,
    "UNIT_FONT_SIZE": 14,
    "TITLE_FONT_SIZE": 20,
    "FRA_PROC_ATUAL_WIDTH": 160,
    "FRA_TEMP_FORNO_WIDTH": 100,
    "FRA_PRESS_CARG_WIDTH": 100,
    "FRA_MOTOR_AMPS_WIDTH": 100,
    "FRA_MATRIX_ALT_WIDTH": 100,
}


###############################################################################
### Carga do arquivo .config
###############################################################################
CONFIG_PATH = _app_dir() / ".config"
_overrides = _load_file(CONFIG_PATH)
_config = _apply_casts(DEFAULTS, _overrides)

# Expor variaveis como antes
PLC_IP = _config["PLC_IP"]
PLC_RACK = _config["PLC_RACK"]
PLC_SLOT = _config["PLC_SLOT"]
DB_NUMBER = _config["DB_NUMBER"]
SB_STORE_FLAG = _config["SB_STORE_FLAG"]
BN_STORE_FLAG = _config["BN_STORE_FLAG"]
SB_ID_PROD = _config["SB_ID_PROD"]
ML_ID_PROD = _config["ML_ID_PROD"]
SB_COD_CORR = _config["SB_COD_CORR"]
ML_COD_CORR = _config["ML_COD_CORR"]
SB_TEMP_FORNO = _config["SB_TEMP_FORNO"]
SB_PRESSAO_CARGA = _config["SB_PRESSAO_CARGA"]
SB_CORRENTE_MOTOR = _config["SB_CORRENTE_MOTOR"]
SB_ALTURA_MATRIZ = _config["SB_ALTURA_MATRIZ"]

BD_USER = _config["BD_USER"]
BD_PASSWORD = _config["BD_PASSWORD"]
BD_HOST = _config["BD_HOST"]
BD_DATABASE = _config["BD_DATABASE"]
DB_CONFIG = {
    "host": BD_HOST,
    "user": BD_USER,
    "password": BD_PASSWORD,
    "database": BD_DATABASE,
}

TIMER = _config["TIMER"]
APP_SIZE = _config["APP_SIZE"]
PV_FONT_SIZE = _config["PV_FONT_SIZE"]
UNIT_FONT_SIZE = _config["UNIT_FONT_SIZE"]
TITLE_FONT_SIZE = _config["TITLE_FONT_SIZE"]
FRA_PROC_ATUAL_WIDTH = _config["FRA_PROC_ATUAL_WIDTH"]
FRA_TEMP_FORNO_WIDTH = _config["FRA_TEMP_FORNO_WIDTH"]
FRA_PRESS_CARG_WIDTH = _config["FRA_PRESS_CARG_WIDTH"]
FRA_MOTOR_AMPS_WIDTH = _config["FRA_MOTOR_AMPS_WIDTH"]
FRA_MATRIX_ALT_WIDTH = _config["FRA_MATRIX_ALT_WIDTH"]

__all__ = list(DEFAULTS.keys()) + ["DB_CONFIG"]
