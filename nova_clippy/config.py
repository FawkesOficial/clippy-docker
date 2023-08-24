from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from requests import Session
import logging as log
import configparser
from pathlib import Path
from InquirerPy import inquirer
from appdirs import user_data_dir

# TODO dynamically store and load a config file like:
#cfg = {s:dict(config.items(s)) for s in config.sections()}

def load_config():
    """Load a basic user config."""
    cfgpath = Path(user_data_dir("clippy")) / "config.ini"
    if Path.is_file(cfgpath):
        log.info(f"Ficheiro de configuração encontrado: {cfgpath}")
        try:
            config = configparser.ConfigParser()
            config.read(cfgpath)
            try: username = config.get("Credenciais","username")
            except configparser.NoOptionError: username = None
            try: password = config.get("Credenciais","password")
            except configparser.NoOptionError: password = None
            return username, password
        except configparser.MissingSectionHeaderError:
            return None, None
    else:
        log.info("Nenhum ficheiro de configuração encontrado.")
    return None, None

def save_config():
    """Save a basic user config."""
    global username, password
    cfgpath = Path(user_data_dir("clippy")) / "config.ini"
    config = configparser.ConfigParser()
    try:
        config.read(cfgpath)
    except FileNotFoundError:
        pass
    except configparser.MissingSectionHeaderError:
        pass
    
    if (not Path.is_file(cfgpath) or "Credenciais" not in config.sections() or username != config.get("Credenciais","username") or password != config.get("Credenciais","password") ) and inquirer.confirm(
        message="Guardar credenciais em sistema para a próxima vez?",
        default=True,
        confirm_letter="s",
        reject_letter="n",
        transformer=lambda result: "Sim" if result else "Não",
    ).execute():
        config['Credenciais'] = {"username": username, "password": password}
        Path.mkdir(cfgpath.parent, parents=True, exist_ok=True)
        with open(cfgpath, 'w+') as configfile:
            config.write(configfile)
            print(f"Ficheiro de configuração guardado em: '{cfgpath}'")

def update_credentials(new_user, new_password):
    """Update saved credentials."""
    global username, password
    username = new_user
    password = new_password

# Multithreading
MAX_THREADS = 8

def session_mount():
    global session
    #Implement auto retry
    retry_strategy = Retry(
        total=3,  # Number of total retries (including the initial request)
        backoff_factor=0.3,  # Factor to apply exponential backoff between retries
        status_forcelist=[500, 502, 503, 504],  # HTTP status codes to retry
    )

    # Create a custom HTTP adapter with the retry strategy
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    log.debug("Session mounted successfully.")

# Domain
domain='https://clip.fct.unl.pt'

session_mount()
username, password = load_config()
log.info("Config.py loaded.")