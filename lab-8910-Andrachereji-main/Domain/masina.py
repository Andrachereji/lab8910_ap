from dataclasses import dataclass

from Domain.entity import Entity


@dataclass
class Masina(Entity):
    '''
    Creeaza o masina
    -id_masina:id-ul masinii care este unic
    -model:modelul masinii
    an_achizitie:anul achizitiei care trebuie sa fie pozitiv
    nr_km:numarul de km care trebuie sa fie pozitiv
    in_garantie: "Da" daca masina este inca in garantie sau "Nu" in caz contrar
    '''

    model: str
    an_achizitie: int
    nr_km: float
    in_garantie: str
