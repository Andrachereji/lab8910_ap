from Domain.validator_card_client import Card_clientValidator
from Domain.validator_masina import MasinaValidator
from Repository.json_repository import JsonRepository
from Service.card_client_service import Card_clientService
from Service.masina_service import MasinaService
from Service.tranzactie_service import TranzactieService
from Service.undo_redo_service import UndoRedoService
from Tests.test_card_client_repository import test_card_client_repository
from Tests.test_card_client_service import test_card_client_service
from Tests.test_masina_repository import test_masina_repository
from Tests.test_masina_service import test_masina_service
from Tests.test_my_sorted import test_my_sorted
from Tests.test_tranzactii_repository import test_tranzactie_repository
from Tests.test_tranzactii_service import test_tranzactii_service
from Tests.test_validator_card_client import test_card_client_validator
from Tests.test_validator_masina import test_masina_validator
from UserInterface.Console import Console


def main():
    undo_redo_service = UndoRedoService()

    masina_repository = JsonRepository('masini.json')
    masina_validator = MasinaValidator()
    masina_service = MasinaService(masina_repository,
                                   masina_validator,
                                   undo_redo_service)

    card_client_repository = JsonRepository('card_client.json')
    card_client_validator = Card_clientValidator()
    card_client_service = Card_clientService(card_client_repository,
                                             card_client_validator,
                                             undo_redo_service)

    tranzactie_repository = JsonRepository('tranzactie.json')
    tranzactie_service = TranzactieService(tranzactie_repository,
                                           masina_repository,
                                           card_client_repository,
                                           undo_redo_service)

    console = Console(masina_service,
                      card_client_service,
                      tranzactie_service,
                      undo_redo_service)
    console.run_console()


if __name__ == '__main__':
    test_masina_repository()
    test_card_client_repository()
    test_tranzactie_repository()
    test_masina_service()
    test_card_client_service()
    test_tranzactii_service()
    test_card_client_validator()
    test_masina_validator()
    test_my_sorted()
    main()
