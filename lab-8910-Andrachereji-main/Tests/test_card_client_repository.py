from Domain.card_client import Card_client
from Repository.card_client_repository import Card_clientRepository
from Repository.json_repository import JsonRepository

from utils import clear_file


def test_card_client_repository():
    filename = 'test_c.json'
    clear_file(filename)
    card_client_repository = JsonRepository(filename)
    added = Card_client('1', 'Chereji', 'Andra',
                        '6020702125808', '02.07.2002', '10.10.2020')
    card_client_repository.create(added)
    assert card_client_repository.read(added.id_entity) == added
    card_client_repository.delete(added.id_entity)
    assert card_client_repository.read(added.id_entity) is None
    card_client_repository.create(added)
    updated = Card_client('1', 'Chereji', 'Miruna',
                          '6030752125808', '02.08.2003', '10.10.2020')
    card_client_repository.update(updated)
    assert card_client_repository.read(added.id_entity) == updated
