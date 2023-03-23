from Domain.masina import Masina
from Domain.validator_masina import MasinaValidator


def test_masina_validator():
    masina_validator = MasinaValidator()
    valid1 = Masina('1', 'dacia', 2020, 1200, 'Da')
    masina_validator.validate(valid1)
    assert masina_validator.validate(valid1) is None
