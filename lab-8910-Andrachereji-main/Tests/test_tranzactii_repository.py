from Repository.json_repository import JsonRepository
from Repository.tranzactie_repository import TranzactieRepository
from utils import clear_file
from Domain.tranzactie import Tranzactie


def test_tranzactie_repository():
    filename = 'test_t.json'
    clear_file(filename)
    tranzactie_repository = JsonRepository(filename)
    added = Tranzactie('1', '1', '1', 120, 100, '12.12.2020', '10.00')
    tranzactie_repository.create(added)
    assert tranzactie_repository.read(added.id_entity) == added
    tranzactie_repository.delete(added.id_entity)
    assert tranzactie_repository.read(added.id_entity) is None
    tranzactie_repository.create(added)
    updated = Tranzactie('1', '1', '1', 1300, 1400, '11.12.2020', '11.00')
    tranzactie_repository.update(updated)
    assert tranzactie_repository.read(added.id_entity) == updated
