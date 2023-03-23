from Domain.masina import Masina
from Domain.validator_masina import MasinaValidator
from Repository.json_repository import JsonRepository
from Service.masina_service import MasinaService
from Service.undo_redo_service import UndoRedoService
from utils import clear_file


def test_masina_service():
    filename = 'test_m.json'
    clear_file(filename)
    masina_repository = JsonRepository(filename)
    masina_validator = MasinaValidator()
    undo_redo_service = UndoRedoService()
    masina_service = MasinaService(masina_repository,
                                   masina_validator,
                                   undo_redo_service)
    added = Masina('100', 'dacia', 2000, 1200, 'Da')
    masina_service.adaugare_masina('100', 'dacia', 2000, 1200, 'Da')
    assert masina_repository.read(added.id_entity) == added
    undo_redo_service.do_undo()
    assert masina_repository.read(added.id_entity) is None
    undo_redo_service.do_redo()
    assert masina_repository.read(added.id_entity) == added
    updated = Masina('100', 'dacia', 2010, 1020, 'Nu')
    masina_service.update_masina('100', 'dacia', 2010, 1020, 'Nu')
    assert masina_repository.read(added.id_entity) == updated
    undo_redo_service.do_undo()
    assert masina_repository.read(added.id_entity) == added
    undo_redo_service.do_redo()
    assert masina_repository.read(added.id_entity) == updated
    masina_service.stergere_masina(updated.id_entity)
    assert masina_repository.read(updated.id_entity) is None
    undo_redo_service.do_undo()
    assert masina_repository.read(updated.id_entity) == updated
    undo_redo_service.do_redo()
    assert masina_repository.read(updated.id_entity) is None
    masina_service.random_cars(2)
    assert len(masina_service.get_all()) == 2
    undo_redo_service.do_undo()
    assert len(masina_service.get_all()) == 0
    undo_redo_service.do_redo()
    assert len(masina_service.get_all()) == 2
    masina_service.adaugare_masina('1', 'dacia', 2020, 50000, 'Nu')
    masina_service.adaugare_masina('2', 'dacia', 2010, 500000, 'Da')
    masina_service.actualizare_garantie()
    masina1 = masina_repository.read('1')
    masina2 = masina_repository.read('2')
    assert masina1.in_garantie == 'Da'
    assert masina2.in_garantie == 'Nu'
    undo_redo_service.do_undo()
    assert masina_repository.read('2').in_garantie == 'Da'
    undo_redo_service.do_redo()
    assert masina_repository.read('2').in_garantie == 'Nu'
