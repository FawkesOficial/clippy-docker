from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from requests import Session
import logging as log

def session_mount(reset:bool = False):
    global session
    if not globals().get('_session_initialized') or reset:
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

        globals()['_session_initialized'] = True
        log.debug("Session mounted successfully.")

domain='https://clip.fct.unl.pt'

session_mount()
log.info("Config loaded.")