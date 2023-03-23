from Domain.card_client import Card_client
from Domain.masina import Masina
from Domain.tranzactie import Tranzactie
from Repository.json_repository import JsonRepository
from Service.tranzactie_service import TranzactieService
from Service.undo_redo_service import UndoRedoService
from utils import clear_file


def test_tranzactii_service():
    filename1 = 'test_t.json'
    filename2 = 'test_m.json'
    filename3 = 'test_c.json'
    clear_file(filename1)
    clear_file(filename2)
    clear_file(filename3)
    tranzactie_repository = JsonRepository(filename1)
    masina_repository = JsonRepository(filename2)
    card_client_repository = JsonRepository(filename3)
    undo_redo_service = UndoRedoService()
    tranzactie_service = TranzactieService(tranzactie_repository,
                                           masina_repository,
                                           card_client_repository,
                                           undo_redo_service)
    masina = Masina('100', 'dacia', 2000, 1200, 'Da')
    card_client = Card_client('1', 'Chereji', 'Andra',
                              '6020702125808', '02.07.2002', '10.10.2020')
    masina_repository.create(masina)
    card_client_repository.create(card_client)
    added = Tranzactie('1', '100', '1', 120, 100, '12.12.2020', '10.00')
    tranzactie_service.adaugare_tranzactie('1', '100', '1', 120, 100,
                                           '12.12.2020', '10.00')
    new_added = Tranzactie('1', '100', '1', 0, 90, '12.12.2020', '10.00')
    assert tranzactie_repository.read(added.id_entity) == new_added
    undo_redo_service.do_undo()
    assert tranzactie_repository.read(added.id_entity) is None
    undo_redo_service.do_redo()
    assert tranzactie_repository.read(added.id_entity) == new_added
    updated = Tranzactie('1', '100', '1', 140, 130, '12.12.2020', '10.00')
    tranzactie_service.update_tranzactie('1', '100', '1', 140, 130,
                                         '12.12.2020', '10.00')
    assert tranzactie_repository.read(added.id_entity) == updated
    undo_redo_service.do_undo()
    assert tranzactie_repository.read(added.id_entity) == new_added
    undo_redo_service.do_redo()
    assert tranzactie_repository.read(added.id_entity) == updated
    tranzactie_service.stergere_tranzactie(updated.id_entity)
    assert tranzactie_repository.read(updated.id_entity) is None
    undo_redo_service.do_undo()
    assert tranzactie_repository.read(added.id_entity) == updated
    undo_redo_service.do_redo()
    assert tranzactie_repository.read(updated.id_entity) is None
    result = tranzactie_service.get_interval(100, 300)
    assert result is not None
    ordonat_masini = tranzactie_service.\
        get_ordonare_masini_dupa_suma_manopera()
    for masina in ordonat_masini:
        assert masina.suma_manopera == max(m.suma_manopera for m
                                           in ordonat_masini)
    ordonat_carduri = tranzactie_service.get_ordonare_card_dupa_reducere()
    for card in ordonat_carduri:
        assert card.suma_reducere == max(c.suma_reducere for c
                                         in ordonat_carduri)
    tranzactie_service.adaugare_tranzactie('2', '100', '1', 100, 100,
                                           '11.10.2021', '11.00')
    tranzactie_service.adaugare_tranzactie('3', '100', '1', 200, 100,
                                           '17.11.2021', '11.00')
    tranzactie_service.stergere_tranzactii_interval('10.10.2021', '20.11.2021')
    assert tranzactie_repository.read('2') is None
    assert tranzactie_repository.read('3') is None
    undo_redo_service.do_undo()
    assert tranzactie_repository.read('2') is not None
    assert tranzactie_repository.read('3') is not None
    undo_redo_service.do_redo()
    assert tranzactie_repository.read('2') is None
    assert tranzactie_repository.read('3') is None
    tranzactie_service.adaugare_tranzactie('2', '100', '1', 100, 100,
                                           '11.10.2021', '11.00')
    tranzactie_service.adaugare_tranzactie('3', '100', '1', 200, 100,
                                           '17.11.2021', '11.00')
    tranzactie_service.stergere_tranzactie_masina('100')
    assert tranzactie_repository.read('2') is None
    assert tranzactie_repository.read('3') is None
    undo_redo_service.do_undo()
    assert tranzactie_repository.read('2') is not None
    assert tranzactie_repository.read('3') is not None
    undo_redo_service.do_redo()
    assert tranzactie_repository.read('2') is None
    assert tranzactie_repository.read('3') is None
