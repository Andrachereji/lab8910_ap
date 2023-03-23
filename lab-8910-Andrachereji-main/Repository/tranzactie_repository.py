from typing import Dict, Union, Optional, List

import jsonpickle

from Domain.tranzactie import Tranzactie
from Repository.masina_repository import MasinaRepository


class TranzactieRepository:

    def __init__(self, filename):
        self.filename = filename

    def __read_file(self):
        try:
            with open(self.filename, 'r') as f:
                return jsonpickle.loads(f.read())
        except Exception:
            return {}

    def __write_file(self, objects: Dict[str, Tranzactie]):
        with open(self.filename, 'w') as f:
            f.write(jsonpickle.dumps(objects))

    def create(self, tranzactie: Tranzactie) -> None:
        """
        Adauga o tranzactie in "baza de date"
        :param tranzactie:tranzactia pe care dorim sa o adaugam
        :return:None
        """

        tranzactii = self.__read_file()
        if self.read(tranzactie.id_entity) is not None:
            id = tranzactie.id_entity
            raise KeyError(f'Exista deja o tranzactie cu id {id}.')
        tranzactii[tranzactie.id_entity] = tranzactie
        self.__write_file(tranzactii)

    def read(self, id_tranzactie=None):
        """
        Citeste o tranzactie din "baza de date"
        :param id_tranzactie:id-ul tranzactiei pe care dorim sa o citim
        :return:tranzactia cu id-ul id_tranzactie
               lista cu toate tranzactiile daca id-ul tranzactiei nu exista
        """

        tranzactii = self.__read_file()
        if id_tranzactie:
            if id_tranzactie in tranzactii:
                return tranzactii[id_tranzactie]
            else:
                return None

        return list(tranzactii.values())

    def update(self, tranzactie: Tranzactie) -> None:
        """
        Actualizeaza o tranzactie din "baza de date"
        :param tranzactie:tranzactia pe care dorim sa o actualizam
        :return:None
        """

        tranzactii = self.__read_file()
        if self.read(tranzactie.id_entity) is None:
            id = tranzactie.id_entity
            msg = f'Nu exista o tranzactie cu id {id} de actualizat.'
            raise KeyError(msg)

        tranzactii[tranzactie.id_entity] = tranzactie
        self.__write_file(tranzactii)

    def delete(self, id_tranzactie: str) -> None:
        """
        Sterge o tranzactie din "baza de date"
        :param id_tranzactie:id-ul tranzactiei pe care dorim sa o stergem
        :return:None
        """
        tranzactii = self.__read_file()
        if self.read(id_tranzactie) is None:
            raise KeyError(f'Nu exista tranzactie cu id {id_tranzactie} '
                           f'de sters.')
        del tranzactii[id_tranzactie]
        self.__write_file(tranzactii)
