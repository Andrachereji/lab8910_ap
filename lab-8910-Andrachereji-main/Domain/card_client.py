from dataclasses import dataclass

from Domain.entity import Entity


@dataclass
class Card_client(Entity):
    '''
    Creeaza cardul unui client
    -id_card_client:id-ul cardului care trebuie sa fie unic
    -nume:numele clientului
    -prenume:prenumele clientului
    -cnp:cnp-ul clientului care trebuie sa fie unic
    -data_nasterii:data nasterii clientului
    -data_inregistrarii:data inregistrarii cardului
    '''

    nume: str
    prenume: str
    cnp: str
    data_nasterii: str
    data_inregistrarii: str
