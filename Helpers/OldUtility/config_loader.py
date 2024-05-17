from Helpers.globals import get_config
import json
from typing import Optional, Tuple
from dotenv import dotenv_values,load_dotenv

_config: Optional[dict] = None

def load_config() -> Tuple[str, str, int, str, str, str]:
    global _config
    if _config is None:
        try:
            config = dotenv_values(dotenv_path=r"Settings\Environments\.env.dev")  # get the config variable from the file
            _config = {
                "database": {
                    "hostname": config["DATABASE_HOST"],
                    "port": int(config["DATABASE_PORT"]),
                    "username": config["DATABASE_USER"],
                    "password": config["DATABASE_PASSWORD"],
                    "database": config["DATABASE_NAME"],
                }
            }
        except (FileNotFoundError, json.JSONDecodeError):
            raise Exception("Unable to load config from config.json")
    if _config is None:
        raise Exception("Config is not loaded")
    
    try:
        db_host = _config['database']['hostname']
        db_port = _config['database']['port']
        db_user = _config['database']['username']
        db_pass = _config['database']['password']
        db_name = _config['database']['database']
    except KeyError as e:
        raise Exception(f"Missing configuration value: {e}")

    return db_host, db_port, db_user, db_pass, db_name
