from Domain.card_client import Card_client
from Domain.validator_card_client import Card_clientValidator


def test_card_client_validator():
    card_client_validator = Card_clientValidator()
    valid1 = Card_client('1', 'Chereji', 'Andra',
                         '6020702125808', '02.07.2002',
                         '10.10.2020')
    card_client_validator.validate(valid1)
    assert card_client_validator.validate(valid1) is None
