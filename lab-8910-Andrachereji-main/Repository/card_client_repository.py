from typing import Dict, Union, Optional, List

import jsonpickle

from Domain.card_client import Card_client


class Card_clientRepository:

    def __init__(self, filename):
        self.filename = filename

    def __read_file(self):
        try:
            with open(self.filename, 'r') as f:
                return jsonpickle.loads(f.read())
        except Exception:
            return {}

    def __write_file(self, objects: Dict[str, Card_client]):
        with open(self.filename, 'w') as f:
            f.write(jsonpickle.dumps(objects))

    def create(self, card_client: Card_client) -> None:
        """
        Adauga un card nou in "baza de date"
        :param card_client:cardul care trebuie adaugat
        :return:None
        """
        carduri_clienti = self.__read_file()
        id = card_client.id_entity
        if self.read(card_client.id_entity) is not None:
            raise KeyError(f'Exista deja un card cu id {id}.')
        for card in carduri_clienti:
            if card_client.cnp == carduri_clienti[card].cnp:
                raise KeyError('Cnp-ul nu este unic')
        carduri_clienti[card_client.id_entity] = card_client
        self.__write_file(carduri_clienti)

    def read(self, id_card_client=None):
        """
        Citeste un card din "baza de date"
        :param id_card_client:id-ul cardului pe care dorim sa il citim
        :return:-cardul cu id-ul id_card_client
                -lista cu toate cardurile daca id-ul cardului nu exista
        """

        carduri_clienti = self.__read_file()
        if id_card_client:
            if id_card_client in carduri_clienti:
                return carduri_clienti[id_card_client]
            else:
                return None

        return list(carduri_clienti.values())

    def update(self, card_client: Card_client) -> None:
        """
        Actualizeaza un card din "baza de date"
        :param card_client:cardul care trebuie actualizat
        :return:None
        """

        carduri_clienti = self.__read_file()
        id = card_client.id_entity
        if self.read(id) is None:
            msg = f'Nu exista un card  cu id-ul {id} de actualizat.'
            raise KeyError(msg)

        carduri_clienti[id] = card_client
        self.__write_file(carduri_clienti)

    def delete(self, id_card_client: str) -> None:
        """
        Sterge un card din "baza de date"
        :param id_card_client:id-ul cardului care trebuie sters
        :return:None
        """
        carduri_clienti = self.__read_file()
        if self.read(id_card_client) is None:
            raise KeyError(
                f'Nu exista un card cu id-ul {id_card_client} de sters.')

        del carduri_clienti[id_card_client]
        self.__write_file(carduri_clienti)
