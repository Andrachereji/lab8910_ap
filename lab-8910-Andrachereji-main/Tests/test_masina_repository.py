from Domain.masina import Masina
from Repository.json_repository import JsonRepository
from Repository.masina_repository import MasinaRepository

from utils import clear_file


def test_masina_repository():
    filename = 'test_m.json'
    clear_file(filename)
    masina_repository = JsonRepository(filename)
    added = Masina('1', 'mercedes', 2015, 100500, 'Da')
    masina_repository.create(added)
    assert masina_repository.read(added.id_entity) == added
    masina_repository.delete(added.id_entity)
    assert masina_repository.read(added.id_entity) is None
    masina_repository.create(added)
    updated = Masina('1', 'citroen', 2013, 100000, 'Da')
    masina_repository.update(updated)
    assert masina_repository.read(added.id_entity) == updated
