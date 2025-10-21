# /service.py - VERSION DEBUG SIMPLE
import win32serviceutil
import win32service
import win32event
import servicemanager
import sys
import time
import logging
from pathlib import Path

class MetasearchAPIService(win32serviceutil.ServiceFramework):
    _svc_name_ = "MetasearchAPIService"
    _svc_display_name_ = "Metasearch API Service"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        
        # Setup logging IMMÉDIATEMENT
        log_file = Path(__file__).parent / "logs" / "debug_simple.log"
        log_file.parent.mkdir(exist_ok=True)
        
        logging.basicConfig(
            filename=str(log_file),
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filemode='w'
        )
        
        logging.info("=== SERVICE DEBUG INIT ===")
        logging.info(f"Service initialisé, PID: {win32service.GetCurrentProcessId()}")

    def SvcStop(self):
        logging.info("=== SERVICE STOP DEMANDÉ ===")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        logging.info("=== SERVICE STOP OK ===")

    def SvcRun(self):
        try:
            logging.info("=== SERVICE RUN DÉBUT ===")
            servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                                servicemanager.PYS_SERVICE_STARTED,
                                (self._svc_name_, ''))
            
            logging.info("Signal SERVICE_RUNNING envoyé")
            
            # JUSTE ATTENDRE - pas de FastAPI pour l'instant
            counter = 0
            while True:
                # Attendre le signal stop OU 10 secondes
                result = win32event.WaitForSingleObject(self.hWaitStop, 10000)
                
                if result == win32event.WAIT_OBJECT_0:
                    logging.info("Signal STOP reçu, arrêt du service")
                    break
                
                # Sinon, juste logger qu'on est vivant
                counter += 1
                logging.info(f"Service actif - cycle {counter}")
                
                if counter > 100:  # Éviter les logs infinis
                    logging.info("Service stable depuis 1000 secondes")
                    break
            
            logging.info("=== SERVICE RUN FIN ===")
            
        except Exception as e:
            logging.error(f"ERREUR dans SvcRun: {e}")
            import traceback
            logging.error(f"Traceback: {traceback.format_exc()}")
            raise

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MetasearchAPIService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(MetasearchAPIService)

