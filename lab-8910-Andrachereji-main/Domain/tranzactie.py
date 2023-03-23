from dataclasses import dataclass

from Domain.entity import Entity


@dataclass
class Tranzactie(Entity):
    '''
    Creeaza o tranzactie
    -id_tranzactie:id-ul tranzactie care trebuie sa fie unic
    -id_masina:id-ul masinii care trebuie sa existe
    -id_card_client:id-ul cardului care poate sa nu existe,
    dar daca exista se aplica o reducere de 10% pentru manopera
    -suma_piese:pretul pieselor,
    daca masina se afla in garantie atunci piesele sunt gratuite
    -suma manopera:pretul manoperei
    -data:data la care s-a facut tranzactia
    -ora:ora la care s-a facut tranzactia
    '''

    id_masina: str
    id_card_client: str
    suma_piese: float
    suma_manopera: float
    data: str
    ora: str
