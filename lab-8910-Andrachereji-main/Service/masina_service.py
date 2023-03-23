import uuid
import random

from Domain.actualizare_garantie_operation import UpdateGarantieOperation
from Domain.add_operation import AddOperation
from Domain.delete_operation import DeleteOperation
from Domain.masina import Masina
from Domain.multiple_add_operation import MultipleAddOperation
from Domain.update_operation import UpdateOperation
from Domain.validator_masina import MasinaValidator
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService
from utils import get_random_string


class MasinaService:
    def __init__(self, masina_repository: Repository,
                 masina_validator: MasinaValidator,
                 undo_redo_service: UndoRedoService):
        self.masina_repository = masina_repository
        self.masina_validator = masina_validator
        self.undo_redo_service = undo_redo_service

    def adaugare_masina(self, id_masina, model,
                        an_achizitie, nr_km, in_garantie) -> None:
        '''
        Adauga o masina in masina_repository
        :param id_masina:id-ul masinii care se adauga
        :param model:modelul masinii
        :param an_achizitie:anul achizitiei
        :param nr_km:numarul de km
        :param in_garantie:ne spune daca masina mai este in garantie sau nu
        '''
        masina = Masina(id_masina, model,
                        an_achizitie, nr_km, in_garantie)
        self.masina_validator.validate(masina)
        self.masina_repository.create(masina)

        self.undo_redo_service.clear_redo()
        add_operation = AddOperation(self.masina_repository, masina)
        self.undo_redo_service.add_to_undo(add_operation)

    def update_masina(self, id_masina, model,
                      an_achizitie, nr_km, in_garantie) -> None:
        '''
        Actualizeaza o masina existenta in masina_repository
        :param id_masina:id-ul masinii care se actualizeaza
        :param model:modelul masinii
        :param an_achizitie:anul achizitiei
        :param nr_km:numarul de km
        :param in_garantie:ne spune daca masina mai
        este in garantie sau nu
        '''
        masina = self.masina_repository.read(id_masina)
        masina_updated = Masina(id_masina, model,
                                an_achizitie, nr_km, in_garantie)
        self.masina_validator.validate(masina_updated)
        self.masina_repository.update(masina_updated)

        self.undo_redo_service.clear_redo()
        update_operation = UpdateOperation(self.masina_repository,
                                           masina_updated, masina)
        self.undo_redo_service.add_to_undo(update_operation)

    def stergere_masina(self, id_masina) -> None:
        '''
        Sterge o masina din masina_repository
        :param id_masina: id-ul masinii care se sterge
        '''
        masina = self.masina_repository.read(id_masina)
        self.masina_repository.delete(id_masina)

        self.undo_redo_service.clear_redo()
        delete_operation = DeleteOperation(self.masina_repository, masina)
        self.undo_redo_service.add_to_undo(delete_operation)

    def get_all(self):
        '''
        Afiseaza toate masinile din repository
        :return: lista cu toate masinile
        '''
        return self.masina_repository.read()

    def random_cars(self, number) -> None:
        listBool = ["Nu", "Da"]
        undo_redo = []
        for i in range(number):
            id = str(uuid.uuid1())
            model = get_random_string(7)
            an_achizitie = random.randrange(1900, 2021, 4)
            nr_km = random.randrange(000000, 999999, 6)
            in_garantie = random.choice(listBool)
            masina = Masina(id, model, an_achizitie, nr_km, in_garantie)
            self.masina_validator.validate(masina)
            self.masina_repository.create(masina)
            undo_redo.append(masina)
        self.undo_redo_service.clear_redo()
        add_operation = MultipleAddOperation(self.masina_repository, undo_redo)
        self.undo_redo_service.add_to_undo(add_operation)

    def actualizare_garantie(self):
        '''
        Modifica garantia masinii astfel:
        daca km sunt mai putini de 60 000 si masina are mai
        putin de 3 ani de la achizitie: in garantie
        altfel:nu e in garantie
        '''
        masini = self.get_all()
        masini_updated = self.get_all()
        for masina in masini_updated:
            if (2021 - masina.an_achizitie) <= 3 and masina.nr_km <= 60000:
                masina.in_garantie = 'Da'
                self.masina_repository.update(masina)
            else:
                masina.in_garantie = 'Nu'
                self.masina_repository.update(masina)

        self.undo_redo_service.clear_redo()
        update_operation = UpdateGarantieOperation(self.masina_repository,
                                                   masini_updated, masini)
        self.undo_redo_service.add_to_undo(update_operation)
