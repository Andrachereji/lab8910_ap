from Domain.card_client import Card_client
from Domain.validator_card_client import Card_clientValidator
from Repository.card_client_repository import Card_clientRepository
from Repository.json_repository import JsonRepository
from Service.card_client_service import Card_clientService
from Service.undo_redo_service import UndoRedoService
from utils import clear_file


def test_card_client_service():
    filename = 'test_c.json'
    clear_file(filename)
    card_client_repository = JsonRepository(filename)
    card_client_validator = Card_clientValidator()
    undo_redo_service = UndoRedoService()
    card_client_service = Card_clientService(card_client_repository,
                                             card_client_validator,
                                             undo_redo_service)
    added = Card_client('1', 'Chereji', 'Andra',
                        '6020702125808', '02.07.2002', '10.10.2020')
    card_client_service.adaugare_card_client('1', 'Chereji', 'Andra',
                                             '6020702125808',
                                             '02.07.2002', '10.10.2020')
    assert card_client_repository.read(added.id_entity) == added
    undo_redo_service.do_undo()
    assert card_client_repository.read(added.id_entity) is None
    undo_redo_service.do_redo()
    assert card_client_repository.read(added.id_entity) == added
    updated = Card_client('1', 'Chereji', 'Miruna',
                          '6020702125808', '02.10.2002', '10.10.2020')
    card_client_service.update_card_client('1', 'Chereji', 'Miruna',
                                           '6020702125808', '02.10.2002',
                                           '10.10.2020')
    assert card_client_repository.read(added.id_entity) == updated
    undo_redo_service.do_undo()
    assert card_client_repository.read(added.id_entity) == added
    undo_redo_service.do_redo()
    assert card_client_repository.read(added.id_entity) == updated
    card_client_service.stergere_card_client(updated.id_entity)
    assert card_client_repository.read(updated.id_entity) is None
    undo_redo_service.do_undo()
    assert card_client_repository.read(updated.id_entity) == updated
    undo_redo_service.do_redo()
    assert card_client_repository.read(updated.id_entity) is None
