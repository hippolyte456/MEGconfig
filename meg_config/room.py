'''
TODO cahier des charges à définir avec Fosca
- It has to reduce the possibility of mistakes while letting access to all possible experiments configurations for the user.
- Robustness : 0 erreur possible sur les envois et receptions de trigger etc // moins grave sur les checks et fonctinnalités supplémentaire.
'''


CONFIG_PATH = "/home/hippolytedreyfus/Documents/meg_config/meg_config/config/hardware_config.yaml"
USER_CONFIG_PATH = "/home/hippolytedreyfus/Documents/meg_config/meg_config/config/user_config.yaml"


import yaml
from ._stim_pc import StimPC
from ._eyetracker import Eyelink
from ._response_buttons import ResponseButtons

#TODO : se renseigner sur ce qu'ils font à l'ICM : contacter l'ingé qui a surement eu le temps de faire ça ?
class MegRoom(): #Heritage ?
    ''' 
    Robust hardware configuration setup for the neurospin meg,
    with a great amount of verbosity, to be usefull to the user just before to start the session.
    
    This class has to be used by the meg experimenters. 
    It is an intermediary class of expyriments with the specific need / hardware setup of neurospin and requires a config file (yaml?)
    '''  

    def __init__(self, hardware_path, user_path):
        self.hardware_config = self._load_config(hardware_path)
        self.user_config = self._load_config(user_path)

        # Initialisation des sous-composants avec la config correspondante
        self.stim_pc = StimPC(self._parse_by_object("stim_pc"))
        self.eyetracker = Eyelink(self._parse_by_object("eyelink_system"))
        self.response_buttons = ResponseButtons(self._parse_by_object("response_buttons"))

        # Vérification initiale de la configuration
        self._pytest_config()

          
    def _load_config(self, file_path):
        """Charge un fichier YAML et retourne son contenu sous forme de dictionnaire."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return yaml.safe_load(file) or {}  # Retourne un dict vide en cas d'erreur
        except yaml.YAMLError as e:
            print(f"Erreur lors du chargement de {file_path} : {e}")
            return {}

    def _parse_by_object(self, key):
        """Récupère la section spécifique du fichier de configuration."""
        return self.hardware_config.get(key, {})  # Retourne le dictionnaire associé à 'key', ou un dict vide si absent

    # def _parse_by_object(self, key):
    #     """Récupère la section spécifique du fichier de configuration en fusionnant hardware et user config."""
    #     config = {}
    #     if key in self.hardware_config:
    #         config.update(self.hardware_config[key])
    #     if key in self.user_config:
    #         config.update(self.user_config[key])
    #     return config


    def _pytest_config(self):
        '''run all tests'''
        pass
        #HARDWARE
        # test port parallèles 
        # test des boutons réponses 
        # test de la bonne connexion et synchro de tous les equipements
        # SOFTWARE
        # data quality assessement
        # check de l'environnement python

    
    def show_all(self):
        '''Show all the hardware available in the room'''
        def recursive_print(obj, indent=0):
            for attr, value in obj.__dict__.items():
                if hasattr(value, "__dict__"):
                    print("  " * indent + f"{attr}:")
                    recursive_print(value, indent + 1)
                else:
                    print("  " * indent + f"{attr}: {value}")
        
        print("MEG Room Configuration:")
        recursive_print(self)
