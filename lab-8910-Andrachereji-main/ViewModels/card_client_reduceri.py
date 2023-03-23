from dataclasses import dataclass


@dataclass
class Card_clientReducere:
    nume: str
    prenume: str
    cnp: str
    data_nasterii: str
    data_inregistrarii: str
    suma_reducere: float
