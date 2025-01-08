import requests
from contextlib import suppress


def get_data_yugioh(petition: str):
    """
    Función en común para usar en las funciones
    url_cropped y card_list_archetype
    
    Warns
    -----
    No recomiendo usar solo esta función ya que devuelve
    todos los datos del diccionario y cambia dependiendo que pides
    
    Parameters
    ----------
    petition: str
        para ver si es name o archetype,
        de ahí se usa distintas:
            para url_cropped = peticion=f"name={name_monster}"
            para card_list_archetype = peticion=f"archetype={archetype}"
    """
    
    global data
    
    url = "https://db.ygoprodeck.com/api/v7/cardinfo.php?{}".format(petition)
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()["data"]
    else:
        print(f"Error {response.status_code}")
        print(response.json()["error"])


def url_cropped(name_card: str):
    """
    Devuelve la ruta de la imagen completa del arte para poder descargarla
    
    Warns
    -----
    Favor buscar antes el nombre correcto o
    usar antes la función card_list_archetype
    y descargarlo en la pc a mano, las reglas de la api no deja descargar
    directo la imagen ni usar la url para guardarlo, y recomienda
    guardar la imagen en una base de datos que el usuario maneje
    
    Notes
    -----
    Usar la carta insignia del arquetipo en cuestión,
    eso puede ser a gusto o en consenso que usan otras plataformas
    para identificar el arquetipo
    
    Parameters
    ----------
    name_monster: str
        Nombre de la mounstro en inglés, 
        la api no hace distinción al uso de mayúsculas y minúsculas
    
    Warnings
    -----
    NameError al usar función get_data_yugioh e intentar usar
    la variable data pero el status_code no es 200
    """
    
    global data
    
    petition = f"name={name_card}"
    get_data_yugioh(petition)
    
    with suppress(NameError):
        cropped = data[0]["card_images"][0]["image_url_cropped"]
        print(f'La imagen de la carta {name_card} es:\n')
        print(cropped)


def card_list_archetype(archetype: str):
    """
    Lista el nombre de las cartas que tiene el arquetipo
    Ayuda para usar la función url_cropped que necesita el nombre de
    la carta de mounstro
    
    Parameters
    ----------
    archetype: str
        Nombre del arquetipo en inglés,
        la api no hace distinción al uso de mayúsculas y minúsculas
    
    Warns
    -----
    * NameError al usar función get_data_yugioh e intentar usar
    la variable data pero el status_code no es 200
    * No usar for con las dos funciones porque la api
    tiene límite de peticiones por segundo
    """
    
    global data
    
    petition = f"archetype={archetype}"
    get_data_yugioh(petition)
    
    with suppress(NameError):
        print(f'El arquetipo {archetype} contiene estas cartas:\n')
        for card in data:
            print(card['name'])