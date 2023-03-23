
from typing import Dict, Union, Optional, List

import jsonpickle

from Domain.masina import Masina
from utils import get_random_string


class MasinaRepository:

    def __init__(self, filename):
        self.filename = filename

    def __read_file(self):
        try:
            with open(self.filename, 'r') as f:
                return jsonpickle.loads(f.read())
        except Exception:
            return {}

    def __write_file(self, objects: Dict[str, Masina]):
        with open(self.filename, 'w') as f:
            f.write(jsonpickle.dumps(objects))

    def create(self, masina: Masina) -> None:
        """
        Adauga o masina in "baza de date"
        :param car:masina pe care dorim sa o adaugam
        :return:None
        """

        masini = self.__read_file()
        if self.read(masina.id_entity) is not None:
            raise KeyError(f'Exista deja o masina cu id {masina.id_entity}.')

        masini[masina.id_entity] = masina
        self.__write_file(masini)

    def read(self, id_masina=None) -> Union[Optional[Masina], List[Masina]]:
        """
        Citeste o masina din "baza de date"
        :param id_masina:id-ul masini pe care dorim sa o citim
        :return: masina cu id-ul id_masina
                lista cu toate masinile daca id-ul masinii nu exista
        """

        masini = self.__read_file()
        if id_masina:
            if id_masina in masini:
                return masini[id_masina]
            else:
                return None

        return list(masini.values())

    def update(self, masina: Masina) -> None:
        """
        Actualizeaza o masina din "baza de date"
        :param masina:masina pe care dorim sa o actualizam
        :return:None
        """

        masini = self.__read_file()
        if self.read(masina.id_entity) is None:
            id = masina.id_entity
            msg = f'Nu exista o masina cu id-ul {id} de actualizat.'
            raise KeyError(msg)

        masini[masina.id_entity] = masina
        self.__write_file(masini)

    def delete(self, id_masina: str) -> None:
        """
        Sterge o masina din "baza de date"
        :param id_masina:id-ul masinii pe care dorim sa o stergem
        :return:None
        """
        masini = self.__read_file()
        if self.read(id_masina) is None:
            raise KeyError(f'Nu exista o masina cu id {id_masina} de sters.')

        del masini[id_masina]
        self.__write_file(masini)
