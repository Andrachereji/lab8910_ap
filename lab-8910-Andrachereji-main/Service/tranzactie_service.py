from Domain.add_operation import AddOperation
from Domain.multiple_delete_operation import MultipleDeleteOperation
from Domain.delete_operation import DeleteOperation
from Domain.tranzactie import Tranzactie
from Domain.update_operation import UpdateOperation
from Repository.exceptions import NoSuchIdError
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService
from ViewModels.card_client_reduceri import Card_clientReducere
from ViewModels.masina_suma_manopera import MasinaSuma_manopera
from utils import my_sorted


class TranzactieService:
    def __init__(self,
                 tranzactie_repository: Repository,
                 masina_repository: Repository,
                 card_client_repository: Repository,
                 undo_redo_service: UndoRedoService):
        self.tranzactie_repository = tranzactie_repository
        self.masina_repository = masina_repository
        self.card_client_repository = card_client_repository
        self.undo_redo_service = undo_redo_service

    def adaugare_tranzactie(self, id_tranzactie, id_masina, id_card_client,
                            suma_piese, suma_manopera, data, ora):
        '''
        Adauga o tranzactie in repository
        :param id_tranzactie: id-ul tranzactiei care se adauga
        :param id_masina: id-ul masinii
        :param id_card_client:id-ul cardului
        :param suma_piese:pretul pieselor
        :param suma_manopera:pretul manoperei
        :param data:data tranzactiei
        :param ora: ora tranzactiei
        '''

        tranzactie = Tranzactie(id_tranzactie, id_masina, id_card_client,
                                suma_piese, suma_manopera, data, ora)
        if self.masina_repository.read(id_masina) is None:
            raise KeyError(f'Nu exista masina cu id-ul {id_masina}')

        if tranzactie.id_card_client != '':
            tranz = tranzactie.suma_manopera
            tranz1 = tranz - ((10 / 100) * tranz)
            tranzactie.suma_manopera = tranz1
        masina = self.masina_repository.read(tranzactie.id_masina)
        if masina.in_garantie == 'Da':
            tranzactie.suma_piese = 0
        self.tranzactie_repository.create(tranzactie)

        self.undo_redo_service.clear_redo()
        add_operation = AddOperation(self.tranzactie_repository, tranzactie)
        self.undo_redo_service.add_to_undo(add_operation)

    def update_tranzactie(self, id_tranzactie, id_masina, id_card_client,
                          suma_piese, suma_manopera, data, ora):
        '''
        Actualizeaza o tranzactie din repository
        :param id_tranzactie: id-ul tranzactiei care se actualizeaza
        :param id_masina: id-ul masinii
        :param id_card_client:id-ul cardului
        :param suma_piese:pretul pieselor
        :param suma_manopera:pretul manoperei
        :param data:data tranzactiei
        :param ora: ora tranzactiei
        '''
        tranzactie = self.tranzactie_repository.read(id_tranzactie)
        tranzactie_updated = Tranzactie(id_tranzactie, id_masina,
                                        id_card_client, suma_piese,
                                        suma_manopera, data, ora)
        if self.masina_repository.read(id_masina) is None:
            raise NoSuchIdError(f'Nu exista masina cu id-ul {id_masina}')
        self.tranzactie_repository.update(tranzactie_updated)

        self.undo_redo_service.clear_redo()
        update_operation = UpdateOperation(self.tranzactie_repository,
                                           tranzactie_updated,
                                           tranzactie)
        self.undo_redo_service.add_to_undo(update_operation)

    def stergere_tranzactie(self, id_tranzactie):
        '''
        Sterge o tranzactie din repository
        :param id_tranzactie: id-ul tranzactiei care se sterge
        '''

        tranzactie = self.tranzactie_repository.read(id_tranzactie)
        self.tranzactie_repository.delete(id_tranzactie)

        self.undo_redo_service.clear_redo()
        delete_operation = DeleteOperation(self.tranzactie_repository,
                                           tranzactie)
        self.undo_redo_service.add_to_undo(delete_operation)

    def get_all(self):
        '''
        Afiseaza toate tranzactiile din repository
        :return:lista cu toate tranzactiile
        '''

        return self.tranzactie_repository.read()

    def get_interval(self, capat_stanga, capat_dreapta):
        '''
        Afiseaza tranzactiile care au suma_manopera in
        intervalul [capat_stanga, capat_dreapta]
        :param capat_stanga: capatul din stanga a intervalului
        :param capat_dreapta: capatul din dreapta a intervalului
        :return: o lista cu tranzactiile cu proprietatea ceruta
        '''
        result = []
        tran = self.tranzactie_repository.read()
        for tranzactie in tran:
            if capat_dreapta >= tranzactie.suma_manopera \
                    >= capat_stanga:
                result.append(tranzactie)
        return result

    def get_ordonare_masini_dupa_suma_manopera(self):
        '''
        Ordoneaza masinile din repository dupa suma manoperei
        :return:o lista cu masinile ordonate
        '''

        def inner(masini):
            if not masini:
                return []
            else:
                masina = masini[0]
                tranzactie_masina = filter(lambda tranzactie:
                                           tranzactie.id_masina ==
                                           masina.id_entity, self.get_all())
                suma_manopere = sum([tranzactie.suma_manopera
                                     for tranzactie in tranzactie_masina])
                return [MasinaSuma_manopera(masina.model, masina.an_achizitie,
                                            masina.nr_km,
                                            masina.in_garantie,
                                            suma_manopere)] + inner(masini[1:])

        masini = self.masina_repository.read()
        result = inner(masini)
        # for masina in self.masina_repository.read():
        # tranzactie_masina = filter(lambda tranzactie:
        # tranzactie.id_masina ==
        # masina.id_entity, self.get_all())
        # suma_manopere = sum([tranzactie.suma_manopera
        # for tranzactie in tranzactie_masina])
        # result.append(
        # MasinaSuma_manopera(masina.model, masina.an_achizitie,
        # masina.nr_km, masina.in_garantie,
        # suma_manopere))
        return my_sorted(result, key=lambda x: x.suma_manopera, reverse=True)

    def get_ordonare_card_dupa_reducere(self):
        '''
        Ordoneaza cardurile clientilor in functie de reducerile aplicate
        :return:o lista cu cardurile ordonate
        '''
        result = []
        for card in self.card_client_repository.read():
            tranzactie_card = filter(lambda tranzactie:
                                     tranzactie.id_card_client
                                     == card.id_entity, self.get_all())
            suma_reduceri = sum([((10 / 100) * tranzactie.suma_manopera)
                                 for tranzactie in tranzactie_card])
            result.append(Card_clientReducere(card.nume, card.prenume,
                                              card.cnp, card.data_nasterii,
                                              card.data_inregistrarii,
                                              suma_reduceri))
        return sorted(result, key=lambda x: x.suma_reducere, reverse=True)

    def stergere_tranzactii_interval(self, data_inainte, data_dupa):
        '''
        Sterge tranzactiile care au data intr-un interval dat
        :param data_inainte:data din stanga intervalului
        :param data_dupa:data din dreapta intervalului
        :return:
        '''
        tran = self.get_all()
        left = []
        right = []
        undo_redo = []
        left_str = data_inainte.split('.')
        for nr in left_str:
            left.append(int(nr))
        right_str = data_dupa.split('.')
        for nr in right_str:
            right.append(int(nr))
        for tranzactie in tran:
            lst = []
            lst_str = tranzactie.data.split('.')
            for data in lst_str:
                lst.append(int(data))
            if left[2] < lst[2] < right[2]:
                self.stergere_tranzactie(tranzactie.id_entity)
                undo_redo.append(tranzactie)
            elif left[2] == lst[2] and left[1] < lst[1]:
                self.stergere_tranzactie(tranzactie.id_entity)
                undo_redo.append(tranzactie)
            elif right[2] == lst[2] and lst[1] < right[1]:
                self.stergere_tranzactie(tranzactie.id_entity)
                undo_redo.append(tranzactie)
            elif left[1] == lst[1] and lst[0] >= left[0]:
                self.stergere_tranzactie(tranzactie.id_entity)
                undo_redo.append(tranzactie)
            elif lst[1] == right[1] and lst[0] <= right[0]:
                self.stergere_tranzactie(tranzactie.id_entity)
                undo_redo.append(tranzactie)
        self.undo_redo_service.clear_redo()
        delete_operation = MultipleDeleteOperation(
            self.tranzactie_repository, undo_redo)
        self.undo_redo_service.add_to_undo(delete_operation)

    def stergere_tranzactie_masina(self, id_masina):
        '''
        Sterge toate tranzactiile care au id-ul masinii "id_masina"
        :param id_masina: id-ul masinii
        '''
        tranzactii = self.get_all()
        deleted = []
        for tranzactie in tranzactii:
            if tranzactie.id_masina == id_masina:
                deleted.append(tranzactie)
                self.tranzactie_repository.delete(tranzactie.id_entity)
        self.undo_redo_service.clear_redo()
        delete_operation = MultipleDeleteOperation(
            self.tranzactie_repository, deleted)
        self.undo_redo_service.add_to_undo(delete_operation)
