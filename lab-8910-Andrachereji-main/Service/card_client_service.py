from Domain.add_operation import AddOperation
from Domain.card_client import Card_client
from Domain.delete_operation import DeleteOperation
from Domain.update_operation import UpdateOperation
from Domain.validator_card_client import Card_clientValidator
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService


class Card_clientService:
    def __init__(self, card_client_repository: Repository,
                 card_client_validator: Card_clientValidator,
                 undo_redo_service: UndoRedoService):
        self.card_client_repository = card_client_repository
        self.card_client_validator = card_client_validator
        self.undo_redo_service = undo_redo_service

    def adaugare_card_client(self, id_card_client, nume, prenume,
                             cnp, data_nasterii, data_inregistrarii):
        '''
        Adauga un card in repository
        :param id_card_client: id-ul cardului care se adauga
        :param nume: numele detinatorului cardului
        :param prenume: prenumele detinatorului cardului
        :param cnp: cnp-ul detinatorului cardului
        :param data_nasterii:data nasterii detinatorlui cardului
        :param data_inregistrarii: data inregistrarii cardului
        '''
        card_client = Card_client(id_card_client, nume, prenume,
                                  cnp, data_nasterii, data_inregistrarii)
        self.card_client_validator.validate(card_client)
        self.card_client_repository.create(card_client)

        self.undo_redo_service.clear_redo()
        add_operation = AddOperation(self.card_client_repository, card_client)
        self.undo_redo_service.add_to_undo(add_operation)

    def update_card_client(self, id_card_client, nume, prenume,
                           cnp, data_nasterii, data_inregistrarii):
        '''
        Actualizeaza un card existent in repository
        :param id_card_client: id-ul cardului care se actualizeaza
        :param nume: numele detinatorului cardului
        :param prenume: prenumele detinatorului cardului
        :param cnp: cnp-ul detinatorului cardului
        :param data_nasterii:data nasterii detinatorlui cardului
        :param data_inregistrarii: data inregistrarii cardului
        '''
        card_client = self.card_client_repository.read(id_card_client)
        card_client_updated = Card_client(id_card_client, nume, prenume,
                                          cnp, data_nasterii,
                                          data_inregistrarii)
        self.card_client_validator.validate(card_client_updated)
        self.card_client_repository.update(card_client_updated)

        self.undo_redo_service.clear_redo()
        update_operation = UpdateOperation(self.card_client_repository,
                                           card_client_updated,
                                           card_client)
        self.undo_redo_service.add_to_undo(update_operation)

    def stergere_card_client(self, id_card_client):
        '''
        Sterge un card din repository
        :param id_card_client: id-ul cardului care se sterge
        '''
        card_client = self.card_client_repository.read(id_card_client)
        self.card_client_repository.delete(id_card_client)

        self.undo_redo_service.clear_redo()
        delete_operation = DeleteOperation(self.card_client_repository,
                                           card_client)
        self.undo_redo_service.add_to_undo(delete_operation)

    def get_all(self):
        '''
        Afiseaza toate cardurile din repository
        :return: lista cu toate cardurile
        '''
        return self.card_client_repository.read()
