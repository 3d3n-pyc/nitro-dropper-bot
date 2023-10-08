import json

class IsDict(Exception):
    """Erreur qui indique que la variable est un dictionnaire"""
    "Raise when path is not complete"
    def __init__(self):
        super().__init__('Path is not complete')

class PathError(Exception):
    """Erreur qui indique que le chemin n'est pas valide"""
    "Raise when end of path return None"
    def __init__(self):
        super().__init__('End of path return None')

default:dict = json.load(open('data/messages.json', encoding='utf-8'))

def get(variable:str, dictionary:dict=default) -> str:
    """Obtenir un message à partir d'un dictionnaire 

    Args:
        variable (str): Chemin du message (message.welcome)
        dictionary (dict): Dictionnaire où est référencé les messages

        {
            "message" : {
                "welcome" : "Salut"
            }
        }

    Raises:
        PathError: Erreur qui indique que le chemin n'est pas valide
        IsDict: Erreur qui indique que la variable est un dictionnaire

    Returns:
        str: Message en fonction du language
    """
    
    for value in variable.split('.'):
        if type(dictionary) == str:
            raise PathError
            
        dictionary = dictionary.get(value)

        if dictionary == None:
            raise PathError
    
    if type(dictionary) == dict:
        raise IsDict
    
    return dictionary